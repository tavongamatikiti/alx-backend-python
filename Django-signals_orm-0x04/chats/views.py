"""
Views for the messaging application.
Implements ViewSets for Conversation and Message models with filters.
Includes view caching for performance optimization.
"""

from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import viewsets, status, filters, permissions
from rest_framework.decorators import action, api_view, permission_classes as perm_decorator
from rest_framework.response import Response
from .models import User, Conversation, Message
from .serializers import UserSerializer, ConversationSerializer, MessageSerializer
from .permissions import IsParticipantOfConversation, IsMessageSender
from .pagination import MessagePagination, ConversationPagination
from .filters import MessageFilter, ConversationFilter


class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet for listing and creating users.
    Only authenticated users can view user lists.
    Users can only update their own profile.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Filter to return only the authenticated user's data for sensitive operations.
        Admin users can see all users.
        """
        if self.request.user.is_staff:
            return User.objects.all()
        # Regular users can only see themselves
        return User.objects.filter(user_id=self.request.user.user_id)


class ConversationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing conversations.
    Provides endpoints to list, create, and retrieve conversations.
    Only participants can view and interact with conversations.
    """
    queryset = Conversation.objects.all().prefetch_related('participants', 'messages')
    serializer_class = ConversationSerializer
    permission_classes = [permissions.IsAuthenticated, IsParticipantOfConversation]
    pagination_class = ConversationPagination
    filterset_class = ConversationFilter

    def get_queryset(self):
        """
        Filter conversations to only show those where the user is a participant.
        """
        return Conversation.objects.filter(
            participants=self.request.user
        ).prefetch_related('participants', 'messages').distinct()

    def create(self, request, *args, **kwargs):
        """
        Create a new conversation with specified participants.
        Automatically adds the requesting user as a participant.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        conversation = serializer.save()

        # Ensure the creator is added as a participant
        if self.request.user not in conversation.participants.all():
            conversation.participants.add(self.request.user)

        return Response(
            self.get_serializer(conversation).data,
            status=status.HTTP_201_CREATED
        )

    @action(detail=True, methods=['post'])
    def add_message(self, request, pk=None):
        """
        Add a message to an existing conversation.
        Only participants can add messages.
        """
        conversation = self.get_object()

        # Automatically set sender to authenticated user
        message_data = {
            'conversation': conversation.conversation_id,
            'sender': self.request.user.user_id,
            'message_body': request.data.get('message_body')
        }

        serializer = MessageSerializer(data=message_data)
        serializer.is_valid(raise_exception=True)
        message = serializer.save()

        return Response(
            MessageSerializer(message).data,
            status=status.HTTP_201_CREATED
        )


@method_decorator(cache_page(60), name='list')  # Cache list view for 60 seconds
class MessageViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing messages.
    Provides endpoints to list, create, and retrieve messages.
    Only participants can view/create messages. Only senders can edit/delete their messages.
    Supports pagination (20 per page) and filtering by conversation, sender, and date range.

    Caching:
        - List view is cached for 60 seconds for performance optimization
    """
    queryset = Message.objects.all().select_related('sender', 'conversation')
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated, IsParticipantOfConversation, IsMessageSender]
    pagination_class = MessagePagination
    filterset_class = MessageFilter

    def get_queryset(self):
        """
        Filter messages to only show those in conversations where the user is a participant.
        Also supports filtering by conversation ID.
        """
        # Base queryset: only messages from conversations where user is a participant
        queryset = Message.objects.filter(
            conversation__participants=self.request.user
        ).select_related('sender', 'conversation').distinct()

        # Optional filter by conversation_id
        conversation_id = self.request.query_params.get('conversation', None)
        if conversation_id:
            queryset = queryset.filter(conversation__conversation_id=conversation_id)

        return queryset

    def create(self, request, *args, **kwargs):
        """
        Create a new message in a conversation.
        Automatically sets the sender to the authenticated user.
        """
        # Override sender to be the authenticated user for security
        data = request.data.copy()
        data['sender_id'] = str(self.request.user.user_id)

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)

        # Verify user is a participant in the conversation
        conversation_id = serializer.validated_data.get('conversation').conversation_id
        conversation = Conversation.objects.filter(
            conversation_id=conversation_id,
            participants=self.request.user
        ).first()

        if not conversation:
            return Response(
                {'error': 'You are not a participant in this conversation.'},
                status=status.HTTP_403_FORBIDDEN
            )

        message = serializer.save()
        return Response(
            self.get_serializer(message).data,
            status=status.HTTP_201_CREATED
        )

@api_view(['DELETE'])
@perm_decorator([permissions.IsAuthenticated])
def delete_user(request):
    """
    Delete the authenticated user's account.

    This view allows a user to delete their own account.
    All related data (messages, notifications, message histories) will be
    automatically deleted via CASCADE foreign keys and post_delete signals.

    Method: DELETE
    Authentication: Required
    Permissions: User can only delete their own account

    Returns:
        200 OK: User successfully deleted
        403 Forbidden: User trying to delete someone else's account
    """
    user = request.user

    # Security check: Ensure user is deleting their own account
    if not user.is_authenticated:
        return Response(
            {'error': 'Authentication required'},
            status=status.HTTP_401_UNAUTHORIZED
        )

    # Store user info for response before deletion
    user_id = str(user.user_id)
    username = user.username
    email = user.email

    # Delete the user (this triggers post_delete signal)
    user.delete()

    return Response(
        {
            'message': 'User account deleted successfully',
            'deleted_user': {
                'user_id': user_id,
                'username': username,
                'email': email
            }
        },
        status=status.HTTP_200_OK
    )
