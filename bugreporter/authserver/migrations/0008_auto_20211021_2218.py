# Generated by Django 3.2.8 on 2021-10-21 18:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authserver', '0007_auto_20211021_1931'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='reports',
        ),
        migrations.RemoveField(
            model_name='project',
            name='user',
        ),
        migrations.RemoveField(
            model_name='report',
            name='stage',
        ),
        migrations.RemoveField(
            model_name='report',
            name='tag',
        ),
        migrations.RemoveField(
            model_name='report',
            name='user',
        ),
        migrations.AlterField(
            model_name='usertoken',
            name='key',
            field=models.CharField(default='f798cac14468450a995a96f141d7ca11', max_length=255),
        ),
        migrations.DeleteModel(
            name='Comment',
        ),
        migrations.DeleteModel(
            name='Project',
        ),
        migrations.DeleteModel(
            name='Report',
        ),
        migrations.DeleteModel(
            name='Tags',
        ),
        migrations.DeleteModel(
            name='WorkStages',
        ),
    ]
