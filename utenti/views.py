from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from utenti.forms import *
from utenti.tokens import account_activation_token
from .models import Profile


def signup(request):
	if request.method == 'POST':
		form = SignUpForm(request.POST)
		if form.is_valid():
			user = form.save()
			
			user.refresh_from_db() 
			user.username = form.cleaned_data.get('username')
			user.set_password(form.cleaned_data.get('password1'))
			user.email = form.cleaned_data.get('email')
			user.profile.phone_number = form.cleaned_data.get('phone_number')
			user.profile.temporizzazione_giorni = form.cleaned_data.get('temporizzazione_giorni')
			user.is_active = False
			user.save()

			current_site = get_current_site(request)
			subject = 'Activate Your MySite Account'
			message = render_to_string('utenti/account_activation_email.html', {
				'user': user,
				'domain': current_site.domain,
				'uid': urlsafe_base64_encode(force_bytes(user.pk)),
				'token': account_activation_token.make_token(user),
			})
			user.email_user(subject, message)

			return redirect('utenti:account_activation_sent')
	else:
		form = SignUpForm()
	return render(request, 'utenti/signup.html', {'form': form})
	
	
@login_required
def modifica_profilo(request):
	user = get_object_or_404(User, username = request.user)
	if request.method == 'POST':
		form = EditProfileForm(request.POST, instance=request.user)
		if form.is_valid():
			user.username = form.cleaned_data['username']
			user.set_password(form.cleaned_data['new_password1'])
			user.email = form.cleaned_data['email']
			user.profile.phone_number = form.cleaned_data.get('phone_number')
			
			user.save()
			login(request, user)

			return redirect('inserzioni:lista_prodotti')
	else:
		form = EditProfileForm(instance = request.user, initial={'username': request.user.username,'email': request.user.email,'phone_number': request.user.profile.phone_number, 'temporizzazione_giorni': request.user.profile.temporizzazione_giorni})
	return render(request, 'utenti/modifica_profilo.html', {'form': form})


def account_activation_sent(request):
    return render(request, 'utenti/account_activation_sent.html')


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.profile.email_confirmed = True
        user.save()
        login(request, user)
        return redirect('inserzioni:lista_prodotti')
    else:
        return render(request, 'utenti/account_activation_invalid.html')
		
@login_required		
def votazione(request, username):
	user = get_object_or_404(User, username=username)
	profilo_venditore = get_object_or_404(Profile,user=user)
	
	previous_url = request.session['last_view']
	if request.user.username != profilo_venditore.user.username and request.session['last_view'] == "ordine" and request.session['user_name'] == profilo_venditore.user.username:
		if request.method == 'POST':
			form = VoteForm(request.POST)
			if form.is_valid():
				voto = int(form.cleaned_data['voto'])
				profilo_venditore.vote_total = profilo_venditore.vote_total + voto
				profilo_venditore.vote_count = profilo_venditore.vote_count + 1
				profilo_venditore.vote_average = profilo_venditore.vote_total / profilo_venditore.vote_count 
				profilo_venditore.save()
				request.session['last_view'] = "null"
				request.session['user_name'] = "null"
				
				return redirect('inserzioni:lista_prodotti')
	else:
		return redirect('inserzioni:lista_prodotti')
	
	form = VoteForm()
	
	context = {
		'username': username,
		'form': form
	}
	
	return render(request, 'utenti/votazione.html', context)