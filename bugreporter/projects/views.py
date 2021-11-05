from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ViewSet

from authserver.models import UserToken
from extras.decorators import is_logged_in, is_not_token_valid
from extras.slugify import slugify
from projects import Serializers
from projects.Serializers import CreateProjectSerializer
from projects.models import Project


class UserProjects(ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = CreateProjectSerializer
    user_key = ''

    def get_queryset(self):
        token = self.request.session.get('name')
        if token is None:
            raise ValidationError({'error': 'You not logged in'})
        user_get = User.objects.filter(username=self.kwargs.get('username')).first()
        if user_get == UserToken.objects.filter(key=token).first().user:
            return self.queryset.filter(user=user_get)
        return self.queryset.filter(user=user_get, visible=True)

    def get_serializer(self, *args, **kwargs):
        token = self.request.session.get('name')
        if token is None:
            raise ValidationError({'error': 'You not logged in'})
        serializer_class = self.get_serializer_class()
        kwargs.setdefault('context', self.get_serializer_context())
        return serializer_class(*args, **kwargs)

    @is_not_token_valid
    @is_logged_in
    def create(self, request, *args, **kwargs):
        create_info = dict(request.data)
        user = UserToken.objects.filter(key=request.session.get('name')).first().user
        create_info['user'] = user.id
        if user.username != self.kwargs['username']:
            raise ValidationError({'error': 'That project is not your'})
        create_info['name'] = slugify(create_info['name'][0])
        serializer = self.get_serializer(data=create_info)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'response': 'created'})

    @is_logged_in
    def destroys(self, request, *args, **kwargs):
        project_id = self.kwargs['id']
        project = Project.objects.filter(id=project_id, user__username=self.kwargs['username'])
        if not project.exists():
            raise ValidationError({'error': 'Project not found in your projects.'})
        self.perform_destroy(project.first())
        return Response({'response': 'successful delete.'})


class Settings(ViewSet):
    @is_logged_in
    @is_not_token_valid
    def update(self, request, *args, **kwargs):
        token = self.request.session.get('name')
        if token is None:
            raise ValidationError({'error': 'You not logged in'})
        user_get = User.objects.filter(username=self.kwargs.get('username')).first()
        project = Project.objects.filter(name=self.kwargs['projectname'], user=user_get)
        if not project.exists():
            raise ValidationError({'error': 'This project not found in your project.'})
        project = project.first()
        visible = True if not project.visible else False
        project.visible = visible
        project.save()
        return Response({'response': 'Visible successfully updated.'})
