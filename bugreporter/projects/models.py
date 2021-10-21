from django.db import models
from django.conf import settings


class Report(models.Model):
    name = models.CharField(max_length=255)
    text = models.TextField(max_length=5000)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='UserReport')
    tag = models.ManyToManyField('Tags', related_name='ReportTags')
    stage = models.ForeignKey('WorkStages', on_delete=models.CASCADE, related_name='ReportStage')
    isOpenned = models.BooleanField(default=True)


class Project(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='UserProject')
    reports = models.ManyToManyField('Report',  related_name='ProjectReports')


class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='UserComment')
    post = models.ForeignKey('Report', on_delete=models.CASCADE, related_name='ReportComment')
    text = models.TextField(max_length=5000)


class WorkStages(models.Model):
    stage = models.CharField(max_length=255)


class Tags(models.Model):
    tag = models.CharField(max_length=255)
    forComments = models.BooleanField(default=False)
