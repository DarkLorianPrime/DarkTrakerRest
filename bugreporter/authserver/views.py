from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from authserver.serializer import RegistrationSerializer
from extras.decorators import is_logged_in, is_not_logged_in, is_not_token_valid
from extras.isCheckers import isEmail
from authserver.models import UserToken


class Login(ViewSet):
    def isLoggined(self, request, *args, **kwargs):
        return Response({'response': request.session['name']}) if request.session.get('name') is not None else Response({'error': 'not authenticated'}, status=400)

    @is_not_token_valid
    @is_not_logged_in
    def login(self, request, *args, **kwargs):
        if request.POST.get('username') is None or request.POST.get('password') is None:
            return Response({'error': 'invalid username/email or password'}, status=400)
        email = isEmail(request.POST.get('username'))
        username = request.POST.get('username')
        if email:
            user = User.objects.filter(email=request.POST.get('username'))
            username = user.first().username if user.exists() else request.POST.get('username')
        auth_user = authenticate(request, username=username, password=request.POST.get('password'))
        if auth_user is not None:
            key = UserToken.objects.get_or_create(user=auth_user)
            request.session['name'] = key[0].key
            return Response({'login': key[0].key})
        return Response({'error': 'login failed. Password or login is not found.'}, status=400)


class Regisration(ViewSet):
    def isRegistered(self, request, *args, **kwargs):
        return Response({'response': request.session['name']}) if request.session.get('name') is not None else Response({'error': 'not authenticated'}, status=400)

    @is_not_token_valid
    @is_not_logged_in
    def registration(self, request, *args, **kwargs):
        new_user = RegistrationSerializer(data=request.POST)
        new_user.is_valid(raise_exception=True)
        new_user.save()
        return Response({'response': new_user.instance.username})


class Logout(ViewSet):
    @is_logged_in
    def logout(self, request, *args, **kwargs):
        del request.session['name']
        return Response({'response': 'logout'})
