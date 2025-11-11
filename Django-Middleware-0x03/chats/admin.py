"""
Admin configuration for the chats app models.
"""

from django.contrib import admin
from .models import User, Conversation, Message


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Admin interface for User model."""
    list_display = ['user_id', 'username', 'email', 'role', 'created_at']
    list_filter = ['role', 'created_at']
    search_fields = ['username', 'email', 'first_name', 'last_name']


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    """Admin interface for Conversation model."""
    list_display = ['conversation_id', 'created_at']
    filter_horizontal = ['participants']


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    """Admin interface for Message model."""
    list_display = ['message_id', 'sender', 'conversation', 'sent_at']
    list_filter = ['sent_at']
    search_fields = ['message_body', 'sender__username']