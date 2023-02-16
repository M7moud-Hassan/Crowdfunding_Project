from django import forms
from django.core.validators import RegexValidator
from .models import RegisterUser
import sys

sys.setrecursionlimit(1500)
class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    mobile_phone = forms.CharField(validators=
          [RegexValidator(regex='^(01)[0125][0-9]{8}$', message='wrong number')])

    class Meta:
        model = RegisterUser
        fields = ['first_name', 'last_name', 'user_email','user_image']

    def clean(self):
        password = self.cleaned_data.get('user_password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("passwords are not matched !!!")



    def save(self, commit=True):
        user = self.save(commit=True)
        user.user_password(self.cleaned_data['user_password'])
        user.is_active = False
        if commit:
            user.save()
        return user


