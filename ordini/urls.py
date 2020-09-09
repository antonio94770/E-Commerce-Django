from django.conf.urls import url
from . import views

app_name = 'ordini'

urlpatterns = [
	url(r'^(?P<id>\d+)/(?P<slug>[-\w]+)/ordine$', views.aggiungi_ordine, name='aggiungi_ordine'),
	url(r'^(?P<id>\d+)/(?P<slug>[-\w]+)/ordine/completato$', views.acquisto_ordine, name='acquisto_ordine'),
	url(r'^storico_vendite/$', views.storico_vendite_ordine, name='storico_vendite_ordine'),
	url(r'^storico_acquisti/$', views.storico_acquisti_ordine, name='storico_acquisti_ordine')
]