# Generated by Django 4.1.6 on 2023-02-14 10:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects_app', '0002_commentreport_projectreport_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reply',
            name='created_at',
        ),
        migrations.AlterField(
            model_name='commentreport',
            name='report',
            field=models.CharField(default='bad', max_length=10),
        ),
        migrations.AlterField(
            model_name='projectreport',
            name='report',
            field=models.CharField(default='bad', max_length=10),
        ),
    ]
