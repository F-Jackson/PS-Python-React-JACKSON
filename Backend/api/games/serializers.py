from rest_framework import serializers

from games.models import GamesModel


class GamesSerializer(serializers.ModelSerializer):
    class Meta:
        model = GamesModel
        fields = '__all__'
