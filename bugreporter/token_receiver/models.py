import datetime

from django.db import models


class PostToken(models.Model):
    token = models.CharField(max_length=255)
    created = models.DateTimeField(default=datetime.datetime.now() + datetime.timedelta(minutes=30))

    def __str__(self):
        return self.token
