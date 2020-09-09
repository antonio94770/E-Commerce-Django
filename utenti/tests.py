from django.test import TestCase
from .forms import SignUpForm, VoteForm
from django import forms
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse


class CustomFormTest(TestCase):

	def test_signup_form(self):
		form = SignUpForm({
			'username': 'ciao',
			'email': 'prova@gmail.com',
			'password1': 'psw12345',
			'password2': 'psw12345',
			'phone_number': '+390522648195',
			'temporizzazione_giorni': 1,
			})

		self.assertTrue(form.is_valid())


	def test_vote_form(self):
		form = VoteForm({
			'voto': 1
			})

		self.assertTrue(form.is_valid())


	def test_votazione_view(self):

		user = User.objects.create_user('username_test', 'psw_test', 'email_test@gmail.com')

		url = reverse('utenti:votazione', args=[user])
		url2 = '/votazione/'+ str(user) + '/'

		self.assertEqual(url, url2)