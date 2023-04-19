from unittest.util import _MAX_LENGTH
from rest_framework import serializers
from .models import *
from .utils import *

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
            "image_url",
        ]
        
        
class AreaSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Area
        fields = [
            "url",
            "id",
            "name",
            "size",
        ]
        
        
class OwnedPokemonSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = OwnedPokemon
        fields = [
            "url",
            "id",
            "pokemon",
            "player",
            # "current_area", # TODO : uncomment when area is done
            # "requested_area", # TODO : uncomment when area is done
            "current_happiness",
        ]

class ComplexPokemonSerializer(PokemonSerializer):
    pokemon_type_object = PokemonTypeSerializer(source="pokemon_type", read_only=True)
    owned_pokemon_object = OwnedPokemonSerializer(source="owned_pokemon", read_only=True)
    class Meta:
        model = Pokemon
        fields = PokemonSerializer.Meta.fields + [
            "pokemon_type_object",
            "owned_pokemon_object",
        ]
        
class ComplexPokemonOfPlayerSerializer(ComplexPokemonSerializer):
    is_owned = serializers.SerializerMethodField()
    class Meta:
        model = Pokemon
        fields = ComplexPokemonSerializer.Meta.fields + [
            "is_owned"
        ]
        
    def get_is_owned(self, obj):
        # Default value of "is_owned"
        user = User.objects.get(username=get_current_username(self.context["request"]))
        return obj.owned_pokemons.filter(player__user=user).exists()

class ComplexPlayerSerializer(PlayerSerializer):
    user_object = UserSerializer(source="user", read_only=True)
    class Meta:
        model = Player
        fields = PlayerSerializer.Meta.fields + [
            "user_object",
        ]
        
class ComplexOwnedPokemonSerializer(PlayerSerializer):
    # TODO : Uncomment "current_area_object" and "requested_area_object" when area is done (4 lines below)
    
    player_object = PlayerSerializer(source="player", read_only=True)
    # current_area_object = AreaSerializer(source="current_area", read_only=True)
    # requested_area_object = AreaSerializer(source="requested_ared", read_only=True)
    class Meta:
        model = OwnedPokemon
        fields = OwnedPokemonSerializer.Meta.fields + [
            "player_object",
            # "current_area_object",
            # "requested_area_object",
        ]