"""
Views for the messaging application.
Implements ViewSets for Conversation and Message models.
"""

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import User, Conversation, Message
from .serializers import UserSerializer, ConversationSerializer, MessageSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet for listing and creating users.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ConversationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing conversations.
    Provides endpoints to list, create, and retrieve conversations.
    """
    queryset = Conversation.objects.all().prefetch_related('participants', 'messages')
    serializer_class = ConversationSerializer

    def create(self, request, *args, **kwargs):
        """
        Create a new conversation with specified participants.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        conversation = serializer.save()
        return Response(
            self.get_serializer(conversation).data,
            status=status.HTTP_201_CREATED
        )

    @action(detail=True, methods=['post'])
    def add_message(self, request, pk=None):
        """
        Add a message to an existing conversation.
        """
        conversation = self.get_object()
        message_data = {
            'conversation': conversation.conversation_id,
            'sender_id': request.data.get('sender_id'),
            'message_body': request.data.get('message_body')
        }

        serializer = MessageSerializer(data=message_data)
        serializer.is_valid(raise_exception=True)
        message = serializer.save()

        return Response(
            MessageSerializer(message).data,
            status=status.HTTP_201_CREATED
        )


class MessageViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing messages.
    Provides endpoints to list, create, and retrieve messages.
    """
    queryset = Message.objects.all().select_related('sender', 'conversation')
    serializer_class = MessageSerializer

    def create(self, request, *args, **kwargs):
        """
        Create a new message in a conversation.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        message = serializer.save()
        return Response(
            self.get_serializer(message).data,
            status=status.HTTP_201_CREATED
        )

    def get_queryset(self):
        """
        Optionally filter messages by conversation.
        """
        queryset = super().get_queryset()
        conversation_id = self.request.query_params.get('conversation', None)
        if conversation_id:
            queryset = queryset.filter(conversation__conversation_id=conversation_id)
        return queryset