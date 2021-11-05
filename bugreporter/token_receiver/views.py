import datetime
import uuid

from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from token_receiver.models import PostToken


class getToken(ViewSet):
    def get_token(self, request, *args, **kwargs):
        token = PostToken.objects.first()
        if token is None:
            token = PostToken.objects.create(token=uuid.uuid4().hex)
            return Response({'response': token.token})
        if token.created.replace(tzinfo=None) <= datetime.datetime.now():
            PostToken.objects.update(token=uuid.uuid4().hex, created=datetime.datetime.now() + datetime.timedelta(minutes=30))
            return Response({'response': PostToken.objects.first().token})
        return Response({'response': token.token})
