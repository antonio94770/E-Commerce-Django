from django import forms
from decimal import *
from django.core.validators import MaxValueValidator, MinValueValidator
from inserzioni.models import Categoria,Regione,Prodotto


class FiltroForm(forms.Form):
	regione = forms.ModelChoiceField(queryset = Regione.objects.all(), empty_label="tutto", required=False)
	categoria = forms.ModelChoiceField(queryset = Categoria.objects.all(), empty_label="tutto", required=False)
		
		
class InserisciInserzioneForm(forms.Form):
	regione = forms.ModelChoiceField(queryset = Regione.objects.all(), empty_label=None)
	categoria = forms.ModelChoiceField(queryset = Categoria.objects.all(), empty_label=None)
	titolo = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', "placeholder": "Inserisci titolo.", 'maxlength':200}))
	descrizione = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', "placeholder": "Inserisci una descrizione del prodotto."}))
	prezzo = forms.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
	disponibilita = forms.BooleanField(required=False, initial = True)
	immagine = forms.ImageField(required=False)

class ModificaInserzioneFiltroForm(forms.Form):
	CHOICES=[('tutto','Tutto'),
			('venduti','Venduti'),
			('disponibili','Disponibili')]

	filtro = forms.ChoiceField(choices=CHOICES)