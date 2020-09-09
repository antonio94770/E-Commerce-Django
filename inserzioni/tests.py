from django.test import TestCase
from .models import *
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse


class InserzioniTest(TestCase):

	def test_modifica_inserzione_view(self):

		categoria = Categoria.objects.create(nome="test categoria")
		regione = Regione.objects.create(nome="test regione")
		user = User.objects.create_user('username_test', 'psw_test', 'email_test@gmail.com')
		profile = get_object_or_404(Profile,user=user)

		prodotto = Prodotto.objects.create(categoria=categoria, regione=regione, user=profile, nome="titolo test", descrizione="descrizione test", prezzo=29)

		url = reverse('inserzioni:modifica_prodotti', args=[prodotto.id, prodotto.slug])
		url2 = '/'+ str(prodotto.id) + '/' + prodotto.slug + '/modifica'

		self.assertEqual(url, url2)