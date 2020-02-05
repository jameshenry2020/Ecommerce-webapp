from django import forms
from django.contrib.auth.forms import UserCreationForm
from account.models import MyAccount
from django.contrib.auth import authenticate

class RegisterationForm(UserCreationForm):
    email=forms.EmailField(max_length=60, help_text='please provide a valid email')

    class Meta:
        model = MyAccount
        fields =('first_name','last_name','email','username','phone','password1','password2')

class AccountAuthenticationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    class Meta:
        model=MyAccount
        fields=('email', 'password')

    def clean(self):
        if self.is_valid():
            email =self.cleaned_data['email']
            password = self.cleaned_data['password']

            if not authenticate(email=email, password=password):
                raise forms.ValidationError('invalid login')


class UserProfileUpdateForm(forms.ModelForm):

    class Meta:
        model = MyAccount
        fields = ('email','first_name','last_name', 'username','phone')

    def clean_email(self):
        if self.is_valid():
            email = self.cleaned_data['email']
            try:
                account =MyAccount.objects.exclude(pk=self.instance.pk).get(email=email)
            except MyAccount.DoesNotExist:
                return email
            raise forms.ValidationError('email"%s" is already in use.'% account)

    def clean_username(self):
        if self.is_valid():
            username = self.cleaned_data['username']
            try:
                account =MyAccount.objects.exclude(pk=self.instance.pk).get(username=username)
            except MyAccount.DoesNotExist:
                return username
            raise forms.ValidationError('username"%s" is already in use.'% account.username)