"""
Custom permission classes for the messaging app.
Controls access to conversations and messages based on participation.
"""

from rest_framework import permissions


class IsParticipantOfConversation(permissions.BasePermission):
    """
    Custom permission to only allow participants of a conversation to access it.

    This permission checks:
    1. User is authenticated
    2. User is a participant in the conversation being accessed
    3. For messages, user is a participant in the message's conversation

    Applied to:
    - ConversationViewSet: ensures users can only access conversations they're part of
    - MessageViewSet: ensures users can only view/send messages in conversations they're part of
    """

    message = "You must be a participant of this conversation to perform this action."

    def has_permission(self, request, view):
        """
        Check if user is authenticated before proceeding to object-level permissions.
        """
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        """
        Check if user is a participant in the conversation.

        For Conversation objects: check if user is in participants
        For Message objects: check if user is in the conversation's participants
        """
        # Handle Conversation objects
        if hasattr(obj, 'participants'):
            return request.user in obj.participants.all()

        # Handle Message objects - check the conversation's participants
        if hasattr(obj, 'conversation'):
            return request.user in obj.conversation.participants.all()

        # If neither, deny access
        return False


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    Others can read but not modify.
    """

    def has_object_permission(self, request, view, obj):
        """
        Read permissions are allowed for any authenticated user.
        Write permissions are only allowed to the owner.
        """
        # Read permissions (GET, HEAD, OPTIONS) are allowed for authenticated users
        if request.method in permissions.SAFE_METHODS:
            return request.user.is_authenticated

        # Write permissions are only allowed to the owner
        # For messages, check if user is the sender
        if hasattr(obj, 'sender'):
            return obj.sender == request.user

        # For other objects, check if user is the creator/owner
        if hasattr(obj, 'user'):
            return obj.user == request.user

        return False


class IsMessageSender(permissions.BasePermission):
    """
    Permission to only allow the sender of a message to edit or delete it.
    """

    message = "You can only edit or delete your own messages."

    def has_object_permission(self, request, view, obj):
        """
        Only allow the sender to modify their message.
        """
        # For Message objects
        if hasattr(obj, 'sender'):
            # Allow read for participants (checked by IsParticipantOfConversation)
            if request.method in permissions.SAFE_METHODS:
                return True
            # Only sender can modify
            return obj.sender == request.user

        return False
