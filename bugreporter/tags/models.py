from django.db import models


class Tag(models.Model):
    tag = models.CharField(max_length=255)
    project = models.ForeignKey('projects.Project', on_delete=models.CASCADE, related_name='TagStage')
# Create your models here.
