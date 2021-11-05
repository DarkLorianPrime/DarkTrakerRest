import datetime
import uuid

from django.core.exceptions import BadRequest
from django.utils.deprecation import MiddlewareMixin
from rest_framework.response import Response

from token_receiver.models import PostToken


class TokenMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.method == 'POST' or request.method == 'DELETE':
            if request.POST.get('token') is not None:
                token = PostToken.objects.filter(token=request.POST.get('token'))
                if token.exists():
                    if token.first().created.replace(tzinfo=None) <= datetime.datetime.now():
                        PostToken.objects.update(token=uuid.uuid4().hex,
                                                 created=datetime.datetime.now() + datetime.timedelta(minutes=30))
                        request.token = 'Need update'
                        return
                    else:
                        request.token = token
                        return
            else:
                request.token = 'Not passed'
                return
            request.token = None
            return
