from django.contrib import admin
from .models import Fight, Pokemon, Feedback

class FightAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Fight._meta.get_fields()]
admin.site.register(Fight, FightAdmin)

class PokemonAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Pokemon._meta.get_fields()]
admin.site.register(Pokemon, PokemonAdmin)

class FeedbackAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Feedback._meta.get_fields()]
admin.site.register(Feedback, FeedbackAdmin)