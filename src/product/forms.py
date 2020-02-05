from django import forms

PAYMENT_METHOD=(
    ('C','credit card'),
    ('P', 'paypal')
)

class CheckOutForm(forms.Form):
    building_number=forms.CharField(label='apartment no', widget=forms.TextInput(attrs={
        'placeholder':'Apartment no',
        'class':'form-control'
    }))
    street_name=forms.CharField(widget=forms.TextInput(attrs={
        'placeholder':'street name',
         'class':'form-control'
    }))
    area=forms.CharField(widget=forms.TextInput())
    city=forms.CharField(widget=forms.TextInput())
    save_as_default=forms.BooleanField(widget=forms.CheckboxInput())
    payment_option=forms.ChoiceField(widget=forms.RadioSelect,  choices=PAYMENT_METHOD)


class ContactForm(forms.Form):
    subject=forms.CharField(label='Subject', widget=forms.TextInput(attrs={
        'class':'form-control',
         'placeholder':'subject....'
    }))
    email=forms.EmailField(widget=forms.EmailInput(attrs={
        'class':'form-control'
    }))