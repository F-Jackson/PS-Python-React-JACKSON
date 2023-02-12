from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics
from django.http import Http404

from games.constants import GAMES_LIST_RECEIVE_LENGTH
from games.models import GamesModel
from games.serializers import GamesSerializer


class GameListView(generics.ListAPIView):
    serializer_class = GamesSerializer
    model = GamesModel
    paginate_by = GAMES_LIST_RECEIVE_LENGTH
    
    def get_queryset(self):
        queryset = self.model.objects.all()
        return queryset


class GameSingleView(generics.RetrieveAPIView):
    serializer_class = GamesSerializer
    queryset = GamesModel.objects.all()
    lookup_field = 'pk'

