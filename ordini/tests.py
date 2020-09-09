from django.test import TestCase
from django.urls import resolve

from .views import storico_vendite_ordine, storico_acquisti_ordine

class OrdiniTest(TestCase):

	def test_storico_vendite_view(self):
		view = resolve('/storico_vendite/')
		self.assertEquals(view.func, storico_vendite_ordine)

	def test_storico_acquisti_view(self):
		view = resolve('/storico_acquisti/')
		self.assertEquals(view.func, storico_acquisti_ordine)


