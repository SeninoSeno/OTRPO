from django.shortcuts import render
import requests
from django.core.paginator import Paginator


url = "https://pokeapi.co/api/v2/pokemon"
request_res = requests.get(f'{url}').json()
pokemon_count = requests.get(f'{url}').json()['count']
pokemons = requests.get(f'{url}?limit={pokemon_count}&offset=0').json()['results']

def index(request):
    q = request.GET.get('q')
    page = request.GET.get('page')

    filtered = []
    if q is None or q == 'None':
        filtered = pokemons
    else:
        for pokemon in pokemons:
            if pokemon['name'].__contains__(q):
                filtered.append(pokemon)

    paginator = Paginator(filtered, 10)
    page_obj = paginator.get_page(page)

    for pokemon in page_obj:
        pokemon['info'] = get_all_info(pokemon['name'])

    context = {
        'pokemons': filtered,
        'page_obj': page_obj,
        'q': request.GET.get('q'),
    }
    return render(request, 'index.html', context)

def pokemon(request, name):
    info = get_all_info(name)
    print(info)
    context = {
        "pokemon": info,
        "hp": info['stats'][0]['base_stat'],
        "attack": info['stats'][1]['base_stat'],
    }
    return render(request, "pokemon.html", context)

def get_some_info(name):
    return requests

def get_all_info(name):
    return requests.get(f"{url}/{name}").json()