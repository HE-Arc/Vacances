from django.shortcuts import render

from .serializers import *
from .models import *

from rest_framework import viewsets


class PokemonViewSet(viewsets.ModelViewSet):
    queryset = Pokemon.objects.all()
    serializer_class = ComplexPokemonSerializer

class PokemonTypeViewSet(viewsets.ModelViewSet):
    queryset = PokemonType.objects.all()
    serializer_class = PokemonTypeSerializer

class UserTypeViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer