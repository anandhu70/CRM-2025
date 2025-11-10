from django import forms

from . models import Course

class AddCourseForm(forms.ModelForm):

    class Meta:

        model= Course

        exclude=['active_status','uuid']

        widgets={

            'name':forms.TextInput(attrs={'class':'form-control','required':'required'}),
            'code':forms.TextInput(attrs={'class':'form-control','required':'required'}),
            'fee':forms.TextInput(attrs={'class':'form-control','required':'required'}),
            'offer_percent':forms.TextInput(attrs={'class':'form-control','required':'required'}),
            'mode':forms.CheckboxSelectMultiple(attrs={'class':'form-check-input'}),






        }

    