# Generated by Django 4.1.6 on 2023-02-17 19:26

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registeruser',
            name='user_email',
            field=models.EmailField(max_length=70),
        ),
        migrations.AlterField(
            model_name='registeruser',
            name='user_image',
            field=models.ImageField(blank=True, null=True, upload_to='image/'),
        ),
        migrations.AlterField(
            model_name='registeruser',
            name='user_mobile',
            field=models.CharField(max_length=11, validators=[django.core.validators.RegexValidator(message='wrong number', regex='^(01)[0125][0-9]{8}$')]),
        ),
    ]