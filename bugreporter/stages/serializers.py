from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer

from stages.models import WorkStages


class StagesSerializer(ModelSerializer):
    class Meta:
        model = WorkStages
        fields = '__all__'

    def validate(self, data):
        if WorkStages.objects.filter(stage=data.get('stage'), project=data.get('project')).exists():
            raise ValidationError({'error': 'This stage already exists.'})
        return data
