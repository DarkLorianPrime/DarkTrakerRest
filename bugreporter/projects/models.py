from django.db import models
from django.conf import settings
from bugs.models import Report
from stages.models import WorkStages


class Project(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='User_Project')
    visible = models.BooleanField(default=True)
    reports = models.ManyToManyField(Report, related_name='Project_Reports')
