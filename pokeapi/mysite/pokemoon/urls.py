from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name='index'),
    path("<str:name>/info", views.pokemon, name='pokemon'),
    path("<str:name>/fight", views.fight, name='fight'),
    path("<str:name>/fight/result", views.result, name='result'),
    path("<str:name>/save", views.save_to_ftp, name='save'),
    path("<str:name>/ftp", views.save_to_ftp, name='save'),
    # API ↓
    path("pokemon/list", views.PokemonList.as_view()),
    path("pokemon/<int:id>", views.PokemonInfo.as_view()),
    path("pokemon/random", views.RandomPokemon.as_view()),
    path("fight", views.PokemonFight.as_view()),
    path("fight/fast", views.PokemonAutoFight.as_view()),
    path("fight/auto", views.PokemonAutoFight.as_view()),
]