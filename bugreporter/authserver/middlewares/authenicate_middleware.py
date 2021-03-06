from django.contrib.auth import authenticate
from django.utils.deprecation import MiddlewareMixin

from authserver.models import UserToken


class LoginMiddleware(MiddlewareMixin):
    def process_request(self, request):
        request.account = request.session.get('name')
