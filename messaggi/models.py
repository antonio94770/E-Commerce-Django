from django.db import models
from utenti.models import Profile
from django.utils import timezone
 
 
class Chat(models.Model):
    members = models.ManyToManyField(Profile)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering=['-date']
 
    @models.permalink
    def get_absolute_url(self):
        return 'users:messages', (), {'chat_id': self.pk }
 
 
class Message(models.Model):
    chat = models.ForeignKey(Chat)
    author = models.ForeignKey(Profile)
    message = models.TextField()
    pub_date = models.DateTimeField(default=timezone.now)
    is_readed = models.BooleanField(default=False)
 
    class Meta:
        ordering=['pub_date']
 
    def __str__(self):
        return self.message