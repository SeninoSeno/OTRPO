from django.shortcuts import render
import requests


def index(request):
    url = "https://pokeapi.co/api/v2/pokemon"
    count = requests.get(f'{url}').json()['count']
    pokemons = requests.get(f'{url}?limit={count}&offset=0').json()['results']

    context = {
        'pokemons': pokemons,
    }

    return render(request, 'index.html', context)
