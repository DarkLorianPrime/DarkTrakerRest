from django.contrib.auth.models import User
from rest_framework import fields, serializers
from rest_framework.serializers import ModelSerializer


def check_email(email):
    if User.objects.filter(email=email).exists():
        raise serializers.ValidationError({'error': 'This email already exists.'})


class RegistrationSerializer(ModelSerializer):
    email = fields.EmailField(validators=[check_email])

    class Meta:
        fields = ['username', 'password', 'email']
        model = User

    def create(self, validated_data):
        return User.objects.create_user(username=validated_data['username'],
                                        password=validated_data['password'],
                                        email=validated_data['email'])