from django.db.models import Q
from django.shortcuts import render

# Create your views here.
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ViewSet

from authserver.models import UserToken
from bugs.models import Report
from extras.decorators import is_not_token_valid, is_logged_in
from projects.models import Project
from tags.Serializator import TagsSerializer
from tags.models import Tag


class Tags(ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagsSerializer

    def get_queryset(self, *args, **kwargs):
        token = self.request.session.get('name')
        if token is None:
            raise ValidationError({'error': 'You not logged in'})
        username = UserToken.objects.filter(key=token).first().user
        project = Project.objects.filter(name=self.kwargs['projectname'], user__username=self.kwargs.get('username'))
        if not project.exists():
            raise ValidationError({'error': 'Project does not exist'})
        if self.kwargs.get('username') != username.username:
            if not project.filter(visible=True).exists():
                raise ValidationError([])
        return self.queryset.filter(Q(project=project.first()) | Q(project=None))

    @is_not_token_valid
    @is_logged_in
    def create(self, request, *args, **kwargs):
        post_data = request.POST
        username = UserToken.objects.filter(key=self.request.session.get('name')).first().user
        project = Project.objects.filter(name=self.kwargs['projectname'], user=username)
        if not project.exists():
            raise ValidationError({'error': 'Project not found'})
        serialize = self.get_serializer(data={'tag': post_data.get('tag'), 'project': project.first().id})
        serialize.is_valid(raise_exception=True)
        serialize.save()
        return Response({'response': serialize.instance.tag})


class TagsWithBugs(ViewSet):
    def get_report(self, name, token, self_report=False):
        username = UserToken.objects.filter(key=token).first().user
        report = Report.objects.filter(id=name)
        if self_report:
            report = report.filter(user=username)
        else:
            user = self.kwargs['username']
            report = report.filter(user__username=user)
        if not report.exists():
            raise ValidationError({'error': 'Report not found'})
        return report

    @is_not_token_valid
    @is_logged_in
    def create(self, request, *args, **kwargs):
        token = self.request.session.get('name')
        report = self.get_report(name=self.kwargs['bug'], token=token, self_report=True)
        tag = request.POST.get('tag')
        if tag is None:
            raise ValidationError({'error': 'tag not specified'})
        if not report.first().tags.filter(id=tag).exists():
            raise ValidationError({'error': 'This tag does not exist'})
        report.first().tags.add(tag)
        return Response({'response': 'Tag successfully pinned to this report'})

    def list(self, request, *args, **kwargs):
        token = self.request.session.get('name')
        report = self.get_report(name=self.kwargs['bug'], token=token, self_report=False)
        return Response({'response': report.first().tags.values_list('tag')})

    @is_logged_in
    def destroy(self, request, *args, **kwargs):
        tag_id = self.kwargs['id']
        token = self.request.session.get('name')
        report = self.get_report(name=self.kwargs['bug'], token=token, self_report=True)
        report.first().tags.remove(tag_id)
        return Response({'response': 'successful delete.'})