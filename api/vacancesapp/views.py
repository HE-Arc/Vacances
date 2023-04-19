from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from rest_framework.decorators import action
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import *
from .models import *
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import viewsets


class PokemonViewSet(viewsets.ModelViewSet):
    queryset = Pokemon.objects.all()
    serializer_class = ComplexPokemonSerializer
    
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]
    

class PokemonTypeViewSet(viewsets.ModelViewSet):
    queryset = PokemonType.objects.all()
    serializer_class = PokemonTypeSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    
    #@action(detail=True, methods=["POST"], url_path="login")
    #def login(self, request, pk):
    #    print("Hello")
    #    print(request.data)
    #
    #    queryset = User.objects.all()
    #    
    #    return queryset
        #login_page = self.request.query_params.get('loginPage')
    #    username = self.request.query_params.get('username')
    #    password = self.request.query_params.get('password')
    #    user = authenticate(username=username, password=password)
    #    if user is not None:
    #        login(self.request, user)
    #        return [user]
    #    
    #    return None
    
    
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


class LoginView(APIView):
    def post(self, request):
        data = request.data
        username = data.get('username')
        password = data.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            serializer = UserSerializer(user, context={'request': request})
            return Response({'success': 'Login successful'})

        return Response({'error': 'error'})


class PlayerViewSet(viewsets.ModelViewSet):
    queryset = Player.objects.all()
    serializer_class = ComplexPlayerSerializer
    