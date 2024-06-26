from django.db import models
from user.models import UserProfile


# chat room model 
class Conversation(models.Model):
    initiator = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True, related_name="convo_starter")
    receiver = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True, related_name="convo_participant")
    start_time = models.DateTimeField(auto_now_add=True)


#chat message model
class Message(models.Model):
    sender = models.ForeignKey(UserProfile, on_delete=models.SET_NULL,null=True, related_name='message_sender')
    text = models.CharField(max_length=200, blank=True)
    attachment = models.FileField(blank=True)
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE,)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-timestamp',)
