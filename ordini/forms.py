from django import forms

class FiltroOrdineForm(forms.Form):

	giorni = (
			(0,'Tutto'),
			(1,'1 giorno'),
			(30,'30 giorni'),
			(60,'60 giorni')
			)
	filtro = forms.ChoiceField(choices=giorni, label="Intervallo giorni")
	