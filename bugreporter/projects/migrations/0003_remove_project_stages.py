# Generated by Django 3.2.8 on 2021-11-03 11:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0002_project_stages'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='stages',
        ),
    ]
