from rest_framework import fields, serializers
from rest_framework.serializers import ModelSerializer

from projects.models import Project


# def check_email(name):
#     if Project.objects.filter(name=name).exists():
#         raise serializers.ValidationError({'error': 'This email already exists.'})


class CreateProjectSerializer(ModelSerializer):
    class Meta:
        fields = ['id', 'name', 'user']
        model = Project

    def validate(self, data):
        print(1)
        if data.get('name') is not None:
            if Project.objects.filter(name=data.get('name'), user=data.get('user')).exists():
                raise serializers.ValidationError({'error': 'This projects already exists.'})
            return data
