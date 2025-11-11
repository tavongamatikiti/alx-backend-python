"""
Serializers for the messaging application.
Handles serialization of User, Conversation, and Message models.
"""

from rest_framework import serializers
from .models import User, Conversation, Message


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the User model.
    """
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'user_id',
            'username',
            'first_name',
            'last_name',
            'full_name',
            'email',
            'phone_number',
            'role',
            'created_at'
        ]
        read_only_fields = ['user_id', 'created_at']

    def get_full_name(self, obj):
        """
        Returns the user's full name.
        """
        return f"{obj.first_name} {obj.last_name}".strip()


class MessageSerializer(serializers.ModelSerializer):
    """
    Serializer for the Message model.
    Includes nested sender information.
    """
    sender = UserSerializer(read_only=True)
    sender_id = serializers.UUIDField(write_only=True)
    message_preview = serializers.CharField(read_only=True, max_length=50)

    class Meta:
        model = Message
        fields = [
            'message_id',
            'sender',
            'sender_id',
            'conversation',
            'message_body',
            'message_preview',
            'sent_at'
        ]
        read_only_fields = ['message_id', 'sent_at']

    def validate_message_body(self, value):
        """
        Validates that message_body is not empty.
        """
        if not value or not value.strip():
            raise serializers.ValidationError("Message body cannot be empty.")
        return value

    def to_representation(self, instance):
        """
        Add a preview field to the representation.
        """
        representation = super().to_representation(instance)
        representation['message_preview'] = instance.message_body[:50]
        return representation


class ConversationSerializer(serializers.ModelSerializer):
    """
    Serializer for the Conversation model.
    Includes nested messages and participants.
    """
    participants = UserSerializer(many=True, read_only=True)
    participant_ids = serializers.ListField(
        child=serializers.UUIDField(),
        write_only=True
    )
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Conversation
        fields = [
            'conversation_id',
            'participants',
            'participant_ids',
            'messages',
            'created_at'
        ]
        read_only_fields = ['conversation_id', 'created_at']

    def create(self, validated_data):
        """
        Create a new conversation with participants.
        """
        participant_ids = validated_data.pop('participant_ids')
        conversation = Conversation.objects.create()
        conversation.participants.set(
            User.objects.filter(user_id__in=participant_ids)
        )
        return conversation