from django.db import models

# Create your models here.

class RegisterUser(models.Model):
    user_id = models.AutoField(primary_key=True)
    first_name=models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    user_email = models.CharField(max_length=70)
    user_password = models.CharField(max_length=30)
    user_mobile = models.CharField(max_length=11)
    user_image = models.ImageField(max_length=255)


#models.SlugField(max_length=255)