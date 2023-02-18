from django import forms
from django.core.validators import RegexValidator
from django.contrib.auth.hashers import make_password
from .models import RegisterUser

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    mobile_phone = forms.CharField(validators=[
        RegexValidator(regex='^(01)[0125][0-9]{8}$', message='wrong number')
    ])

    class Meta:
        model = RegisterUser
        fields = ['first_name', 'last_name', 'user_email', 'user_image']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("passwords are not matched !!!")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_password = make_password(self.cleaned_data['password'])
        user.is_active = False
        if commit:
            user.save()
        return user


