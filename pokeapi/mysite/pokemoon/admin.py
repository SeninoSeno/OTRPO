from django.contrib import admin
from .models import Fight

class FightAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Fight._meta.get_fields()]

admin.site.register(Fight, FightAdmin)