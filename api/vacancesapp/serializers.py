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
            "password",
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
    display_image_url = serializers.SerializerMethodField()
    class Meta:
        model = Pokemon
        fields = [
            "url",
            "id",
            "pokemon_type",
            "name",
            "obtainable",
            "image_url",
            "display_image_url"
        ]
        
    read_only_fields = ['url', 'id']
    extra_kwargs = {
        'pokemon_type': {'required': True},
        'name': {'required': True},
    }
        
    def get_display_image_url(self, obj):
        if not obj.image_url:
            return "https://www.pokepedia.fr/images/5/54/Sprite_MissingNo._RV.png"
        return obj.image_url
        
        
class AreaSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Area
        fields = [
            "url",
            "id",
            "name",
            "image",
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
        if (not self.context["request"].user.is_authenticated):
            return False
        user = User.objects.get(username=self.context["request"].user)
        return obj.owned_pokemons.filter(player__user=user).exists()

class ComplexPlayerSerializer(PlayerSerializer):
    user_object = UserSerializer(source="user", read_only=True)
    class Meta:
        model = Player
        fields = PlayerSerializer.Meta.fields + [
            "user_object",
        ]
        
class ComplexOwnedPokemonSerializer(PlayerSerializer):    
    pokemon_object = ComplexPokemonSerializer(source="pokemon", read_only=True)
    player_object = PlayerSerializer(source="player", read_only=True)
    #pokemon_type_object = PokemonTypeSerializer(source="pokemon__pokemon_type", read_only=True)
    class Meta:
        model = OwnedPokemon
        fields = OwnedPokemonSerializer.Meta.fields + [
            "pokemon_object",
            "player_object",
            #"pokemon_type_object",
        ]