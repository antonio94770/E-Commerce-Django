from django.db import models
from django.http import HttpResponse
from django.urls import reverse

from utenti.models import Profile
from inserzioni.models import Prodotto


class Ordine(models.Model):
	compratore = models.ForeignKey(Profile, related_name="compratore", on_delete=models.CASCADE)
	venditore = models.ForeignKey(Profile, related_name="venditore", on_delete=models.CASCADE)
	prodotto = models.ForeignKey(Prodotto, on_delete=models.CASCADE)
	prezzo = models.DecimalField(max_digits=10, decimal_places=2)
	orario_acquisto = models.DateTimeField(auto_now_add=True)
 
	class Meta:
		ordering = ('orario_acquisto', )
		verbose_name = 'ordine'
		verbose_name_plural = 'ordini'
