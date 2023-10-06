from django.shortcuts import render
import requests
from django.core.paginator import Paginator


def index(request):
    q = request.GET.get('q')
    page = request.GET.get('page')

    url = "https://pokeapi.co/api/v2/pokemon"
    count = requests.get(f'{url}').json()['count']
    pokemons = requests.get(f'{url}?limit={count}&offset=0').json()['results']

    filtered = []
    if q is None:
        filtered = pokemons
    else:
        for pokemon in pokemons:
            if pokemon['name'].__contains__(q):
                filtered.append(pokemon)

    paginator = Paginator(filtered, 10)
    page_obj = paginator.get_page(page)

    context = {
        'pokemons': filtered,
        'page_obj': page_obj,
        'q': request.GET.get('q'),
    }

    return render(request, 'index.html', context)
