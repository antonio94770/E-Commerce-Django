from django.test import TestCase
from django.urls import resolve
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from .models import Chat
from utenti.models import Profile


class MessaggiTest(TestCase):

	def test_messaggi_view(self):
		chat = Chat.objects.create()

		user1 = User.objects.create_user('username_test', 'psw_test', 'email_test@gmail.com')
		user2 = User.objects.create_user('username_test2', 'psw_test2', 'email_test2@gmail.com')

		profile1 = get_object_or_404(Profile,user=user1)
		profile2 = get_object_or_404(Profile,user=user2)

		
		profile1.email_confirmed = True
		profile2.email_confirmed = True

		chat.members.add(profile1)
		chat.members.add(profile2)


		url = reverse('messaggi:messaggio', args=[chat.id])
		url2 = '/messaggi/'+ str(chat.id) + '/'

		self.assertEqual(url, url2)
		self.assertEqual(chat.members.count(), 2)
		self.assertTrue(profile1.email_confirmed)
		self.assertTrue(profile2.email_confirmed)



