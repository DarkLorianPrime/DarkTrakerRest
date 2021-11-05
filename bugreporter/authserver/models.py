import uuid

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models


class UserToken(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='User_Token')
    key = models.CharField(max_length=255, default=uuid.uuid4().hex)

    def __str__(self):
        return self.key
