# Generated by Django 3.2.8 on 2021-10-20 20:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authserver', '0004_auto_20211020_2315'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usertoken',
            name='key',
            field=models.CharField(default='fa2947f0536b446789876620e827b804', max_length=255),
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('reports', models.ManyToManyField(related_name='ProjectReports', to='authserver.Report')),
            ],
        ),
    ]
