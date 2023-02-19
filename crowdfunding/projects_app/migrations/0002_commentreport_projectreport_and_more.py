# Generated by Django 4.1.6 on 2023-02-14 09:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('projects_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CommentReport',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('report', models.CharField(default='bad', max_length=200)),
                ('comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects_app.comment')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects_app.user')),
            ],
        ),
        migrations.CreateModel(
            name='ProjectReport',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('report', models.CharField(default='bad', max_length=200)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects_app.project')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects_app.user')),
            ],
        ),
        migrations.RemoveField(
            model_name='project_report',
            name='project',
        ),
        migrations.RemoveField(
            model_name='project_report',
            name='user',
        ),
        migrations.RemoveField(
            model_name='donation',
            name='created_at',
        ),
        migrations.DeleteModel(
            name='Comment_Report',
        ),
        migrations.DeleteModel(
            name='Project_Report',
        ),
    ]