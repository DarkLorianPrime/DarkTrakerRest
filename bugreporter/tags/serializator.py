from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer

from tags.models import Tag


class TagsSerializer(ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'

    def validate(self, data):
        tag = Tag.objects.filter(tag=data.get('tag'), project=data.get('project'))
        if tag.exists():
            raise ValidationError({'error': f'This tag already exists. His id is: {tag.first().id}'})
        return data