from django.shortcuts import render
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseRedirect
from django.core.mail import send_mail
from django.utils import timezone

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

import requests
import random
import json
import os
from ftplib import FTP

from .models import Fight, Pokemon, Feedback


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
    pokemon = Pokemon.objects.get(name=name)
    print(Feedback.objects.filter(pokemon=pokemon))
    for feedback in Feedback.objects.filter(pokemon=name):
        print(feedback)

    context = {
        "pokemon": info,
        "hp": info['stats'][0]['base_stat'],
        "attack": info['stats'][1]['base_stat'],
    }
    return render(request, "pokemon.html", context)

def fight(request, name):
    pc_id = get_random_pokemon_id()
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
            message_text += f"\nВы проигарли ту битву... Вы рассыпались в прах при {data['user_hp']} очках здоровия. А у ворога вашего {data['pc_hp']} очков осталося"

        send_mail(
            'Информация о битве',
            message_text,
            os.environ['EMAIL_HOST_USER'],
            [data['email']],
            fail_silently=False,
        )

    return HttpResponse("Fight saved")

def save_to_ftp(request, name):
    if request.method == 'POST':
        pokemon = get_some_info(name)
        data = request.POST.dict()
        md = f"# [{name}](https://pokeapi.co/api/v2/pokemon/{name})\n"
        md += "### Info\n"
        md += f"* id: {pokemon['id']}\n"
        md += f"* height: {pokemon['height']}\n"
        md += f"* weight: {pokemon['weight']}\n"
        md += f"* hp: {pokemon['height']}\n"
        md += f"* attack: {pokemon['height']}\n"
        md += "### Image\n"
        md += f"[poke]({pokemon['image']} \"Image of {name}\")"

        try:
            ftp = FTP(data['server'])
            ftp.login(data['login'], data['password'])
            folder = f"{timezone.now().strftime('%Y%m%d')}"
            if not(folder in ftp.nlst()):
                ftp.mkd(folder)
            ftp.cwd(folder)
            if not(f"{name}.md" in ftp.nlst()):
                with open(f"{name}.md", "w") as file:
                    file.write(md)
                ftp.storbinary(f"STOR {name}.md", open(f"{name}.md", "rb"))
                os.remove(f"{name}.md")
            else:
                return HttpResponse("File already on ftp-server")
            ftp.quit()
            ftp.close()
        except Exception as e:
            return HttpResponse(f"Error: {e}")
        return HttpResponse("File saved on ftp-server")

def feedback(request, name):
    if request.method == 'POST':
        rating = request.POST.dict()['rating']
        text = request.POST.dict()['feedback']

        if not(Pokemon.objects.filter(name=name).exists()):
            pokemon = Pokemon()
            pokemon.pokid = get_some_info(name)['id']
            pokemon.name = name
            pokemon.save()
        pokemon = Pokemon.objects.get(name=name)

        feedback = Feedback()
        feedback.rating = rating
        feedback.text = text
        feedback.pokemon = pokemon
        feedback.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def get_name(id):
    return requests.get(f"{url}/{id}").json()['name']
def get_all_info(name):
    return requests.get(f"{url}/{name}").json()
def get_random_pokemon_id():
    pokemon_id = random.randint(1, pokemon_count);
    if pokemon_id > 1017:
        pokemon_id = 10000 + pokemon_id - 1017
    return pokemon_id
def get_some_info(id):
    info = get_all_info(id)
    return {
        "id": info['id'],
        "name": info['name'],
        "image": info['sprites']['front_default'],
        "height": info['height'],
        "weight": info['weight'],
        "hp": info['stats'][0]['base_stat'],
        "attack": info['stats'][1]['base_stat'],
    }


class RandomPokemon(APIView):
    def get(self, request):
        return Response({"pokemon": get_random_pokemon_id()})

class PokemonList(APIView):
    def get(self, request):
        f = request.GET.get('filters')
        filtered = []
        if f is None:
            filtered = pokemons
        else:
            for pokemon in pokemons:
                if pokemon['name'].__contains__(f):
                    filtered.append(pokemon)
        return Response({"pokemons": filtered})

class PokemonInfo(APIView):
    def get(self, request, id):
        return Response(get_some_info(id))

def skirmish(pc_throw, pc_hp, pc_attack, user_throw, user_hp, user_attack):
    winner = None
    if (pc_throw % 2 == user_throw % 2):
        pc_hp -= user_attack
        if pc_hp <= 0:
            winner = 'user'
    else:
        user_hp -= pc_attack
        if user_hp <= 0:
            winner = 'pc'
    return pc_hp, user_hp, winner

def fight_logic(user_id, pc_id, user_throw=None, is_auto=False):
    round_count = 0

    pc_throw = random.randint(1, 10)
    pc_hp = get_some_info(pc_id)['hp']
    pc_attack = get_some_info(pc_id)['attack']

    if user_throw is None:
        user_throw = random.randint(1, 10)
    user_hp = get_some_info(user_id)['hp']
    user_attack = get_some_info(user_id)['attack']

    winner = None
    if is_auto:
        while winner is None:
            pc_hp, user_hp, winner = skirmish(pc_throw, pc_hp, pc_attack, user_throw, user_hp, user_attack)
        round_count += 1
    else:
        pc_hp, user_hp, winner = skirmish(pc_throw, pc_hp, pc_attack, user_throw, user_hp, user_attack)
        round_count += 1

    return pc_hp, user_hp, winner, round_count

def get_ids(request):
    user_id = request.GET.get('user')
    if user_id is None:
        user_id = get_random_pokemon_id()

    pc_id = request.GET.get('pc')
    if pc_id is None:
        pc_id = get_random_pokemon_id()

    return user_id, pc_id

class PokemonFight(APIView):
    def get(self, request):
        user_id, pc_id = get_ids(request)
        return Response({'user': get_some_info(user_id),
                         'pc': get_some_info(pc_id)})

    def post(self, request):
        user_id, pc_id = get_ids(request)
        if (request.data < 1 or request.data > 10 or not(isinstance(request.data, int))):
            return Response(status=status.HTTP_418_IM_A_TEAPOT)
        else:
            pc_hp, user_hp, winner, round_count = fight_logic(user_id, pc_id, request.data)

        user_data = get_some_info(user_id)
        user_data['hp'] = user_hp
        pc_data = get_some_info(pc_id)
        pc_data['hp'] = pc_hp

        return Response({'winner': winner,
                         'round': round_count,
                         'user': user_data,
                         'pc': pc_data})

class PokemonAutoFight(APIView):
    def get(self, request):
        user_id, pc_id = get_ids(request)

        pc_hp, user_hp, winner, round_count = fight_logic(user_id, pc_id,
                                                          is_auto=True)
        user_data = get_some_info(user_id)
        user_data['hp'] = user_hp
        pc_data = get_some_info(pc_id)
        pc_data['hp'] = pc_hp

        return Response({'winner': winner,
                         'round': round_count,
                         'user': user_data,
                         'pc': pc_data})