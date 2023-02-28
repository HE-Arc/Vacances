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
                views.UserTypeViewSet,
                basename="user")

urlpatterns = [
    path("", include(router.urls))
]