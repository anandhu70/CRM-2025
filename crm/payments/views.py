from django.shortcuts import render,redirect

from django.views import View

from .forms import SetPaymentForm

from django.utils.decorators import method_decorator

from authentication.permissions import permited_users

from .models import Payment,EMI,Transaction

from django.utils import timezone

from django.db import transaction

import razorpay

from decouple import  config

from django.contrib import messages

from django.db.models import Sum

# pdf related imports

from django.template.loader import render_to_string

from weasyprint import HTML

from django.http import HttpResponse

# Create your views here.
@method_decorator(permited_users(['Student']),name='dispatch')
class StudentPaymentView(View):

    def get(self,request,*args,**kwargs):

        return render(request,'payments/student-payment.html')
@method_decorator(permited_users(['Student']),name='dispatch')
class StudentPaymentSetView(View):

    form_class = SetPaymentForm

    def get(self,request,*args,**kwargs):

        form = self.form_class()

        data = {'form':form}

        return render(request,'payments/set-payment.html',context=data)
    
    def post(self,request,*args,**kwargs):

        form = self.form_class(request.POST)

        if form.is_valid():

            with transaction.atomic():

                payment = form.save(commit=False)

                course = request.user.students.course

                payment.student = request.user.students

                payment.course = course

                payment.fee = course.fee

                amount_to_be_paid = course.fee

                payment_option = form.cleaned_data.get('payment_option')

                if form.cleaned_data.get('payment_option') == 'One Time':

                    amount_to_be_paid = course.fee

                    payment.no_of_emi = 0


                    if course.offer_percent:

                        amount_to_be_paid = course.fee-(course.fee*course.offer_percent/100)

                    payment.amount_to_be_paid  = amount_to_be_paid

                    payment.save()

                    

                elif form.cleaned_data.get('payment_option') == 'EMI' :

                    no_of_emi = form.cleaned_data.get('no_of_emi')

                    if no_of_emi == '2' :

                        amount_to_be_paid = course.fee+(course.fee*5/100)

                    elif no_of_emi == '3' :

                        amount_to_be_paid = course.fee+(course.fee*10/100)

                payment.amount_to_be_paid  = amount_to_be_paid

                payment.save()

                days = 10

                for i in range(1,payment.no_of_emi+1):

                    amount = payment.amount_to_be_paid/payment.no_of_emi

                    due_date = payment.student.join_date + timezone.timedelta(days=days)

                    EMI.objects.create(payment=payment,installment_no=i,amount=amount,due_date=due_date)

                    days += 25



                return redirect('student-payment')
        
        data = {'form':form}

        return render(request,'payments/set-payment.html',context=data)
    
@method_decorator(permited_users(['Student']),name='dispatch')    
class StudentPaymentListView(View):

    def get(self,request,*args,**kwargs):

        payment = Payment.objects.get(student=request.user.students,course=request.user.students.course)

        data = {'payment':payment}

        return render(request,'payments/payment-list.html',context=data)
    
@method_decorator(permited_users(['Student']),name='dispatch')    
class RazorPayView(View):

    def get(self,request,*args,**kwargs):

        student = request.user.students

        course = request.user.students.course

        payment = Payment.objects.get(student=student,course=course)

        
        client = razorpay.Client(auth=(config('RZP_CLIENT_ID'), config('RZP_CLIENT_SECRET')))


        if payment.payment_option == 'One Time':

            amount=payment.amount_to_be_paid

            data = { "amount": amount*100, "currency": "INR", "receipt": "order_rcptid_11" }

            order = client.order.create(data=data) 

            order_id = order.get('id')



            Transaction.objects.create(payment=payment,rzp_order_id=order_id,amount=amount)

        elif payment.payment_option == 'EMI':

            uuid  = kwargs.get('uuid')

            emi = EMI.objects.get(uuid=uuid)

            amount = emi.amount

            data = { "amount": amount*100, "currency": "INR", "receipt": "order_rcptid_11" }

            order = client.order.create(data=data) 

            order_id = order.get('id')

            Transaction.objects.create(payment=payment,emi=emi,rzp_order_id=order_id,amount=amount)

        data = {'RZP_CLIENT_ID':config('RZP_CLIENT_ID'),'amount':amount,'order_id':order_id}

        return render(request,'payments/razorpay.html',context=data)
    
class PaymentVerifyView(View):

    def post(self,request,*args,**kwargs):

        data = request.POST

        razorpay_order_id = data.get('razorpay_order_id')

        razorpay_payment_id = data.get('razorpay_payment_id')

        razorpay_signature = data.get('razorpay_signature')

        client = razorpay.Client(auth=(config('RZP_CLIENT_ID'), config('RZP_CLIENT_SECRET')))
        
        verified = client.utility.verify_payment_signature({
                                                'razorpay_order_id': razorpay_order_id,
                                                'razorpay_payment_id': razorpay_payment_id,
                                                'razorpay_signature': razorpay_signature
                                                })
        transaction = Transaction.objects.get(rzp_order_id=razorpay_order_id)

        transaction.rzp_payment_id = razorpay_payment_id

        transaction.rzp_signature = razorpay_signature

        transaction.transaction_at = timezone.now()

        if verified:
            
            transaction.status = 'Success'

            messages.success(request,'Payment Successful')

            if transaction.payment.payment_option == 'One Time':

                transaction.payment.full_paid = True

                transaction.payment.save()

            elif transaction.payment.payment_option == 'EMI':

                transaction.emi.paid = True

                transaction.emi.save()

                total = EMI.objects.filter(payment=transaction.payment,paid=True).aggregate(Sum('amount'))['amount__sum']

                if total == transaction.payment.amount_to_be_paid :

                    transaction.payment.full_paid = True

                    transaction.payment.save()
                
        else:

            transaction.status ='Failed'

            messages.error(request,'Payment Failed')

        transaction.save()
            
        return redirect('payment-list')
    
class GeneratePDFView(View):

    def get(self,request,*args,**kwargs):

        student = request.user.students

        course = student.course

        payment = Payment.objects.get(student=student,course=course)

        if payment.payment_option == 'One Time':

            transaction = Transaction.objects.get(payment=payment,status='Success')
        
        elif payment.payment_option == 'EMI':

            uuid = kwargs.get('uuid')

            emi = EMI.objects.get(uuid = uuid)

            transaction = Transaction.objects.get(payment=payment,emi=emi,status='Success')

        context = {'transaction':transaction}

        template = 'payments/invoice.html'

        content =  render_to_string(template,context)

        pdf = HTML(string=content)

        response = HttpResponse(content_type='application/pdf')

        response['Content-Dispositon'] = f'inline; filename="{transaction.payment.student.first_name}-{transaction.payment.student.last_name}-payment.pdf"'

        pdf.write_pdf(response)

        return response