from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<str:name>', views.pokemon, name='pokemon'),
    path('<str:name>/fight', views.fight, name='fight'),
]