from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.db.models import F
from rest_framework.decorators import action
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import *
from .models import *
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404

class PokemonViewSet(viewsets.ModelViewSet):
    """Registred pokemons in the app (the pokedex)"""
    queryset = Pokemon.objects.all()
    serializer_class = ComplexPokemonSerializer
    
    #authentication_classes = [SessionAuthentication]
    #permission_classes = [IsAuthenticated]
    
    @action(detail=False, methods=['get'])
    def unowned_by_user(self, request):
        """
        Get all pokemons that are not owned by the connected user
        It's a shortcut to "pokemon_of_player", to avoid filter "is_owned == False" on the front side
        """
        connectedUserResponse = UserViewSet.current(self, request)
        if connectedUserResponse.status_code != status.HTTP_200_OK:
            return connectedUserResponse
        
        user = connectedUserResponse.data.get("id")
        
        # aaa__bbb__ccc means : aaa with relation (double _) to bbb with relation to ccc
        queryset = Pokemon.objects.exclude(owned_pokemons__player__user=user)
        serializer = ComplexPokemonSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def pokemons_of_user(self, request):
        """
        Get all pokemons in the app with an indication if it is owned by the connected user
        """
        queryset = Pokemon.objects.all()
        serializer = ComplexPokemonOfPlayerSerializer(queryset, many=True, context={'request': request})

        return Response(serializer.data)
    
    @action(detail=True, methods=['post']) # detail=True means that the id of the pokemon is passed in the url
    def buy(self, request, pk=None):
        """
        Perform the purchase of a pokemon by the connected user
        It will reduce the money of the user and add the pokemon to his list of owned pokemons
        """ 
        pokemon = get_object_or_404(Pokemon, pk = pk)
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
    
    @action(detail=True, methods=["DELETE"], url_path="delete-with-refund")
    def delete_with_refound(self, request, pk):
        itemToDelete = get_object_or_404(Pokemon, pk = pk)
        
        players = Player.objects.filter(owned_pokemons__pokemon=itemToDelete)
        refund = itemToDelete.pokemon_type.cost
        
        # TODO Transaction ?
        players.update(money=F('money') + refund)
        itemToDelete.delete()
        
        return Response(status=status.HTTP_204_NO_CONTENT)
        
class PokemonTypeViewSet(viewsets.ModelViewSet):
    queryset = PokemonType.objects.all()
    serializer_class = PokemonTypeSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    def create(self, request):
        values = request.data
        user = User(username=values['username'])
        
        # set password and hash it
        user.set_password(values['password'])
        
        serializer = None
        try:
            # TODO Transaction ?
            user.save()
            
            # add the profile of the user (player instance)
            player = Player(user=user)
            player.username = user.username
            player.is_manager = False
            player.money = 50
            
            player.save()
            
            serializer = UserSerializer(user, context={'request': request})
            return Response({'user' : serializer.data}, status=status.HTTP_201_CREATED)
        
        except:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    @action(detail=False, methods=['post'])
    def login(self, request):
        data = request.data
        username = data.get('username')
        password = data.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            print(user)
            login(request, user)
            return Response({'success': 'Login successful'}, status=status.HTTP_200_OK)

        return Response({'error': 'error'}, status=status.HTTP_401_UNAUTHORIZED)
    
    @action(detail=False, methods=['get'])
    def current(self, request):        
        if request.user.is_authenticated:
            serializer = UserSerializer(request.user, context={'request': request})
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

    @action(detail=False, methods=['get'])
    def logout(self, request):
        logout(request)
        return Response(status=status.HTTP_200_OK)
    

class PlayerViewSet(viewsets.ModelViewSet):
    queryset = Player.objects.all()
    serializer_class = ComplexPlayerSerializer

    @action(detail=False, methods=['get'])
    def my_data(self, request):
        connectedUserResponse = UserViewSet.current(self, request)
        if connectedUserResponse.status_code != status.HTTP_200_OK:
            return connectedUserResponse
        
        user = connectedUserResponse.data.get("id")
        
        queryset = Player.objects.filter(user=user)
        serializer = ComplexPlayerSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data[0])
    
    @action(detail=False, methods=['post'])
    def reduce_money(self, request, qty=0):
        connectedUserResponse = UserViewSet.current(self, request)
        if connectedUserResponse.status_code != status.HTTP_200_OK:
            return connectedUserResponse
        
        user = connectedUserResponse.data.get("id")
        
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
        connectedUserResponse = UserViewSet.current(self, request)
        if connectedUserResponse.status_code != status.HTTP_200_OK:
            return connectedUserResponse
        
        user = connectedUserResponse.data.get("id")
        
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
    
    @action(detail=False, methods=['get'])
    def my_pokemons(self, request):
        connectedUserResponse = UserViewSet.current(self, request)
        if connectedUserResponse.status_code != status.HTTP_200_OK:
            return connectedUserResponse
        
        user = connectedUserResponse.data.get("id")
        
        player = Player.objects.get(user=user)
        
        queryset = OwnedPokemon.objects.filter(player=player)
        serializer = ComplexOwnedPokemonSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)
        
class AreaViewSet(viewsets.ModelViewSet):
    queryset = Area.objects.all()
    serializer_class = AreaSerializer
        
