from django.conf.urls import url
from django.contrib import admin
from . import views

app_name = 'inserzioni'


urlpatterns = [
	url(r'^admin/', admin.site.urls),
    url(r'^$', views.lista_prodotti, name='lista_prodotti'),
	url(r'^(?P<regione_slug>[-\w]+)/(?P<categoria_slug>[-\w]+)$', views.lista_prodotti, name='lista_prodotti_filtro_regione_categoria'),
    url(r'^(?P<id>\d+)/(?P<slug>[-\w]+)/$', views.dettaglio_prodotti, name='dettaglio_prodotti'),
	url(r'^crea_inserzione/', views.crea_inserzione, name='crea_inserzione'),
	url(r'^le_mie_inserzioni/', views.lista_mie_inserzioni, name='lista_mie_inserzioni'),
	url(r'^(?P<id>\d+)/(?P<slug>[-\w]+)/modifica$', views.modifica_prodotti, name='modifica_prodotti')
]