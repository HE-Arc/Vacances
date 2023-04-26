from django.db import models

from django.contrib.auth.models import User

class Player(models.Model):
    user = models.ForeignKey(User, related_name="players", on_delete=models.CASCADE)
    username = models.CharField(max_length=150, unique=True)
    is_manager = models.BooleanField()
    money = models.PositiveIntegerField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

class PokemonType(models.Model):
    name = models.CharField(max_length=100)
    max_happiness = models.PositiveIntegerField()
    cost = models.PositiveIntegerField()
    cash_factor = models.FloatField()

class Pokemon(models.Model):
    pokemon_type = models.ForeignKey(PokemonType, related_name="pokemons", on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    obtainable = models.BooleanField()
    image_url = models.URLField(null=True, blank=True)

class Area(models.Model):
    name = models.CharField(max_length=100)
    image = models.CharField(max_length=200, default=None)

class OwnedPokemon(models.Model):
    pokemon = models.ForeignKey(Pokemon, null=True, related_name="owned_pokemons", on_delete=models.SET_NULL)
    player = models.ForeignKey(Player, related_name="owned_pokemons", on_delete=models.CASCADE)
    current_area = models.ForeignKey(Area, null=True, related_name="owned_pokemons_current", on_delete=models.SET_NULL)
    requested_area = models.ForeignKey(Area, null=True, related_name="owned_pokemons_requested", on_delete=models.SET_NULL)
    current_happiness = models.PositiveIntegerField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)