from django.contrib import admin
from .models import Ordine


class GestioneOrdiniAdmin(admin.ModelAdmin):
	list_display = ['venditore', 'compratore', 'prezzo', 'orario_acquisto']


admin.site.register(Ordine, GestioneOrdiniAdmin)