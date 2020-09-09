from .models import *
from utenti.models import Profile

def nuovi_dialoghi_count(request):
	count = 0
	if request.user.is_authenticated():
		chats = Chat.objects.filter(members__in=[request.user.id])
		profile = Profile.objects.get(user=request.user)
		if chats:
			for chat in chats:
				if Message.objects.filter(chat=chat.id, is_readed=False).exclude(author=profile).count():
					count = count + 1
					continue
	return {"nuovi_dialoghi_count":count}


