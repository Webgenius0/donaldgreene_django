from django.contrib import admin
from unfold.admin import ModelAdmin

from .models import ChatGroup, Message

@admin.register(ChatGroup)
class ChatGroupAdmin(ModelAdmin):
    list_display = ['name', 'admin','created_at']

@admin.register(Message)
class MessageAdmin(ModelAdmin):
    list_display = ['sender', 'recipient','group', 'content','timestamp', 'is_read']
