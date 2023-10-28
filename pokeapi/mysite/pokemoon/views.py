from django.shortcuts import render
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt,csrf_protect
from django.core.mail import send_mail

import requests
import random
import json
import os

from .models import Fight


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
    context = {
        "pokemon": info,
        "hp": info['stats'][0]['base_stat'],
        "attack": info['stats'][1]['base_stat'],
    }
    return render(request, "pokemon.html", context)

def fight(request, name):
    pc_id = random.randint(1, pokemon_count)
    pc_info = get_all_info(pc_id)
    user_info = get_all_info(name)

    context = {
        "pc": pc_info,
        "pc_hp": pc_info['stats'][0]['base_stat'],
        "pc_attack": pc_info['stats'][1]['base_stat'],

        "user": user_info,
        "user_hp": user_info['stats'][0]['base_stat'],
        "user_attack": user_info['stats'][1]['base_stat'],
    }
    return render(request, "fight.html", context)

def result(request, name):
    data = json.loads(request.body.decode("utf-8"))

    fight = Fight()
    fight.first_pokemon_id = data['user_id']
    fight.first_pokemon_hp = data['user_hp']
    fight.second_pokemon_id = data['pc_id']
    fight.second_pokemon_hp = data['pc_hp']
    fight.round_count = data['round_count']
    fight.winner_id = data['winner_id']
    fight.save()

    if (data['send_on_mail']):
        message_text = f"Развернулась однажды битва меж {get_name(data['user_id'])} (Вы) да {get_name(data['pc_id'])}. " \
               f"Долгая была битва... Ажна в {data['round_count']} день/дня и {data['round_count']} ночь/ночи билися!" \
               f"\nЕжели исход не помните - освежу память вашу:"
        if (data['user_id'] == data['winner_id']):
            message_text += f"\nПобедили Вы! Побили ворожину аж до {data['pc_hp']} очков здоровия, сам оставшись при {data['user_hp']}. Эво как!"
        else:
            message_text += f"\nВы проигарли ту битву... Вы рассыпались в прах при {data['user_hp']} очках здоровия. А у ворога вашего {data['pc_hp']} осталося"

        send_mail(
            'Информация о битве',
            message_text,
            os.environ['EMAIL_HOST_USER'],
            [data['email']],
            fail_silently=False,
        )

    return HttpResponse("Fight saved")

def get_name(id):
    return requests.get(f"{url}/{id}").json()['name']

def get_all_info(name):
    return requests.get(f"{url}/{name}").json()