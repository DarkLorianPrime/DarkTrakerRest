import uuid

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models


class PostToken(models.Model):
    token = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.token


class UserToken(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='UserToken')
    key = models.CharField(max_length=255, default=uuid.uuid4().hex)

    def __str__(self):
        return self.key
