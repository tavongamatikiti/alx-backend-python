"""
Models for the messaging application.
Defines User, Conversation, Message, Notification, and MessageHistory models with proper relationships.
Includes custom managers and signals support.
"""

import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Custom User model extending Django's AbstractUser.
    Includes additional fields for phone number and role.

    Inherited from AbstractUser:
    - username
    - first_name
    - last_name
    - password (hashed password field)
    """
    user_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        db_index=True
    )
    email = models.EmailField(unique=True, null=False)
    phone_number = models.CharField(max_length=15, null=True, blank=True)

    ROLE_CHOICES = [
        ('guest', 'Guest'),
        ('host', 'Host'),
        ('admin', 'Admin'),
        ('moderator', 'Moderator'),
    ]
    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default='guest',
        null=False
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'users'
        indexes = [
            models.Index(fields=['email']),
        ]

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"


class Conversation(models.Model):
    """
    Conversation model to track group or one-on-one chats.
    Uses many-to-many relationship with User model.
    """
    conversation_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        db_index=True
    )
    participants = models.ManyToManyField(
        User,
        related_name='conversations'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'conversations'
        ordering = ['-created_at']

    def __str__(self):
        return f"Conversation {self.conversation_id}"


class UnreadMessagesManager(models.Manager):
    """
    Custom manager for filtering unread messages.
    Optimized with .only() to retrieve only necessary fields.
    """
    def unread_for_user(self, user):
        """
        Get all unread messages for a specific user (as receiver).
        Uses .only() for field optimization.

        Args:
            user: User object to filter messages for

        Returns:
            QuerySet of unread messages
        """
        return self.filter(
            receiver=user,
            read=False
        ).select_related('sender', 'conversation').only(
            'message_id',
            'message_body',
            'sender__user_id',
            'sender__username',
            'sender__first_name',
            'sender__last_name',
            'conversation__conversation_id',
            'sent_at',
            'read'
        )


class Message(models.Model):
    """
    Message model for storing individual messages within conversations.
    Links to both User (sender, receiver) and Conversation.

    Includes fields for:
    - Threading (parent_message)
    - Read status tracking
    - Edit tracking
    """
    message_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        db_index=True
    )
    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='sent_messages'
    )
    receiver = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='received_messages',
        null=True,
        blank=True,
        help_text="Direct recipient of the message"
    )
    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name='messages'
    )
    message_body = models.TextField(null=False)
    sent_at = models.DateTimeField(auto_now_add=True)

    # New fields for Task requirements
    edited = models.BooleanField(
        default=False,
        help_text="Indicates if the message has been edited"
    )
    read = models.BooleanField(
        default=False,
        help_text="Indicates if the message has been read by the receiver"
    )
    parent_message = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        related_name='replies',
        null=True,
        blank=True,
        help_text="Parent message for threaded conversations"
    )

    # Default and custom managers
    objects = models.Manager()  # Default manager
    unread = UnreadMessagesManager()  # Custom manager for unread messages

    class Meta:
        db_table = 'messages'
        ordering = ['sent_at']
        indexes = [
            models.Index(fields=['conversation', 'sent_at']),
            models.Index(fields=['sender']),
            models.Index(fields=['receiver', 'read']),
            models.Index(fields=['parent_message']),
        ]

    def __str__(self):
        return f"Message from {self.sender} at {self.sent_at}"

    def get_thread(self):
        """
        Recursively retrieve all replies to this message.
        Uses prefetch_related for optimization.

        Returns:
            QuerySet of reply messages
        """
        return Message.objects.filter(
            parent_message=self
        ).prefetch_related('replies').select_related('sender', 'receiver')


class Notification(models.Model):
    """
    Notification model to store user notifications when they receive new messages.
    Created automatically via Django signals (post_save on Message).
    """
    notification_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='notifications',
        help_text="User who receives the notification"
    )
    message = models.ForeignKey(
        Message,
        on_delete=models.CASCADE,
        related_name='notifications',
        help_text="Message that triggered the notification"
    )
    is_read = models.BooleanField(
        default=False,
        help_text="Whether the notification has been read"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'notifications'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'is_read']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return f"Notification for {self.user} - Message {self.message.message_id}"


class MessageHistory(models.Model):
    """
    MessageHistory model to track message edits.
    Stores the old content before each edit.
    Created automatically via Django signals (pre_save on Message).
    """
    history_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    message = models.ForeignKey(
        Message,
        on_delete=models.CASCADE,
        related_name='edit_history',
        help_text="The message that was edited"
    )
    old_content = models.TextField(
        help_text="Content of the message before the edit"
    )
    edited_at = models.DateTimeField(auto_now_add=True)
    edited_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='message_edits',
        help_text="User who made the edit"
    )

    class Meta:
        db_table = 'message_history'
        ordering = ['-edited_at']
        indexes = [
            models.Index(fields=['message', 'edited_at']),
        ]
        verbose_name_plural = 'Message histories'

    def __str__(self):
        return f"Edit history for Message {self.message.message_id} at {self.edited_at}"
