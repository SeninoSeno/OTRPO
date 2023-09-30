from django.core.paginator import Paginator
import requests

url = "https://pokeapi.co/api/v2/pokemon"
count = requests.get(f'{url}').json()['count']
print(count)

# list = [requests.get(f'{url}/{i+1}').json()['name'] for i in range(10)]
# print(list)

list = requests.get(f'{url}?limit={count}&offset=0').json()

print(list['results'])

p = Paginator(list['results'], 10)
print(p.num_pages)






# for i in range (requests.get(f'{url}').json()['count']):
#     pokemon = requests.get(f'https://pokeapi.co/api/v2/pokemon/{i+1}')
#     print(pokemon.json()['name'])

