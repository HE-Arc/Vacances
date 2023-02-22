from django.db import models

from django.contrib.auth.models import User

class PokemonType(models.Model):
    name = models.CharField(max_length=100)
    max_happiness = models.PositiveIntegerField()
    cost = models.PositiveIntegerField()
    cash_factor = models.FloatField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

class Pokemon(models.Model):
    pokemon_type = models.ForeignKey(PokemonType, related_name="pokemons", on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    obtainable = models.BooleanField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

class Area(models.Model):
    name = models.CharField(max_length=100)
    size = models.PositiveIntegerField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

class OwnedPokemon(models.Model):
    pokemon = models.ForeignKey(Pokemon, null=True, related_name="owned_pokemons", on_delete=models.SET_NULL)
    user = models.ForeignKey(User, related_name="owned_pokemons", on_delete=models.CASCADE)
    current_area = models.ForeignKey(Area, null=True, related_name="owned_pokemons_current", on_delete=models.SET_NULL)
    requested_area = models.ForeignKey(Area, null=True, related_name="owned_pokemons_requested", on_delete=models.SET_NULL)
    current_happiness = models.PositiveIntegerField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)