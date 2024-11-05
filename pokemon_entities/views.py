import folium
import json

from django.http import HttpResponseNotFound
from django.shortcuts import render
from django.utils.timezone import localtime, now
from .models import Pokemon, PokemonEntity


MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = (
    'https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision'
    '/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832'
    '&fill=transparent'
)


def add_pokemon(folium_map, lat, lon, image_url=DEFAULT_IMAGE_URL):
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [lat, lon],
        # Warning! `tooltip` attribute is disabled intentionally
        # to fix strange folium cyrillic encoding bug
        icon=icon,
    ).add_to(folium_map)


def show_all_pokemons(request):
    # with open('pokemon_entities/pokemons.json', encoding='utf-8') as database:
    #     pokemons = json.load(database)['pokemons']

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    time_now = localtime(now())
    pokemon_enties = PokemonEntity.objects.filter(appeared_at__lte=time_now, disappeared_at__gte=time_now)

    for entity in pokemon_enties:
        photo = ''
        if entity.pokemon.photo:
            photo = entity.pokemon.photo.url
        add_pokemon(
            folium_map, entity.lat,
            entity.lon,
            request.build_absolute_uri(photo)  # возвращает полную ссылку
        )

    pokemons_on_page = []
    pokemons = Pokemon.objects.all()
    for pokemon in pokemons:
        photo = ''
        if pokemon.photo:
            photo = pokemon.photo.url
        pokemons_on_page.append({
            'pokemon_id': pokemon.id,
            'img_url': photo,
            'title_ru': pokemon.title,
        })

    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    pokemons = Pokemon.objects.filter(id=pokemon_id)
    for pokemon in pokemons:
        if pokemon.id == int(pokemon_id):
            requested_pokemon = pokemon
            break
    else:
        return HttpResponseNotFound('<h1>Такой покемон не найден</h1>')

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)

    pokemon_enties = PokemonEntity.objects.filter(pokemon=requested_pokemon)
    for entity in pokemon_enties:
        photo = ''
        if entity.pokemon.photo:
            photo = entity.pokemon.photo.url
        add_pokemon(
            folium_map, entity.lat,
            entity.lon,
            request.build_absolute_uri(photo)
        )

    previous_evolution = {}
    previous_pokemon = pokemon.previous_evolution
    if previous_pokemon:

        previous_pokemon_photo = ''
        if previous_pokemon.photo:
            previous_pokemon_photo = previous_pokemon.photo.url

        previous_evolution = {
            'img_url': previous_pokemon_photo,
            'title_ru': previous_pokemon.title,
            'pokemon_id': previous_pokemon.id,
        }

    pokemon_parameters = {  # переназвать переменную
        'img_url': photo,
        'title_ru': pokemon.title,
        'title_en': pokemon.title_en,
        'title_jp': pokemon.title_jp,
        'description': pokemon.description,
        'previous_evolution': previous_evolution
    }

    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(), 'pokemon': pokemon_parameters
    })
