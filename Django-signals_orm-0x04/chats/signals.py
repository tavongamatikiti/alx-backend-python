"""
Django signals for the messaging application.

Implements automatic actions triggered by model events:
- Create notifications when new messages are sent
- Log message edit history before updates
- Clean up related data when users are deleted
"""

from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import Message, Notification, MessageHistory

User = get_user_model()


@receiver(post_save, sender=Message)
def create_notification_on_new_message(sender, instance, created, **kwargs):
    """
    Signal handler to create a notification when a new message is created.

    Triggered by: post_save signal on Message model
    When: After a Message instance is saved
    Action: Creates a Notification for the receiver (if exists)

    Args:
        sender: The model class (Message)
        instance: The actual Message instance being saved
        created: Boolean indicating if this is a new record
        **kwargs: Additional keyword arguments
    """
    if created and instance.receiver:
        # Only create notification for new messages with a receiver
        Notification.objects.create(
            user=instance.receiver,
            message=instance,
            is_read=False
        )
        print(f"✅ Notification created for {instance.receiver.username} - Message: {instance.message_id}")


@receiver(pre_save, sender=Message)
def log_message_edit_history(sender, instance, **kwargs):
    """
    Signal handler to log message edits before the message is updated.

    Triggered by: pre_save signal on Message model
    When: Before a Message instance is saved
    Action: If the message body changed, log the old content to MessageHistory

    Args:
        sender: The model class (Message)
        instance: The actual Message instance being saved
        **kwargs: Additional keyword arguments
    """
    # Only log if the message already exists (not a new message)
    if instance.pk:
        try:
            # Fetch the old message from database
            old_message = Message.objects.get(pk=instance.pk)

            # Check if the message body has changed
            if old_message.message_body != instance.message_body:
                # Mark the message as edited
                instance.edited = True

                # Create history entry with old content
                MessageHistory.objects.create(
                    message=old_message,
                    old_content=old_message.message_body,
                    edited_by=instance.sender  # Assuming sender is the one editing
                )
                print(f"✅ Message edit logged - Message: {instance.message_id}")
        except Message.DoesNotExist:
            # Message doesn't exist yet, skip history logging
            pass


@receiver(post_delete, sender=User)
def cleanup_user_data_on_delete(sender, instance, **kwargs):
    """
    Signal handler to clean up related data when a user is deleted.

    Triggered by: post_delete signal on User model
    When: After a User instance is deleted
    Action: Deletes all related messages, notifications, and message histories

    Args:
        sender: The model class (User)
        instance: The actual User instance being deleted
        **kwargs: Additional keyword arguments

    Note:
        Due to CASCADE foreign keys, most related data will be automatically
        deleted by Django. This signal provides explicit logging and can handle
        any custom cleanup logic.
    """
    user_id = instance.user_id
    username = instance.username

    # Count related data before deletion (for logging)
    sent_messages_count = instance.sent_messages.count()
    received_messages_count = instance.received_messages.count()
    notifications_count = instance.notifications.count()

    # Django's CASCADE will automatically delete:
    # - sent_messages (Message.sender FK)
    # - received_messages (Message.receiver FK)
    # - notifications (Notification.user FK)
    # - message_edits (MessageHistory.edited_by FK with SET_NULL)

    print(f"✅ User deleted: {username} (ID: {user_id})")
    print(f"   - Sent messages: {sent_messages_count}")
    print(f"   - Received messages: {received_messages_count}")
    print(f"   - Notifications: {notifications_count}")
    print(f"   All related data cleaned up via CASCADE")


# Alternative signal using django.db.models.signals.m2m_changed
# This would be useful if you want to track changes in Conversation participants
# Uncomment below if needed:

# from django.db.models.signals import m2m_changed
# from .models import Conversation

# @receiver(m2m_changed, sender=Conversation.participants.through)
# def notify_on_conversation_participant_change(sender, instance, action, pk_set, **kwargs):
#     """
#     Signal to notify users when they're added to or removed from a conversation.
#
#     Args:
#         sender: The through model class
#         instance: The Conversation instance
#         action: The type of change (pre_add, post_add, pre_remove, post_remove, etc.)
#         pk_set: Set of primary keys of the User instances being added/removed
#     """
#     if action == "post_add":
#         # Users were added to the conversation
#         for user_pk in pk_set:
#             user = User.objects.get(pk=user_pk)
#             print(f"✅ User {user.username} added to conversation {instance.conversation_id}")
#
#     elif action == "post_remove":
#         # Users were removed from the conversation
#         for user_pk in pk_set:
#             print(f"✅ User with ID {user_pk} removed from conversation {instance.conversation_id}")
