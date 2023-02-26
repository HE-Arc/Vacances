from django.shortcuts import render

from .serializers import PokemonSerializer
from .models import Pokemon

from rest_framework import viewsets

# Create your views here.

class PokemonViewSet(viewsets.ModelViewSet):
    queryset = Pokemon.objects.all()
    serializer_class = PokemonSerializer
