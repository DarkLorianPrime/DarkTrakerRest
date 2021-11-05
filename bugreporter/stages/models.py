from django.conf import settings
from django.db import models


class WorkStages(models.Model):
    project = models.ForeignKey('projects.Project', on_delete=models.CASCADE, blank=True, null=True, related_name='Report_Stage')
    stage = models.CharField(max_length=255)
