from rest_framework.serializers import ModelSerializer

from bugs.models import Report, Comment


class BugSerializer(ModelSerializer):
    class Meta:
        fields = ['id', 'name', 'text', 'stage', 'user']
        model = Report


class CommentSerializer(ModelSerializer):
    class Meta:
        fields = ['user', 'report', 'text']
        model = Comment