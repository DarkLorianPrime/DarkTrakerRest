from django.db.models import Q
from django.shortcuts import render
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ViewSet

from authserver.models import UserToken
from bugs.models import Report
from extras.decorators import is_not_token_valid, is_logged_in
from stages import Serializers
from stages.models import WorkStages
from projects.models import Project


class Stages(ModelViewSet):
    queryset = WorkStages.objects.all()
    serializer_class = Serializers.StagesSerializer

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
        serialize = self.get_serializer(data={'stage': post_data.get('stage'), 'project': project.first().id})
        serialize.is_valid(raise_exception=True)
        serialize.save()
        return Response({'response': serialize.instance.stage})

    @is_logged_in
    def destroys(self, request, *args, **kwargs):
        stage = self.kwargs['id']
        project = Project.objects.filter(name=self.kwargs['projectname'], user__username=self.kwargs['username'])
        if not project.exists():
            raise ValidationError({'error': 'Project not found'})
        stagedelete = WorkStages.objects.filter(project=project.first(), id=stage)
        if not stagedelete.exists():
            raise ValidationError({'error': 'Stage not found in this project'})
        self.perform_destroy(stagedelete.first())
        return Response({'response': 'successful delete.'})


class StagesWithReports(ViewSet):
    @is_not_token_valid
    @is_logged_in
    def update(self, request, *args, **kwargs):
        user = UserToken.objects.filter(key=self.request.session.get('name')).first().user
        project = Project.objects.filter(name=self.kwargs['projectname'], user=user)
        if not project.exists():
            raise ValidationError({'error': 'Project not found in your projects'})
        report = project.first().reports.filter(id=kwargs['bug'])
        if not report.exists():
            raise ValidationError({'error': 'Report not found'})
        stage = request.POST.get('stage')
        if stage is None:
            raise ValidationError({'error': '"stage" not specified.'})
        report.update(stage=request.POST.get('stage'))
        return Response({'response': 'Successful update.'})

    @is_logged_in
    def list(self, request, *args, **kwargs):
        project = Project.objects.filter(name=self.kwargs['projectname'], user__username=self.kwargs['username'])
        if not project.exists():
            raise ValidationError({'error': 'Project not found'})
        report = project.first().reports.filter(id=kwargs['bug'])
        if not report.exists():
            raise ValidationError({'error': 'Report not found'})
        return Response({'response': {'name': report.first().stage.stage, 'id': report.first().stage.id}})