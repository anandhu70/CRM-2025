from django.shortcuts import render,redirect

from django.views import View

from .forms import LoginForm,OTPForm,ChangePasswordForm

from django.contrib.auth import authenticate,login,logout

# for messages and notification

from django.contrib import messages

# Create your views here.

#from django.contrib.auth.models import User

# for otp

from crm.utils import generate_otps,sent_mail,send_otp_sms,masking_email_and_phone

from django.utils.decorators import method_decorator

from authentication.permissions import permited_users

import threading

from django.utils import timezone
# for reset password
from django.contrib.auth import update_session_auth_hash

class LoginView(View):

    form_class = LoginForm

    def get(self,request,*args,**kwargs):

        form = self.form_class()

        data = {'form':form}

        return render(request,'authentication/login.html',context=data)
    
    def post(self,request,*args,**kwargs):

        form = self.form_class(request.POST)

        error = None

        if form.is_valid():

            email = form.cleaned_data.get('email')

            password = form.cleaned_data.get('password')

            user = authenticate(username=email,password=password)

            if user:

                login(request,user)

                messages.success(request,'successfully logined')

                return redirect('dashboard')
            
            error = 'invalid email or password'
        
        data = {'form':form,'error':error}

        return render(request,'authentication/login.html',context=data)
    


    # logout view 
class LogoutView(View):

    def get (self,request,*args,**kwargs):

        logout(request)

        return redirect('login')
    

@method_decorator(permited_users(['Student']),name='dispatch')   
class OtpView(View):

    form_class=OTPForm

    def get(self,request,*args,**kwargs):

        form=self.form_class()

        email_otp,phone_otp= generate_otps()

        # to add it to database(reverse coupling)

        otp=request.user.otp

        otp.email_otp=email_otp

        otp.phone_otp= phone_otp

        otp.save()

        recepient=request.user.students.email

        template= 'email/otp-email.html'

        context={'otp':email_otp,'name':f'{request.user.students.first_name}{request.user.students.last_name}'}

        title= 'Request To Change Password'

        thread=threading.Thread(target=sent_mail,args=(recepient,template,context,title))

        thread.start()


        send_otp_sms(phone_otp)
                                                                #   model in reversed
        masked_email,masked_phone=masking_email_and_phone(request.user.students.email,request.user.students.contact_num)
            # storage--immdiate data    current  (date) time  
        request.session['otp_time']= timezone.now().timestamp()

        remaining_time= 600

        data={'form':form,'masked_email':masked_email,'masked_phone':masked_phone,'remaining_time':remaining_time}

        return render(request,'authentication/otp.html',context=data)  

  

#   for otp verification and database and otp equals
    def post(self,request,*args,**kwargs):

        form=self.form_class(request.POST) 

        error= None 

        if form.is_valid():

            form_email_otp=form.cleaned_data.get('email_otp')

            form_phone_otp=form.cleaned_data.get('phone_otp')

            otp=request.user.otp

            db_email_otp=otp.email_otp

            db_phone_otp=otp.phone_otp

            otp_time=request.session.get('otp_time')

            current_time= timezone.now().timestamp()

            if otp_time:

                elapsed=current_time - otp_time

                # remaining time for invalid otp in correct time

                remaining_time= max(0,600 - int(elapsed))

                if elapsed>600:

                    error= 'OTP expired Request a New One'

            
                elif  form_email_otp== db_email_otp and form_phone_otp == db_phone_otp:

                    messages.success(request,'OTPs verified')

                    request.session.pop('otp_time')

                    # to avoid direct page

                    otp.otp_verified = True


                    otp.save()

                    return redirect('change-password')
                
                else:

                    error= 'Invalid OTP'

        data={'error':error,'remaining_time':remaining_time }        

        return render(request,'authentication/otp.html',context=data)  
@method_decorator(permited_users(['Student']),name='dispatch')
class ChangePasswordView(View):

    form_class= ChangePasswordForm

    def get(self,request,*args,**kwargs) :
         
        #  avoid direct 
         
         if request.user.otp.otp_verified:
             
            form=self.form_class()

            data={'form':form}

            return render (request,'authentication/password.html',context=data) 
         
         else:
             
             return redirect('otp')
             


    def post (self,request,*args,**kwarg) :

        form= self.form_class(request.POST)  

        if form.is_valid ():

            password=form.cleaned_data.get('password')

            user=request.user
                    #defaulth methd
            user.set_password(password) 

            user.save()

            # to avoid direct otp page load and as per condition need to chnge it to false

            otp=user.otp

            otp.otp_verified =False

            otp.save()




            update_session_auth_hash(request,user)
             


            messages.success(request,'Password Updated Successfully')  

            return redirect('dashboard')
        
        data={'form':form}

        return render(request,'authentication/password.html',context=data)


                    

            

            
    


    