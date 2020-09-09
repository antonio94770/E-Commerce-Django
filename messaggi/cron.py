from django_cron import CronJobBase, Schedule
from utenti.models import Profile
from messaggi.models import *
from datetime import datetime, timedelta


class ReportMessaggi(CronJobBase):

	schedule = Schedule(run_every_mins=0)
	code = 'messaggi.ReportMessaggi'

	def do(self):
		profiles = Profile.objects.all()
		for profile in profiles:
			if profile.temporizzazione_giorni > 0 and (datetime.today()-profile.temporizzazione_data).days > profile.temporizzazione_giorni:
				count = 0
				chats = Chat.objects.filter(members__in=[profile.id])
				for chat in chats:
					count = count + Message.objects.filter(chat=chat.id, is_readed=False).exclude(author=profile).count()

				subject = "Hai dei nuovi messaggi"
				message = "Hai ricevuto " + str(count) + " nuovi messaggi"
				profile.user.email_user(subject, message)

				profile.temporizzazione_data = datetime.today()
				profile.save()