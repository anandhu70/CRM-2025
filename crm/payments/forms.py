from django import forms

from . models import Payment,PaymentOptionChoices,EMINumberChoices

class SetPaymentForm(forms.ModelForm):

    class Meta:

        model= Payment

        exclude=['active_status','uuid','student','course','fee','amount_to_be_paid','full_paid']

    payment_option= forms.ChoiceField(choices=PaymentOptionChoices.choices, widget= forms.Select(attrs={'class':'form-select'}))

    no_of_emi= forms.ChoiceField(choices=EMINumberChoices.choices, widget= forms.Select(attrs={'class':'form-select'}))

        