from django.shortcuts import render
import requests
from django.core.paginator import Paginator


def index(request):
    url = "https://pokeapi.co/api/v2/pokemon"
    count = requests.get(f'{url}').json()['count']
    pokemons = requests.get(f'{url}?limit={count}&offset=0').json()['results']

    paginator = Paginator(pokemons, 10)
    page_number = request.GET.get('page')
    print(request)
    print(page_number)
    print(request.GET.get('q'))
    page_obj = paginator.get_page(page_number)

    context = {
        'pokemons': pokemons,
        'page_obj': page_obj,
        'q': request.GET.get('q'),
    }

    return render(request, 'index.html', context)
