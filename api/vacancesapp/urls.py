from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register("pokemons",
                views.PokemonViewSet,
                basename="pokemon")


router.register("pokemon-types",
                views.PokemonTypeViewSet,
                basename="pokemontype")


router.register("users",
                views.UserViewSet,
                basename="user")

router.register("players",
                views.PlayerViewSet,
                basename="player")

urlpatterns = [
    path("", include(router.urls)),
    path("accounts/", include("django.contrib.auth.urls")),
]