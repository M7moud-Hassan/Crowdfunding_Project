# Generated by Django 4.1.6 on 2023-02-18 17:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth_app', '0004_rename_set_password_registeruser_user_password'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registeruser',
            name='first_name',
            field=models.CharField(max_length=29),
        ),
        migrations.AlterField(
            model_name='registeruser',
            name='last_name',
            field=models.CharField(max_length=28),
        ),
        migrations.AlterField(
            model_name='registeruser',
            name='user_password',
            field=models.CharField(max_length=26),
        ),
    ]
