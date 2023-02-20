from django import forms
from django.core.validators import RegexValidator, FileExtensionValidator
from django.forms import NumberInput

from .models import RegisterUser


class UserRegistrationForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(
        attrs={
            "placeholder": "First Name",
            "class": "form-control"
        }))
    last_name = forms.CharField(widget=forms.TextInput(
        attrs={
            "placeholder": "Last Name",
            "class": "form-control"
        }))
    user_email = forms.EmailField(max_length=200, help_text='Required', widget=forms.EmailInput(attrs={
        "placeholder": "Email",
        "class": "form-control"
    }))
    user_password = forms.CharField(widget=forms.PasswordInput(attrs={
        "placeholder": "Password",
        "class": "form-control"
    }))

    confirmPassword = forms.CharField(label="confirm password", widget=forms.PasswordInput(attrs={
        "placeholder": "Confirm Password",
        "class": "form-control"
    }))
    user_mobile = forms.CharField(label="phone number", validators=[RegexValidator(
        '^01[0125][0-9]{8}$', message="Enter a  Egyption Phone Number")], widget=forms.TextInput(attrs={
        "placeholder": "Phone Number",
        "class": "form-control"
    }))
    user_image = forms.ImageField(label="profile image", validators=[FileExtensionValidator(['jpg', 'png', 'jpeg'])],
                                  widget=forms.FileInput(attrs={
                                      "placeholder": "Profile Image",
                                      "class": "form-control"
                                  }))

    def clean(self):
        errors = {}
        valpassword = self.cleaned_data.get('user_password')
        valconfirmpassword = self.cleaned_data.get("confirmPassword")
        if valpassword != valconfirmpassword:
            errors['confirmPassword'] = ('password not match')
        user_email = self.cleaned_data.get('user_email')
        if RegisterUser.objects.filter(user_email=user_email).exists():
            errors['user_email'] = ("Email exists")
        phone = self.cleaned_data.get('user_mobile')
        if RegisterUser.objects.filter(user_mobile=phone).exists():
            errors['user_mobile'] = ("phone exists")
        if errors:
            raise forms.ValidationError(errors)

    class Meta:
        model = RegisterUser
        fields = ('first_name', 'last_name', 'user_email',
                  'user_password', 'confirmPassword', 'user_mobile', 'user_image')


class LoginForm(forms.Form):
    email = forms.EmailField(max_length=200, help_text='Required', widget=forms.EmailInput(attrs={
        "placeholder": "Email",
        "class": "form-control"
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        "placeholder": "Password",
        "class": "form-control"
    }))


class EditProfileForm(forms.ModelForm):
    first_name = forms.CharField(

        widget=forms.TextInput(
            attrs={
                "placeholder": "First Name",
                "class": "form-control",

            }),
        min_length=2,
        max_length=10,

    )
    last_name = forms.CharField(widget=forms.TextInput(
        attrs={
            "placeholder": "Last Name",
            "class": "form-control"
        }),
        min_length=2,
        max_length=10,
    )
    user_mobile = forms.CharField(label="phone number", validators=[RegexValidator(
        '^01[0125][0-9]{8}$', message="Enter a  egypt Phone Number")], widget=forms.TextInput(attrs={
        "placeholder": "Phone Number",
        "class": "form-control"
    }))
    user_image = forms.ImageField(required=False, label="profile image",
                                  validators=[FileExtensionValidator(['jpg', 'png', 'jpeg'])],
                                  widget=forms.FileInput(attrs={
                                      "placeholder": "Profile Image",
                                      "class": "form-control"
                                  }))
    user_password = forms.CharField(required=False, widget=forms.PasswordInput(attrs={
        "placeholder": "Password",
        "class": "form-control"
    }))

    confirmPassword = forms.CharField(required=False, label="confirm password", widget=forms.PasswordInput(attrs={
        "placeholder": "Confirm Password",
        "class": "form-control"
    }))
    country = forms.CharField(required=False, validators=[RegexValidator(
        '^[A-Za-z]+$', message="Enter a Valid Country Name")], widget=forms.TextInput(
        attrs={
            "placeholder": "Country",
            "class": "form-control"
        }))
    birthdate = forms.DateField(required=False,
                                widget=NumberInput(
                                    attrs={
                                        'placeholder': 'BirthDate',
                                        'type': 'date',
                                        'class': 'form-control'
                                    }
                                ))
    facebook_profile = forms.URLField(required=False, error_messages={'required': 'Please Enter a valid Url'},
                                      widget=forms.URLInput(
                                          attrs={
                                              'placeholder': 'Profile Facebook Url',
                                              'class': 'form-control'
                                          }
                                      ))

    def clean(self):
        errors = {}
        password = self.cleaned_data.get('user_password')
        confirmpassword = self.cleaned_data.get("confirmPassword")
        if password != confirmpassword:
            errors['confirmPassword'] = ('password not match')
        phone = self.cleaned_data.get('user_mobile')
        if RegisterUser.objects.filter(user_mobile=phone).exclude(pk=self.instance.pk).exists():
            errors['user_mobile'] = ("phone exists")
        if errors:
            raise forms.ValidationError(errors)

    class Meta:
        model = RegisterUser
        fields = ('first_name', 'last_name', 'user_mobile', 'user_image', 'country', 'user_password', 'birthdate',
                  'facebook_profile')


class DeleteAccountForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        "placeholder": "Password",
        "class": "form-control"
    }))


class PasswordEmailForm(forms.Form):
    email = forms.EmailField(max_length=200, help_text='Required', widget=forms.EmailInput(attrs={
        "placeholder": "Email",
        "class": "form-control"
    }))


class PasswordForm(forms.ModelForm):
    user_password = forms.CharField(widget=forms.PasswordInput(attrs={
        "placeholder": "Password",
        "class": "form-control"
    }))
    confirmPassword = forms.CharField(label="confirm password", widget=forms.PasswordInput(attrs={
        "placeholder": "Confirm Password",
        "class": "form-control"
    }))

    def clean(self):
        errors = {}
        valpassword = self.cleaned_data.get('user_password')
        valconfirmpassword = self.cleaned_data.get("confirmPassword")
        if valpassword != valconfirmpassword:
            errors['confirmPassword'] = ('password not match')
        if errors:
            raise forms.ValidationError(errors)

    class Meta:
        model = RegisterUser
        fields = ['user_password']
