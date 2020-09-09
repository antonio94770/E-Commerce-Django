from django.contrib import admin
from .models import Categoria,Regione,Prodotto


class GestioneCategoriaAdmin(admin.ModelAdmin):
    list_display = ['nome', 'slug']
    prepopulated_fields = {'slug': ('nome',)}


admin.site.register(Categoria, GestioneCategoriaAdmin)


class GestioneRegioneAdmin(admin.ModelAdmin):
    list_display = ['nome', 'slug']
    prepopulated_fields = {'slug': ('nome',)}


admin.site.register(Regione, GestioneRegioneAdmin)


class GestioneProdottoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'slug', 'user', 'prezzo', 'disponibilita', 'regione','orario_creazione', 'orario_aggiornamento', 'immagine']
    list_filter = ['disponibilita', 'orario_creazione', 'orario_aggiornamento', 'regione']
    list_editable = ['disponibilita']
    prepopulated_fields = {'slug': ('nome',)}


admin.site.register(Prodotto, GestioneProdottoAdmin)