from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ViewSet

from authserver.models import UserToken
from bugs.Serializers import BugSerializer, CommentSerializer
from bugs.models import Report
from stages.models import WorkStages
from extras.decorators import is_logged_in, is_not_token_valid
from projects.models import Project


class BugsReport(ModelViewSet):
    queryset = Report.objects.all()
    serializer_class = BugSerializer

    def get_queryset(self):
        token = self.request.session.get('name')
        if token is None:
            raise ValidationError({'error': 'You not logged in'})
        username = UserToken.objects.filter(key=token).first().user
        filter = Project.objects.filter(name=self.kwargs.get('projectname'),
                                        user=User.objects.filter(username=self.kwargs.get('username')).first())
        if self.kwargs.get('username') != username.username:
            d = filter.filter(visible=True)
        else:
            d = filter
        if not d.exists():
            raise ValidationError({'error': 'project not found'})
        return d.first().reports

    @is_not_token_valid
    @is_logged_in
    def create(self, request, *args, **kwargs):
        post = request.POST
        token = self.request.session.get('name')
        username = UserToken.objects.filter(key=token).first().user
        project = Project.objects.filter(name=self.kwargs.get('projectname'), user=username)
        stage = WorkStages.objects.filter(project=project.first(), id=post.get('stage')).first()
        if stage is None:
            stage = WorkStages.objects.filter(project=None, id=post.get('stage')).first()
        serialize = self.get_serializer(
            data={'name': post.get('name'), 'text': post.get('text'), 'stage': stage.id, 'user': username.id})
        serialize.is_valid(raise_exception=True)
        serialize.save()
        if not project.exists():
            raise ValidationError({'error': 'This is not your project, or this project is not exists.'})
        project.first().reports.add(serialize.instance)
        return Response({'response': 'Successfully created'})


class BugsVisible(ViewSet):
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
        report = Report.objects.filter(project=project, user=user_get, id=kwargs['bug'])
        if not report.exists():
            raise ValidationError({'error': 'This report not found in this project.'})
        report = report.first()
        open = True if not report.isOpenned else False
        report.isOpenned = open
        report.save()
        return Response({'response': 'Report isOpened successfully updated.'})


class CommentsWithReports(ModelViewSet):
    serializer_class = CommentSerializer

    def get_queryset(self, *args, **kwargs):
        token = self.request.session.get('name')
        if token is None:
            raise ValidationError({'error': 'You not logged in'})
        username = UserToken.objects.filter(key=token).first().user
        filter = Project.objects.filter(name=self.kwargs['projectname'],
                                        user=User.objects.filter(username=self.kwargs['username']).first())
        d = filter.filter(visible=True) if self.kwargs.get('username') != username.username else filter
        if not d.exists():
            raise ValidationError({'error': 'project not found'})
        if d.first().reports.filter(id=self.kwargs['bug']).first() is not None:
            return d.first().reports.filter(id=self.kwargs['bug']).first()
        raise ValidationError({'error': 'Report not found.'})

    @is_logged_in
    @is_not_token_valid
    def create(self, request, *args, **kwargs):
        username = UserToken.objects.filter(key=self.request.session.get('name')).first()
        report = self.get_queryset()
        text = request.POST.get('text')
        if text is None:
            raise ValidationError({'error': '"text" not specified'})
        serialize = self.get_serializer(data={'user': username.user.id, 'report': report.id, 'text': text})
        serialize.is_valid(raise_exception=True)
        serialize.save()
        report.comment.add(serialize.instance)
        return Response({'response': 'Successfully commented'})

    def list(self, request, *args, **kwargs):
        return Response({'response': self.get_queryset().comment.values_list('text')})