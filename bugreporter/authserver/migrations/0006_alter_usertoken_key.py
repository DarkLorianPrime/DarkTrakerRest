# Generated by Django 3.2.8 on 2021-10-21 15:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authserver', '0005_auto_20211021_0025'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usertoken',
            name='key',
            field=models.CharField(default='cbd071a81e0b4c81bebbf4827f5280ef', max_length=255),
        ),
    ]