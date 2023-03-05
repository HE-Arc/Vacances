from unittest.util import _MAX_LENGTH
from rest_framework import serializers
from .models import *

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = [
            "url",
            "id",
            "username",
        ]
        

class PlayerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Player
        fields = [
            "url",
            "id",
            "user",
            "username",
            "is_manager",
            "money",
        ]
        
    
class PokemonTypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = PokemonType
        fields = [
            "url",
            "id",
            "name",
            "max_happiness",
            "cost",
            "cash_factor",
        ]

class PokemonSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Pokemon
        fields = [
            "url",
            "id",
            "pokemon_type",
            "name",
            "obtainable",
        ]
        
        
class AreaSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Pokemon
        fields = [
            "url",
            "id",
            "name",
            "size",
        ]
        
        
class OwnedPokemonSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Pokemon
        fields = [
            "url",
            "id",
            "pokemon",
            "player",
            "current_area",
            "requested_area",
            "current_happiness",
        ]


class ComplexPokemonSerializer(PokemonSerializer):
    pokemon_type_object = PokemonTypeSerializer(source="pokemon_type", read_only=True)
    class Meta:
        model = Pokemon
        fields = PokemonSerializer.Meta.fields + [
            "pokemon_type_object",
        ]
