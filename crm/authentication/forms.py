from django import forms

from django.contrib.auth.models import User

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

       if not User.objects.filter(username=email).exists():
           
           self.add_error('email','not a registered email address')