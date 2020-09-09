from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from inserzioni.models import Prodotto
from utenti.models import Profile
from .models import Ordine
from ordini.forms import FiltroOrdineForm
from datetime import datetime, timedelta
from django.utils import timezone

@require_POST
@login_required
def aggiungi_ordine(request, id, slug):
	prodotto = get_object_or_404(Prodotto, id=id, slug=slug)

	prezzo_totale = prodotto.prezzo
	user = User.objects.get(username=prodotto.user)
	venditore = Profile.objects.get(user=user)
	compratore = Profile.objects.get(user=request.user)

	if (compratore != venditore):
		return render(request, 'ordini/dettaglio_ordine.html', {'prodotto':prodotto, 'prezzo_totale':prezzo_totale})
	else:
		return redirect ('inserzioni:lista_prodotti')


@require_POST
@login_required
def acquisto_ordine(request, id, slug):
	prodotto = get_object_or_404(Prodotto, id=id, slug=slug)

	prezzo_totale = prodotto.prezzo
	user = User.objects.get(username=prodotto.user)
	venditore = Profile.objects.get(user=user)
	compratore = Profile.objects.get(user=request.user)

	if 'conferma_acquisto' in request.POST:
		if (compratore != venditore and prodotto.disponibilita):
			o = Ordine.objects.create(venditore=venditore,
						compratore=compratore,
						prodotto=prodotto,
						prezzo=prodotto.prezzo
						)
			o.save()

			prodotto.disponibilita = False
			prodotto.venduto = True
			prodotto.save()
			
			request.session['last_view'] = "ordine"
			request.session['user_name'] = venditore.user.username
			return HttpResponseRedirect(reverse('utenti:votazione', args=(venditore.user.username,)))

		
	return redirect ('inserzioni:lista_prodotti')


@login_required
def storico_vendite_ordine(request):
	guadagno = 0
	me = get_object_or_404(Profile,user=request.user)
	ordini = Ordine.objects.filter(venditore=me)
	
	if request.method == 'POST':
		form = FiltroOrdineForm(request.POST)
		if form.is_valid():
			giorni = form.cleaned_data['filtro']
			if giorni != "0":
				#print (datetime.today() - timedelta(days=int(giorni)))
				ordini = Ordine.objects.filter(orario_acquisto__gt=datetime.today()-timedelta(days=int(giorni)), venditore=me)
				
				for o in ordini:
					print (o.orario_acquisto)
					guadagno = guadagno + o.prezzo
				
				print (giorni)
			else:
				for o in ordini:
					guadagno = guadagno + o.prezzo
	else:
		for o in ordini:
			print (o.orario_acquisto)
			guadagno = guadagno + o.prezzo
		
		form = FiltroOrdineForm(initial={'filtro': 0})
		
	return render(request, 'ordini/storico_vendite.html', {'form': form, 'ordini':ordini, 'guadagno':guadagno})
	
	
@login_required
def storico_acquisti_ordine(request):
	me = get_object_or_404(Profile,user=request.user)
	ordini = Ordine.objects.filter(compratore=me)
	
	if request.method == 'POST':
		form = FiltroOrdineForm(request.POST)
		if form.is_valid():
			giorni = form.cleaned_data['filtro']
			if giorni != "0":
				ordini = Ordine.objects.filter(orario_acquisto__gt=datetime.today()-timedelta(days=int(giorni)), compratore=me)		
	else:
		form = FiltroOrdineForm(initial={'filtro': 0})
		
	return render(request, 'ordini/storico_acquisti.html', {'form': form, 'ordini':ordini})



	
	