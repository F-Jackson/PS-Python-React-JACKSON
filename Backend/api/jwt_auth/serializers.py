from rest_framework import serializers


class SToken(serializers.Serializer):
    token = serializers.CharField()
    