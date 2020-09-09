from .forms import *
from .models import *
from django.views.generic import View
from django.db.models import Count
from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from utenti.models import Profile
from datetime import datetime, timedelta


class DialogsView(View):
	def get(self, request):
		user = Profile.objects.get(user=request.user)

		message = Message.objects.filter(chat__members__in=[request.user.id], is_readed=False).exclude(author=user)
		chats = Chat.objects.filter(message__in=message).distinct()
		return render(request, 'messaggi/dialoghi.html', {'user_profile': user, 'chats': chats, 'form':FiltroMessageForm(initial={'filtro_dialoghi': False})})

	def post(self,request):
		user = Profile.objects.get(user=request.user)
		chats = Chat.objects.filter(members__in=[user.id])
		form = FiltroMessageForm(request.POST)
		giorni = 0
		filtro_dialoghi = 'tutto'
		if form.is_valid():
			giorni = form.cleaned_data['filtro_giorni']
			filtro_dialoghi = form.cleaned_data['filtro_dialoghi']
			if giorni != "0" and filtro_dialoghi != 'tutto':
				message = Message.objects.filter(chat__members__in=[user.id], is_readed=filtro_dialoghi).exclude(author=user)
				chats = Chat.objects.filter(date__gt=datetime.today()-timedelta(days=int(giorni)), message=message).distinct()
			elif giorni != "0" and filtro_dialoghi == 'tutto':
				chats = Chat.objects.filter(date__gt=datetime.today()-timedelta(days=int(giorni)), members__in=[user.id]).distinct()
			elif giorni == "0" and filtro_dialoghi != 'tutto':
				message = Message.objects.filter(chat__members__in=[user.id], is_readed=filtro_dialoghi).exclude(author=user)
				chats = Chat.objects.filter(members__in=[user.id], message=message).distinct()

		return render(request, 'messaggi/dialoghi.html', {'user_profile': user, 'chats': chats, 'form':FiltroMessageForm(initial={'filtro_giorni': giorni, 'filtro_dialoghi': filtro_dialoghi})})

		
class MessagesView(View):
	def get(self, request, chat_id):
		profile = Profile.objects.get(user=request.user)
		try:
			chat = Chat.objects.get(id=chat_id)
			if profile in chat.members.all():
				chat.message_set.filter(is_readed=False).exclude(author=profile).update(is_readed=True)

			else:
				chat = None
		except Chat.DoesNotExist:
		    chat = None

		return render(
		    request,
		    'messaggi/lista_messaggi.html',
		    {
		        'user_profile': profile,
		        'chat': chat,
		        'form': MessageForm()
		    }
		)
 
	def post(self, request, chat_id):
		profile = Profile.objects.get(user=request.user)
		chat = Chat.objects.get(id=chat_id)
		form = MessageForm(data=request.POST)
		if form.is_valid():
			message = form.save(commit=False)
			message.chat_id = chat_id
			message.author = profile
			message.save()
			chat.date = message.pub_date
			chat.save()

			profile_2 = Profile.objects.exclude(user=request.user).get(chat = chat)
			if not profile_2.temporizzazione_giorni:
				subject = "Hai un nuovo messaggio"
				message = "Hai ricevuto un nuovo messaggio da parte di " + Profile.objects.get(user=request.user).user.username
				profile_2.user.email_user(subject, message)

		return render(
		    request,
		    'messaggi/lista_messaggi.html',
		    {
		        'user_profile': profile,
		        'chat': chat,
		        'form': MessageForm()
		    }
		)
		
class CreateDialogView(View):
	def get(self, request, user_id):
		profile_1 = Profile.objects.get(user=request.user)
		profile_2 = Profile.objects.get(id=user_id)

		chats = Chat.objects.filter(members__in=[profile_1.id, profile_2.id]).annotate(c=Count('members')).filter(c=2)
		if chats.count() == 0:
			chat = Chat.objects.create()
			chat.members.add(profile_1)
			chat.members.add(profile_2)
		else:
			chat = chats.first()
		return redirect(reverse('messaggi:messaggio', kwargs={'chat_id': chat.id}))