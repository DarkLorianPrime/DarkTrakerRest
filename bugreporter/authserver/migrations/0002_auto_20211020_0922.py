# Generated by Django 3.2.8 on 2021-10-20 05:22

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('authserver', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='posttoken',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='usertoken',
            name='key',
            field=models.CharField(default='fc391ef868574f60a88be98dc19bc7be', max_length=255),
        ),
    ]
