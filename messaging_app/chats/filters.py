"""
Custom filter classes for the messaging app.
Enables filtering messages by user, conversation, and time range.
"""

import django_filters
from .models import Message, Conversation


class MessageFilter(django_filters.FilterSet):
    """
    Filter class for Message model.

    Supports filtering by:
    - Conversation ID
    - Sender (user)
    - Date range (sent_at field)
    """
    # Filter by conversation
    conversation = django_filters.UUIDFilter(
        field_name='conversation__conversation_id',
        lookup_expr='exact',
        help_text='Filter messages by conversation UUID'
    )

    # Filter by sender
    sender = django_filters.UUIDFilter(
        field_name='sender__user_id',
        lookup_expr='exact',
        help_text='Filter messages by sender UUID'
    )

    # Date range filters
    date_from = django_filters.DateTimeFilter(
        field_name='sent_at',
        lookup_expr='gte',
        help_text='Filter messages sent after this date (format: YYYY-MM-DD or YYYY-MM-DD HH:MM:SS)'
    )

    date_to = django_filters.DateTimeFilter(
        field_name='sent_at',
        lookup_expr='lte',
        help_text='Filter messages sent before this date (format: YYYY-MM-DD or YYYY-MM-DD HH:MM:SS)'
    )

    # Search in message body
    message_body = django_filters.CharFilter(
        field_name='message_body',
        lookup_expr='icontains',
        help_text='Search for text within message body (case-insensitive)'
    )

    class Meta:
        model = Message
        fields = ['conversation', 'sender', 'date_from', 'date_to', 'message_body']


class ConversationFilter(django_filters.FilterSet):
    """
    Filter class for Conversation model.

    Supports filtering by:
    - Specific participant
    - Date range (created_at field)
    """
    # Filter by participant
    participant = django_filters.UUIDFilter(
        field_name='participants__user_id',
        lookup_expr='exact',
        help_text='Filter conversations by participant UUID'
    )

    # Date range filters
    created_from = django_filters.DateTimeFilter(
        field_name='created_at',
        lookup_expr='gte',
        help_text='Filter conversations created after this date'
    )

    created_to = django_filters.DateTimeFilter(
        field_name='created_at',
        lookup_expr='lte',
        help_text='Filter conversations created before this date'
    )

    class Meta:
        model = Conversation
        fields = ['participant', 'created_from', 'created_to']
