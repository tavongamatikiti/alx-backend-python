"""
URL configuration for the chats app.
Uses Django REST Framework DefaultRouter for automatic URL generation.
"""

from django.urls import path, include
from rest_framework import routers
from .views import UserViewSet, ConversationViewSet, MessageViewSet

# Create a router and register viewsets
router = routers.DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'conversations', ConversationViewSet, basename='conversation')
router.register(r'messages', MessageViewSet, basename='message')

urlpatterns = [
    path('', include(router.urls)),
]