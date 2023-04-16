from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import *
from .models import *
from rest_framework import status


from rest_framework import viewsets


class PokemonViewSet(viewsets.ModelViewSet):
    queryset = Pokemon.objects.all()
    serializer_class = ComplexPokemonSerializer
    
    #authentication_classes = [SessionAuthentication]
    #permission_classes = [IsAuthenticated]
    

class PokemonTypeViewSet(viewsets.ModelViewSet):
    queryset = PokemonType.objects.all()
    serializer_class = PokemonTypeSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    def get_queryset(self):
        queryset = User.objects.all()
        login_page = self.request.query_params.get('loginPage')
        if login_page: # if on login page
            username = self.request.query_params.get('username')
            password = self.request.query_params.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(self.request, user)
                return [user]
            
            return None
            
        else: # if api call
            return queryset
    
    def create(self, request):
        values = request.data
        user = User(username=values['username'])
        
        # set password and hash it
        user.set_password(values['password'])
        
        try:
            user.save()
            serializer = UserSerializer(user, context={'request': request})
            return Response({'data' : serializer.data}, status=status.HTTP_201_CREATED)
        
        except:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PlayerViewSet(viewsets.ModelViewSet):
    queryset = Player.objects.all()
    serializer_class = ComplexPlayerSerializer
    