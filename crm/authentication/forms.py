from django import forms

from django.contrib.auth.models import User


from .models import Profile

class LoginForm(forms.Form):

    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control',
                                                            'required':'required'}))
    
    password = forms.CharField(max_length=20,widget=forms.PasswordInput(attrs={'class':'form-control',
                                                                               'required':'required'}))
    
    def clean(self):

       cleaned_data =  super().clean()

       email = cleaned_data.get('email')

       username,domain = email.split('@')

       domain_list = ["gmail.com",
                       "yahoo.com",
                       "outlook.com",
                       "hotmail.com",
                       "icloud.com",
                       "aol.com",
                       "protonmail.com",
                       "zoho.com",
                      "yandex.com",
                       "mail.com",
                       "mailinator.com"]
        
       if domain not in domain_list :
            
            self.add_error('email','invalid email address')

            # user chnges to profile 

       if not Profile.objects.filter(username=email).exists():
           
           self.add_error('email','not a registered email address')


class OTPForm(forms.Form):

    email_otp = forms.CharField(max_length=4,widget=forms.TextInput(attrs={'class':'form-control',
                                                            'required':'required'}))
    
    phone_otp = forms.CharField(max_length=4,widget=forms.TextInput(attrs={'class':'form-control',
                                                                               'required':'required'})) 

    def clean(self):

       cleaned_data =  super().clean()

       email_otp = cleaned_data.get('email_otp')

       phone_otp = cleaned_data.get('phone_otp')

       if len(email_otp)  <4: 
           
           self.add_error('email_otp','invalid email otp')

       if len(phone_otp) < 4 :
           
           self.add_error('phone_otp','invalid phone otp')



class ChangePasswordForm(forms.Form):

    password = forms.CharField(max_length=15,widget=forms.TextInput(attrs={'class':'form-control',
                                                            'required':'required'}))
    
    confirm_password = forms.CharField(max_length=15,widget=forms.TextInput(attrs={'class':'form-control',
                                                                               'required':'required'})) 

    def clean(self):

       cleaned_data =  super().clean()

       password = cleaned_data.get('password')

       confirm_password = cleaned_data.get('confirm_password')

       if password != confirm_password: 
           
           self.add_error('confirm_password','Password Mismatch')

       

