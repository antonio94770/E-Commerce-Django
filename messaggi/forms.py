from django import forms
from django.forms import ModelForm
from .models import Message

class MessageForm(ModelForm):
    class Meta:
        model = Message
        fields = ['message']
        labels = {'message': ""}

class FiltroMessageForm(forms.Form):
	giorni = (
			(0,'Tutto'),
			(1,'1 giorno'),
			(30,'30 giorni'),
			(60,'60 giorni')
			)

	filtro=[('tutto','Tutto'),
			(False,'Non letti')]

	filtro_dialoghi = forms.ChoiceField(choices=filtro, label="Dialoghi")
	filtro_giorni = forms.ChoiceField(choices=giorni, label="Intervallo giorni")