"""
Book: Building RESTful Python Web Services
Chapter 4: Throttling, Filtering, Testing and Deploying an API with Django
Author: Gaston C. Hillar - Twitter.com/gastonhillar
Publisher: Packt Publishing Ltd. - http://www.packtpub.com
"""
from games.models import GameCategory
from games.models import Game
from games.models import Player
from games.models import PlayerScore
from games.serializers import GameCategorySerializer
from games.serializers import GameSerializer
from games.serializers import PlayerSerializer
from games.serializers import PlayerScoreSerializer
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.reverse import reverse
from django.contrib.auth.models import User
from games.serializers import UserSerializer
from rest_framework import permissions
from games.permissions import IsOwnerOrReadOnly
from rest_framework.throttling import ScopedRateThrottle
from rest_framework import generics
from django_filters import rest_framework as filters


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    name = 'user-list'


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    name = 'user-detail'


class GameCategoryList(generics.ListCreateAPIView):
    queryset = GameCategory.objects.all()
    serializer_class = GameCategorySerializer
    name = 'gamecategory-list'
    throttle_scope = 'game-categories'
    throttle_classes = (ScopedRateThrottle,)
    filterset_fields = ('name',)
    search_fields = ('^name',)
    ordering_fields = ('name',)


class GameCategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = GameCategory.objects.all()
    serializer_class = GameCategorySerializer
    name = 'gamecategory-detail'
    throttle_scope = 'game-categories'
    throttle_classes = (ScopedRateThrottle,)


class GameList(generics.ListCreateAPIView):
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    name = 'game-list'
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly,
        )
    filterset_fields = (
        'name',
        'game_category',
        'release_date',
        'played',
        'owner',
        )
    search_fields = (
        '^name',
        )
    ordering_fields = (
        'name',
        'release_date',
        )

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class GameDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    name = 'game-detail'
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly)


class PlayerList(generics.ListCreateAPIView):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
    name = 'player-list'
    filterset_fields = (
        'name',
        'gender',
        )
    search_fields = (
        '^name',
        )
    ordering_fields = (
        'name',
        )


class PlayerDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
    name = 'player-detail'


class PlayerScoreFilter(filters.FilterSet):
    #https://stackoverflow.com/questions/51850985/django-filter-typeerror-at-goods-init-got-an-unexpected-keyword-argumen
    #https://django-filter.readthedocs.io/en/latest/guide/rest_framework.html
    # Download Bootstrap3 and put it in the django templates in this location C:\Users\ellis\PythonREST\Django01\Lib\site-packages\django\contrib\admin\templates\bootstrap3\
    min_score = filters.NumberFilter(
        field_name='score', lookup_expr='gte')
    max_score = filters.NumberFilter(
        field_name='score', lookup_expr='lte')
    from_score_date = filters.DateTimeFilter(
        field_name='score_date', lookup_expr='gte')
    to_score_date = filters.DateTimeFilter(
        field_name='score_date', lookup_expr='lte')
    player_name = filters.AllValuesFilter(
        field_name='player__name')
    game_name = filters.AllValuesFilter(
        field_name='game__name')

    class Meta:
        model = PlayerScore
        fields = (
            'score',
            'from_score_date',
            'to_score_date',
            'min_score',
            'max_score',
            # player__name will be accessed as player_name
            'player_name',
            # game__name will be accessed as game_name
            'game_name',
        )


class PlayerScoreList(generics.ListAPIView):
    queryset = PlayerScore.objects.all()
    serializer_class = PlayerScoreSerializer
    name = 'playerscore-list'
    filterset_class = PlayerScoreFilter
    ordering_fields = (
        'score',
        'score_date',
        )


class PlayerScoreDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = PlayerScore.objects.all()
    serializer_class = PlayerScoreSerializer
    name = 'playerscore-detail'


class ApiRoot(generics.GenericAPIView):
    name = 'api-root'
    def get(self, request, *args, **kwargs):
        return Response({
            'players': reverse(PlayerList.name, request=request),
            'game-categories': reverse(GameCategoryList.name, request=request),
            'games': reverse(GameList.name, request=request),
            'scores': reverse(PlayerScoreList.name, request=request),
            'users': reverse(UserList.name, request=request),
            })
