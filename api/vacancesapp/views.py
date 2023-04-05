from django.shortcuts import render

from .serializers import *
from .models import *

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response


class PokemonViewSet(viewsets.ModelViewSet):
    queryset = Pokemon.objects.all()
    serializer_class = ComplexPokemonSerializer
    
    @action(detail=False, methods=['get'])
    def unowned_by_user(self, request): 
        # user = request.user TODO Use this when auth is implemented
        user = User.objects.get(username="admin") # TODO TMP LOCAL @Jonas : admin (1 pokemon got), samy (3 pokemon got), MPolo (0 pokemon got)
        
        # aaa__bbb__ccc means : aaa with relation (double _) to bbb with relation to ccc
        queryset = Pokemon.objects.exclude(owned_pokemons__player__user=user)
        serializer = ComplexPokemonSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)

class PokemonTypeViewSet(viewsets.ModelViewSet):
    queryset = PokemonType.objects.all()
    serializer_class = PokemonTypeSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
class PlayerViewSet(viewsets.ModelViewSet):
    queryset = Player.objects.all()
    serializer_class = ComplexPlayerSerializer
    
class OwnedPokemonViewSet(viewsets.ModelViewSet):
    queryset = OwnedPokemon.objects.all()
    serializer_class = ComplexOwnedPokemonSerializer
