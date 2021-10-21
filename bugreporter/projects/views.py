from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet, ModelViewSet

from authserver.models import UserToken
from extras.decorators import is_logged_in
from projects.Serializers import CreateProjectSerializer
from projects.models import Project


class UserProjects(ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = CreateProjectSerializer
    user_key = ''

    def get_serializer(self, *args, **kwargs):
        token = self.request.session.get('name')
        if token is None:
            raise ValidationError({'error': 'You not logged in'})
        serializer_class = self.get_serializer_class()
        kwargs.setdefault('context', self.get_serializer_context())
        return serializer_class(*args, **kwargs)

    @is_logged_in
    def create(self, request, *args, **kwargs):
        create_info = dict(request.data)
        create_info['user'] = UserToken.objects.filter(key=request.session.get('name')).first().user.id
        create_info['name'] = create_info['name'][0]
        serializer = self.serializer_class(data=create_info)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'response': 'created'})

    @is_logged_in
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        project = Project.objects.filter(id=instance.id, user=UserToken.objects.filter(key=request.session.get('name')).first().user)
        if not project.exists():
            return Response({'error': f'Project "{instance.name}" not found in your projects.'})
        self.perform_destroy(instance)
        return Response({'response': 'successful delete.'})
# class UserProjects(ViewSet):
#     @is_logged_in
#     def get_projects(self, request, username, *args, **kwargs):
#         user = User.objects.filter(username=username)
#         if not user.exists():
#             return Response({'error': 'User does not exist'})
#         projects = Project.objects.filter(user=user.first())
#         if not projects.exists():
#             return Response({'error': f'Not found projects for {username}'})
#         # report_list = Report.objects.filter(user=user_reports.first()).values('name', 'tag', 'stage', 'isOpenned')
#         return Response({'response': projects.values('name')})
#
#     @is_logged_in
#     def list_projects(self, request, *args, **kwargs):
#         projects = Project.objects.filter()
#         if not projects.exists():
#             return Response({'error': 'Not found projects.'})
#         return Response({'response': projects.values('name', 'user__username')})
#
#     @is_logged_in
#     def create_project(self, request, *args, **kwargs):
#         user = UserToken.objects.filter(key=kwargs['key']).first().user.id
#         create = CreateProjectSerializer(data={'name': request.POST.get('name'), 'user': user})
#         create.is_valid(raise_exception=True)
#         create.save()
#         return Response({'response': 'Created'})
#
#     @is_logged_in
#     def delete_project(self, request, *args, **kwargs):
#         user = UserToken.objects.filter(key=kwargs['key']).first().user.id
#         # project = Project.objects.filter(user=UserToken.objects.filter(key=request.session.get('name')).first())
#         # if project.exists():
#         #     return Response({'error': 'This project already exists.'})
#