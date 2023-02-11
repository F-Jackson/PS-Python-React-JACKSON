from django.contrib.auth.models import User
from rest_framework import serializers

from jwt_auth.serializers import SToken


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']


class SUser(serializers.Serializer):
    token = SToken()
    user = UserSerializer()
