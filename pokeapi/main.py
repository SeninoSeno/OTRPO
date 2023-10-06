from django.core.paginator import Paginator
import requests


# I test something here

url = "https://pokeapi.co/api/v2/pokemon"
count = requests.get(f'{url}').json()['count']
print(count)

# list = [requests.get(f'{url}/{i+1}').json()['name'] for i in range(10)]
# print(list)

list = requests.get(f'{url}?limit={count}&offset=0').json()

q = "sun"
test = "sunshine"

print(test.__contains__(q))

filetered = []

print(list['results'])
print(list['results'][0]['name'])
for pokemon in list['results']:
    if pokemon['name'].__contains__(q):
        filetered.append(pokemon)

print(filetered)







# for i in range (requests.get(f'{url}').json()['count']):
#     pokemon = requests.get(f'https://pokeapi.co/api/v2/pokemon/{i+1}')
#     print(pokemon.json()['name'])

