from django.shortcuts import render

from .serializers import *
from .models import *

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

current_username = "samy" # TODO TMP LOCAL @Jonas : admin (1 pokemon got), samy (3 pokemon got), MPolo (0 pokemon got)

class PokemonViewSet(viewsets.ModelViewSet):
    queryset = Pokemon.objects.all()
    serializer_class = ComplexPokemonSerializer
    
    @action(detail=False, methods=['get'])
    def unowned_by_user(self, request): 
        # user = request.user TODO Use this when auth is implemented
        user = User.objects.get(username=current_username)
        
        # aaa__bbb__ccc means : aaa with relation (double _) to bbb with relation to ccc
        queryset = Pokemon.objects.exclude(owned_pokemons__player__user=user)
        serializer = ComplexPokemonSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def pokemon_of_player(self, request): 
        queryset = Pokemon.objects.all()
        serializer = ComplexPokemonOfPlayerSerializer(queryset, many=True, context={'request': request})

        return Response(serializer.data)
    
    @action(detail=True, methods=['post']) # detail=True means that the id of the pokemon is passed in the url
    def buy(self, request, pk=None):
        # user = request.user TODO Use this when auth is implemented
        user = User.objects.get(username=current_username)
        pokemon = self.get_object()
        pokemonType = PokemonType.objects.get(id=pokemon.pokemon_type.id)
        
        print("buying pokemon " + str(pokemon) + " for " + str(pokemonType.cost))
        
        # TODO Transaction ?
        paid = PlayerViewSet.reduce_money(self, request, pokemonType.cost)
        print("Payment info :", paid.data, " => ", paid)
        
        if (paid.status_code != 200):
            return Response({"error": paid.data}, status=paid.status_code)
        
        gotPokemon = OwnedPokemonViewSet.create_if_new(self, request, pokemon)
        print("Got pokemon info :", gotPokemon.data, " => ", gotPokemon)
        
        if (gotPokemon.status_code != 200):
            return Response({"error": gotPokemon.data}, status=gotPokemon.status_code)
        
        return Response({"success": True})
        
class PokemonTypeViewSet(viewsets.ModelViewSet):
    queryset = PokemonType.objects.all()
    serializer_class = PokemonTypeSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
class PlayerViewSet(viewsets.ModelViewSet):
    queryset = Player.objects.all()
    serializer_class = ComplexPlayerSerializer

    @action(detail=False, methods=['get'])
    def my_data(self, request):
        # user = request.user TODO Use this when auth is implemented
        user = User.objects.get(username=current_username)
        
        queryset = Player.objects.filter(user=user)
        serializer = ComplexPlayerSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data[0])
    
    @action(detail=False, methods=['post'])
    def reduce_money(self, request, qty=0):
        # user = request.user TODO Use this when auth is implemented
        user = User.objects.get(username=current_username)
        
        player = Player.objects.get(user=user)
        
        if player.money < qty:
            return Response("Error : not enough money", status=status.HTTP_402_PAYMENT_REQUIRED)
        
        player.money -= qty
        player.save()
        
        serializer = ComplexPlayerSerializer(player, context={'request': request})
        return Response(serializer.data)
        
    
class OwnedPokemonViewSet(viewsets.ModelViewSet):
    queryset = OwnedPokemon.objects.all()
    serializer_class = ComplexOwnedPokemonSerializer
    
    @action(detail=False, methods=['post'])
    def create_if_new(self, request, pokemon):
        # user = request.user TODO Use this when auth is implemented
        user = User.objects.get(username=current_username)
        
        player = Player.objects.get(user=user)
        
        if OwnedPokemon.objects.filter(player=player, pokemon=pokemon).exists():
            return Response("Error : pokemon already owned", status=status.HTTP_409_CONFLICT)
        
        # Create new entry
        owned_pokemon = OwnedPokemon()
        owned_pokemon.player = player
        owned_pokemon.pokemon = pokemon
        owned_pokemon.current_area = Area.objects.first() # TODO : get the default area (the one without limit)
        owned_pokemon.requested_area = Area.objects.first() # TODO : get the default area (the one without limit)
        owned_pokemon.current_happiness = 0
        
        owned_pokemon.save()
        
        serializer = ComplexOwnedPokemonSerializer(owned_pokemon, context={'request': request})
        return Response(serializer.data)
        
        
        
