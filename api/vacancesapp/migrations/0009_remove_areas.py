# Generated by Django 4.1.7 on 2023-04-28 17:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("vacancesapp", "0008_alter_ownedpokemon_pokemon"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="ownedpokemon",
            name="current_area",
        ),
        migrations.RemoveField(
            model_name="ownedpokemon",
            name="requested_area",
        ),
        migrations.DeleteModel(
            name="Area",
        ),
    ]
