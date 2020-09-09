from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Categoria,Regione,Prodotto
from utenti.models import Profile
from .forms import *



def lista_prodotti(request,regione_slug=None, categoria_slug=None):
	prodotti = Prodotto.objects.filter(disponibilita=True, venduto=False)
	categoria = Categoria.objects.all()
	regione = Regione.objects.all()
		
	if request.method == 'POST':
		form = FiltroForm(request.POST)
		if form.is_valid():
			categoria_form = "tutto"
			regione_form = "tutto"
			
			if (form.cleaned_data['categoria'] != None):
				categoria_form = form.cleaned_data['categoria'].slug
				
			if (form.cleaned_data['regione'] != None):
				regione_form = form.cleaned_data['regione'].slug
				
			return HttpResponseRedirect(reverse('inserzioni:lista_prodotti_filtro_regione_categoria', args=(regione_form,categoria_form,)))
	else:
		if categoria_slug and regione_slug:
			if(categoria_slug != "tutto" and regione_slug!="tutto"):
				categoria = get_object_or_404(Categoria, slug=categoria_slug)
				regione = get_object_or_404(Regione, slug=regione_slug)
				prodotti = Prodotto.objects.filter(categoria=categoria, regione=regione)
			elif (categoria_slug == "tutto" and regione_slug!="tutto"):
				regione = get_object_or_404(Regione, slug=regione_slug)
				prodotti = Prodotto.objects.filter(regione=regione)
			elif (categoria_slug != "tutto" and regione_slug=="tutto"):
				categoria = get_object_or_404(Categoria, slug=categoria_slug)
				prodotti = Prodotto.objects.filter(categoria=categoria)
		form = FiltroForm(initial={'categoria': categoria, 'regione':regione})
		return render(request, 'inserzioni/list.html', { 'form': form, 'prodotti': prodotti, 'categoria':categoria, 'regione':regione})

def dettaglio_prodotti(request, id, slug):
	prodotto = get_object_or_404(Prodotto, id=id, slug=slug, disponibilita=True, venduto=False)
	compratore = False
	venditore = False
	
	
	if request.user.is_authenticated():
		if prodotto.user.user.username != request.user.username:
			compratore = True;
		else:
			venditore = True;
	
	context = {
		'prodotto': prodotto,
		'compratore': compratore,
		'venditore': venditore
	}
	return render(request, 'inserzioni/detail.html', context)


@login_required
def crea_inserzione(request):
	if request.method == 'POST':
		form = InserisciInserzioneForm(request.POST, request.FILES)
		if form.is_valid():
			user = request.user
			categoria = form.cleaned_data['categoria'].slug
			regione = form.cleaned_data['regione'].slug
			nome = form.cleaned_data['titolo']
			descrizione = form.cleaned_data['descrizione']
			prezzo = form.cleaned_data['prezzo']
			disponibilita = form.cleaned_data['disponibilita']
			immagine = form.cleaned_data['immagine']
			p = Prodotto.objects.create(categoria=Categoria.objects.get(slug=categoria),
						regione=Regione.objects.get(slug=regione),
						user=Profile.objects.get(user=user),
						nome=nome,
						descrizione=descrizione,
						prezzo=prezzo,
						disponibilita=disponibilita,
						immagine=immagine)
			p.save()
       
			return redirect('inserzioni:lista_prodotti')
	else:
		form = InserisciInserzioneForm(initial={'prezzo': 0.00})
		
	return render(request, 'inserzioni/crea_inserzione.html', { 'form': form })
		
@login_required	
def lista_mie_inserzioni(request):
	prodotti = Prodotto.objects.filter(user=Profile.objects.get(user=request.user), venduto=False)

	if request.method == 'POST':
		form = ModificaInserzioneFiltroForm(request.POST)
		if form.is_valid():
			filtro = form.cleaned_data['filtro']
			if filtro == 'venduti':
				prodotti = Prodotto.objects.filter(user=Profile.objects.get(user=request.user), disponibilita=False)
			elif filtro == 'disponibili':
				prodotti = Prodotto.objects.filter(user=Profile.objects.get(user=request.user), disponibilita=True)
	else:
		form = ModificaInserzioneFiltroForm()
	return render(request, 'inserzioni/le_mie_inserzioni.html', { 'prodotti': prodotti, 'form':form})

@login_required
def modifica_prodotti(request, id, slug):
	prodotto = get_object_or_404(Prodotto, user=Profile.objects.get(user=request.user), id=id, slug=slug, venduto=False)

	if request.method == 'POST':
		form = InserisciInserzioneForm(request.POST, request.FILES)
		if form.is_valid():
			prodotto.categoria = Categoria.objects.get(slug=form.cleaned_data['categoria'].slug)
			prodotto.regione = Regione.objects.get(slug=form.cleaned_data['regione'].slug)
			prodotto.nome = form.cleaned_data['titolo']
			prodotto.descrizione = form.cleaned_data['descrizione']
			prodotto.prezzo = form.cleaned_data['prezzo']
			prodotto.disponibilita = form.cleaned_data['disponibilita']
			prodotto.immagine = form.cleaned_data['immagine']
			prodotto.save()
       
			return redirect('inserzioni:lista_mie_inserzioni')
		else:
			return HttpResponse('Data not valid')		
		
	else:
		categoria = Categoria.objects.get(slug=prodotto.categoria.slug)
		form = InserisciInserzioneForm(initial={'categoria': (prodotto.categoria.slug, prodotto.categoria.nome), 'regione': (prodotto.regione.slug, prodotto.regione.nome), 'titolo': prodotto.nome, 'descrizione':prodotto.descrizione, 'prezzo':prodotto.prezzo, 'disponibilita':prodotto.disponibilita, 'immagine':prodotto.immagine})
		return render(request, 'inserzioni/modifica_inserzione.html', {'form': form}) 
	
	
	