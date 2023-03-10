# Generated by Django 4.1.7 on 2023-02-22 12:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Area',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('size', models.PositiveIntegerField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='PokemonType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('max_happiness', models.PositiveIntegerField()),
                ('cost', models.PositiveIntegerField()),
                ('cash_factor', models.FloatField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Pokemon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('obtainable', models.BooleanField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('pokemon_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pokemons', to='vacancesapp.pokemontype')),
            ],
        ),
        migrations.CreateModel(
            name='OwnedPokemon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('current_happiness', models.PositiveIntegerField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('current_area', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='owned_pokemons_current', to='vacancesapp.area')),
                ('pokemon', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='owned_pokemons', to='vacancesapp.pokemon')),
                ('requested_area', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='owned_pokemons_requested', to='vacancesapp.area')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='owned_pokemons', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
