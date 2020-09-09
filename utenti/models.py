from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save,post_delete
from django.dispatch import receiver
from decimal import Decimal
from django.core.validators import RegexValidator


class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	email_confirmed = models.BooleanField(default=False)
	phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Formato numero di telefono: '+999999999', con un massimo di 15 cifre.")
	phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)
	temporizzazione_giorni = models.PositiveIntegerField(default=0)
	temporizzazione_data = models.DateTimeField(auto_now_add=True)
	vote_count = models.PositiveIntegerField(default=0)
	vote_total = models.PositiveIntegerField(default=0)
	vote_average = models.DecimalField(max_digits=2, decimal_places=1, default=Decimal(0.0))
	
	def __str__(self):
		return self.user.username


@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
	if created:
		Profile.objects.create(user=instance)
	instance.profile.save()
	
@receiver(post_delete, sender=Profile)
def delete_user_profile(sender, instance, **kwargs):
	u = User.objects.get(username=instance.user.username)
	u.delete()