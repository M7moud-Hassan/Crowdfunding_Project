# Generated by Django 4.1.6 on 2023-02-18 17:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth_app', '0005_alter_registeruser_first_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registeruser',
            name='user_password',
            field=models.CharField(max_length=150),
        ),
    ]