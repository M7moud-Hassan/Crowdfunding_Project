from django.db import models


# Create your models here.
class Category (models.Model):
    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=50)



class Category(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=50)


class Projects(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50)
    details = models.CharField(max_length=500)
    total_target = models.BigIntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    start = models.DateTimeField()
    end = models.DateTimeField()


<<<<<<< HEAD
class Pictures(models.Model):
    id = models.BigAutoField(primary_key=True)
    image = models.ImageField()
=======
class Pictures (models.Model):
    id=models.BigAutoField(primary_key=True)
    image=models.ImageField()
    id_project = models.ForeignKey(Projects, on_delete=models.CASCADE)

class Tags (models.Model):
    id=models.AutoField(primary_key=True)
    tag=models.CharField(max_length=50)
>>>>>>> 3f8f0790425663e809cb964dce59297cd30ef6ce
    id_project = models.ForeignKey(Projects, on_delete=models.CASCADE)


class Tags(models.Model):
    id = models.BigAutoField(primary_key=True)
    tag = models.CharField(max_length=50)
    id_project = models.ForeignKey(Projects, on_delete=models.CASCADE)

# def user_directory_path(instance, filename):
#     # file will be uploaded to MEDIA_ROOT / user_<id>/<filename>
#     return 'user_{0}/{1}'.format(instance.user.id, filename)
#
#
# class MyModel(models.Model):
#     upload = models.ImageField(upload_to=user_directory_path)
