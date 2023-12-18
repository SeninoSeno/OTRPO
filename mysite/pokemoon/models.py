from django.db import models

class Fight(models.Model):
    first_pokemon_id = models.IntegerField()
    first_pokemon_hp = models.IntegerField()
    second_pokemon_id = models.IntegerField()
    second_pokemon_hp = models.IntegerField()
    winner_id = models.IntegerField()
    round_count = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, null=True)

class Pokemon(models.Model):
    pokid = models.IntegerField()
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Feedback(models.Model):
    rating = models.IntegerField()
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, null=True)
    pokemon = models.ForeignKey("Pokemon", on_delete=models.CASCADE)

    def __str__(self):
        return {
            'rating': self.rating,
            'text': self.text,
            'created_at': self.created_at
        }