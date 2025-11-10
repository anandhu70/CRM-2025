from django import forms

from .models import Students ,EducationChoices, BatchChoices,DistrictChoices,TrainerChoices,CourseChoices

# for making it as models

from course.models import Course

from batch.models import Batch

from trainer.models import Trainer

import re

class AddStudentForm(forms.ModelForm):

    class Meta :

        model  =  Students

        # profile in exclude  bcs random generation of id and pass

        exclude = ['join_date','adm_num','uuid','active_status','profile']

        widgets = {

            'first_name' : forms.TextInput(attrs={'class': "form-control"}),

            'last_name' : forms.TextInput(attrs={'class': "form-control"}),

            'email' : forms.EmailInput(attrs={'class': "form-control"}),

            'contact_num': forms.TextInput(attrs={'class': "form-control"}),

            'photo' : forms.FileInput(attrs={'class': "form-control"}),

            'dob' : forms.DateInput(attrs={'class': "form-control",'type':"date"}),

            'address': forms.TextInput(attrs={'class': "form-control"}),

            'place': forms.TextInput(attrs={'class': "form-control"}),
            
            'pincode': forms.TextInput(attrs={'class': "form-control"}),

        }
    # choice feild for boxes 
    education = forms.ChoiceField(choices=EducationChoices.choices, widget= forms.Select(attrs={'class':'form-select'}))

    batch = forms.ModelChoiceField(queryset=Batch.objects.all(),widget= forms.Select(attrs={'class' : 'form-select'}))

    course = forms.ModelChoiceField(queryset=Course.objects.all(),widget=forms.Select(attrs={'class' : 'form-select'}))

    trainer = forms.ModelChoiceField(queryset=Trainer.objects.all(),widget=forms.Select(attrs={'class' : 'form-select'}))

    district = forms.ChoiceField(choices= DistrictChoices.choices,widget=forms.Select(attrs={'class' : 'form-select'}))
   

#    for custom validation
    def clean(self):
        cleaned_data= super().clean()

        pincode=cleaned_data.get('pincode')

        email=cleaned_data.get('email')

        contact_num= cleaned_data.get('contact_num')


        if len(pincode) < 6:

            self.add_error('pincode','pincode must be 6 digits')
                                                            #for edit no need to chech email exits

        if Students.objects.filter(email=email).exists() and not self.instance:

            self.add_error('email','this email already taken')    

        username,domain=email.split('@')

        domain_list=[

                "gmail.com",
                "yahoo.com",
                "outlook.com",
                "hotmail.com",
                "icloud.com",
                "aol.com",
               "protonmail.com",
              "zoho.com",
               "yandex.com",
               "mail.com",
               "mailinator.com"
            ]
        
        if domain not in domain_list:

            self.add_error('email','invalid email adress')
                                                                         #for edit 
        if Students.objects.filter(contact_num=contact_num).exists() and not self.instance:

            self.add_error('contact_num','this contact number already taken')      

        pattern='(\\+91)?\\d{10}'

        match=re.fullmatch(pattern,contact_num)

        if not match:

            self.add_error('contact_num','invalid phone number')

        #  in edit email already exits occur bcs of required  so need to chnge the required option 

    # def __init__(self,*args,**kwargs) :

    #     super(AddStudentForm,self).__init__(*args,**kwargs) 

    #     if not self.instance:
    #                                  #attrs in dict form to add smthng use []
    #         self.fields.get('email').widget.attrs['required']='required'  