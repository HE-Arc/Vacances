from django.db import models

from django.contrib.auth.models import User

class Player(models.Model):
    user = models.ForeignKey(User, related_name="players", on_delete=models.CASCADE)
    username = models.CharField(max_length=150, unique=True)
    is_manager = models.BooleanField()
    money = models.PositiveIntegerField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def create_for(user: User):
        Player.objects.create(user=user, username=user.username, is_manager=False, money=50)
        
    def reduce_money(self, amount):
        if self.money < amount:
            raise Exception("Not enough money")
        
        self.money -= amount
        self.save()

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

class OwnedPokemon(models.Model):
    pokemon = models.ForeignKey(Pokemon, null=True, related_name="owned_pokemons", on_delete=models.CASCADE)
    player = models.ForeignKey(Player, related_name="owned_pokemons", on_delete=models.CASCADE)
    current_happiness = models.PositiveIntegerField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def create_if_new(pokemon : Pokemon, player : Player):
        if not OwnedPokemon.objects.filter(pokemon=pokemon, player=player).exists():
            OwnedPokemon.objects.create(pokemon=pokemon, player=player, current_happiness=0)
        else:
            raise Exception("Pokemon already owned")