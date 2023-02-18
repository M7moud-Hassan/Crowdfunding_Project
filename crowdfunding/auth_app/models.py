from django.db import models
from django.conf import settings
from django.conf.urls.static import static
from django.core.validators import RegexValidator
from django.contrib.auth.hashers import make_password



# Create your models here.

class RegisterUser(models.Model):
    user_id = models.AutoField(primary_key=True)
    first_name=models.CharField(max_length=29)
    last_name = models.CharField(max_length=28)
    user_email = models.EmailField(max_length=70)
    user_password = models.CharField(max_length=150)
    user_mobile = models.CharField(max_length=11, validators=[
        RegexValidator(regex='^(01)[0125][0-9]{8}$', message='wrong number')])
    user_image = models.ImageField(upload_to ='image/', null=True, blank=True )

