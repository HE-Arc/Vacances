# Generated by Django 4.1.7 on 2023-04-25 17:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vacancesapp', '0006_pokemon_image_url'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='area',
            name='size',
        ),
        migrations.AddField(
            model_name='area',
            name='image',
            field=models.CharField(default=None, max_length=200),
        ),
        migrations.AlterField(
            model_name='pokemon',
            name='image_url',
            field=models.URLField(blank=True, null=True),
        ),
    ]
