# Generated by Django 3.2.8 on 2021-10-21 15:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('authserver', '0006_alter_usertoken_key'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='user',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='UserProject', to='auth.user'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='usertoken',
            name='key',
            field=models.CharField(default='eec867d43c5c4b8986be23040a9ff6ea', max_length=255),
        ),
    ]
