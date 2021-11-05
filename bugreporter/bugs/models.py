from django.conf import settings
from django.db import models


class Report(models.Model):
    name = models.CharField(max_length=255)
    text = models.TextField(max_length=5000)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='UserReport')
    tags = models.ManyToManyField('tags.Tag', related_name='ReportTags')
    comment = models.ManyToManyField('Comment', related_name='ReportComment')
    stage = models.ForeignKey('stages.WorkStages', on_delete=models.CASCADE, related_name='ReportStage')
    isOpenned = models.BooleanField(default=True)


class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='UserComment')
    report = models.ForeignKey(Report, on_delete=models.CASCADE, related_name='ReportComment')
    text = models.TextField(max_length=5000)
