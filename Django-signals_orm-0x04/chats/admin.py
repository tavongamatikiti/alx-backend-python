"""
Admin configuration for the chats app models.
"""

from django.contrib import admin
from .models import User, Conversation, Message, Notification, MessageHistory


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
    list_display = ['message_id', 'sender', 'receiver', 'conversation', 'sent_at', 'edited', 'read']
    list_filter = ['sent_at', 'edited', 'read']
    search_fields = ['message_body', 'sender__username', 'receiver__username']


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    """Admin interface for Notification model."""
    list_display = ['notification_id', 'user', 'message', 'is_read', 'created_at']
    list_filter = ['is_read', 'created_at']
    search_fields = ['user__username', 'user__email']
    readonly_fields = ['notification_id', 'created_at']


@admin.register(MessageHistory)
class MessageHistoryAdmin(admin.ModelAdmin):
    """Admin interface for MessageHistory model."""
    list_display = ['history_id', 'message', 'edited_by', 'edited_at']
    list_filter = ['edited_at']
    search_fields = ['message__message_body', 'old_content']
    readonly_fields = ['history_id', 'edited_at']