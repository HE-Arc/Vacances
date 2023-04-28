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
from rest_framework.decorators import action, api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404

class PokemonViewSet(viewsets.ModelViewSet):
    """Registred pokemons in the app (the pokedex)"""
    queryset = Pokemon.objects.all()
    serializer_class = ComplexPokemonSerializer
        
    # Note : the @auth & @perm doesn't seem to work, so we check if user is authenticated in the method
    # @authentication_classes([SessionAuthentication])
    # @permission_classes([IsAuthenticated])
    @action(detail=False, methods=['get'], url_path="unowned-by-user")
    def unowned_by_user(self, request):
        """
        Get all pokemons that are not owned by the connected user
        It's a shortcut to "pokemon_of_player", to avoid filter "is_owned == False" on the front side
        """
        user = request.user
        if not user.is_authenticated:
            return Response({"error": "You must be logged to get your unowned pokemons"}, status=status.HTTP_401_UNAUTHORIZED)
        
        # aaa__bbb__ccc means : aaa with relation (double _) to bbb with relation to ccc
        queryset = Pokemon.objects.exclude(owned_pokemons__player__user=user)
        serializer = ComplexPokemonSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], url_path="is-owned-by-user")
    def with_is_owned_by_user(self, request):
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
        user = request.user
        if not user.is_authenticated:
            return Response({"error": "You must be logged to buy a pokemon"}, status=status.HTTP_401_UNAUTHORIZED)
        
        pokemon = get_object_or_404(Pokemon, pk = pk)
        pokemonType = PokemonType.objects.get(id=pokemon.pokemon_type.id)

        player = Player.objects.get(user=user)
        
        # TODO Transaction ?
        try:
            OwnedPokemon.create_if_new(pokemon, player)
        except:
            return Response({"error": "Pokemon already owned"}, status=status.HTTP_409_CONFLICT)
        
        try:
            player.reduce_money(pokemonType.cost)
        except:
            return Response({"error": "Not enough money"}, status=status.HTTP_402_PAYMENT_REQUIRED)
        
        return Response({"success": True}, status=status.HTTP_200_OK)
    
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
            Player.create_for(user)
            
            login(request, user)
            
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
            login(request, user)
            print("logged of :", user)
            return Response({'success': 'Login successful'}, status=status.HTTP_200_OK)

        return Response({'error': 'error'}, status=status.HTTP_401_UNAUTHORIZED)

    @action(detail=False, methods=['get'])
    def logout(self, request):
        print("logged out of :", request.user)
        logout(request)
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class PlayerViewSet(viewsets.ModelViewSet):
    queryset = Player.objects.all()
    serializer_class = ComplexPlayerSerializer

    @action(detail=False, methods=['get'], url_path="my-data")
    def my_data(self, request):
        user = request.user
        if not user.is_authenticated:
            return Response({"error": "You must be logged to get your data"}, status=status.HTTP_401_UNAUTHORIZED)
        
        queryset = Player.objects.get(user=user)
        serializer = ComplexPlayerSerializer(queryset, many=False, context={'request': request})
        return Response(serializer.data)
        
    
class OwnedPokemonViewSet(viewsets.ModelViewSet):
    queryset = OwnedPokemon.objects.all()
    serializer_class = ComplexOwnedPokemonSerializer
    
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    
    @action(detail=False, methods=['get'], url_path="my-pokemons")
    def my_pokemons(self, request):
        user = request.user
        queryset = OwnedPokemon.objects.filter(player__user=user)
        serializer = ComplexOwnedPokemonSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'], url_path='increment-happiness')
    def increment_happiness(self, request, pk=None):
        owned_pokemon = get_object_or_404(OwnedPokemon, pk = pk)
        owned_pokemon.current_happiness += 1
        
        pokemon_type = owned_pokemon.pokemon.pokemon_type
        
        # Max happiness reached => reset happiness and give money to the player
        if owned_pokemon.current_happiness >= pokemon_type.max_happiness:
            owned_pokemon.current_happiness = 0
            player=owned_pokemon.player
            player.money += pokemon_type.cash_factor * 10
            
            player.save()
            
        owned_pokemon.save()
        
        serializer = ComplexOwnedPokemonSerializer(owned_pokemon, context={'request': request})
        return Response(serializer.data)
    