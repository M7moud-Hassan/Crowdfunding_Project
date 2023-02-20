from django.db import models



# Create your models here.

class RegisterUser(models.Model):
    user_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=29)
    last_name = models.CharField(max_length=28)
    user_email = models.EmailField(max_length=200)
    user_password = models.CharField(max_length=150)
    is_active = models.BooleanField(default=False)
    is_delete = models.BooleanField(default=False)
    user_mobile = models.CharField(max_length=11, unique=True, null=True)
    user_image = models.ImageField(verbose_name="photo", upload_to="uploads/users/")
    birthdate = models.DateField(null=True)
    facebook_profile = models.URLField(null=True)
    country = models.CharField(max_length=30, null=True)

    def __str__(self):
        fullName = f"" + (self.first_name + " " + self.last_name)
        return fullName
