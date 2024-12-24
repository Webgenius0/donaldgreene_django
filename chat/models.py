from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings



class ChatGroup(models.Model):
    name = models.CharField(max_length=255)
    admin = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='group_admin')
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='chat_groups')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Message(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_messages')
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='received_messages', null=True, blank=True)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    group = models.ForeignKey(ChatGroup, on_delete=models.CASCADE, related_name='messages', null=True, blank=True)
    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f'{self.sender} -> {self.recipient or self.group}: {self.content[:50]}'
