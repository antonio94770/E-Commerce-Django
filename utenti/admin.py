from django.contrib import admin
from .models import Profile


class GestioneProfili(admin.ModelAdmin):
    list_display = ['user', 'email_confirmed', 'vote_count', 'vote_total', 'vote_average']

admin.site.register(Profile, GestioneProfili)