from django.urls import include, path
from . import views

urlpatterns = [
    path("", views.index, name='index'),
    path("<str:name>/info", views.pokemon, name='pokemon'),
    path("<str:name>/fight", views.fight, name='fight'),
    path("<str:name>/fight/result", views.result, name='result'),
    path("<str:name>/save", views.save_to_ftp, name='save'),
    path("<str:name>/ftp", views.save_to_ftp, name='save'),
    path("<str:name>/feedback", views.feedback, name='feedback'),
    # Account ↓
    path('accounts/', include('django.contrib.auth.urls')),
    path("accounts/login", views.login_view, name="login"),
    path("accounts/login/prove/", views.login_prove_view, name="login_prove"),
    path("accounts/logout", views.logout_view, name="logout"),
    path("accounts/registration", views.registration_view, name="register"),
    path('', include('social_django.urls')),
    # API ↓
    path("pokemon/list", views.PokemonList.as_view()),
    path("pokemon/<int:id>", views.PokemonInfo.as_view()),
    path("pokemon/random", views.RandomPokemon.as_view()),
    path("fight", views.PokemonFight.as_view()),
    path("fight/fast", views.PokemonAutoFight.as_view()),
    path("fight/auto", views.PokemonAutoFight.as_view()),
]