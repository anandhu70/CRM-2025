from django.template import Library

from payments.models import Payment

from django.utils import timezone

register=Library()

@register.simple_tag

def check_payment_obj_exists(request):

    student=request.user.students

    course= request.user.students.course


    exists=False

    if Payment.objects.filter(student=student,course=course).exists():

        exists=True

    return exists 

@register.simple_tag

def check_amount_to_be_paid(request,payment_option,no_of_emi):

    course = request.user.students.course

    fee = course.fee

    print(payment_option,no_of_emi)  

@register.simple_tag
def check_due_date(due_date):

    current_date = timezone.now().date()

    late = False

    if current_date > due_date:

        late = True

    return late     

