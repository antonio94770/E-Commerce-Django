from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from . import views

app_name = 'messaggi'

urlpatterns = [
	url(r'^messaggi/$', login_required(views.DialogsView.as_view()), name='dialoghi'),
	url(r'^messaggi/create/(?P<user_id>\d+)/$', login_required(views.CreateDialogView.as_view()), name='crea_dialogo'),
	url(r'^messaggi/(?P<chat_id>\d+)/$', login_required(views.MessagesView.as_view()), name='messaggio')
]