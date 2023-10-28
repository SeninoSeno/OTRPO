from django.db import models

class Fight(models.Model):
    first_pokemon_id = models.IntegerField()
    first_pokemon_hp = models.IntegerField()
    second_pokemon_id = models.IntegerField()
    second_pokemon_hp = models.IntegerField()
    winner_id = models.IntegerField()
    round_count = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
