"""
URL configuration for the chats app.
Uses Django REST Framework DefaultRouter for automatic URL generation.
Supports nested routing with NestedDefaultRouter if needed.
"""

from django.urls import path, include
from rest_framework import routers
from .views import UserViewSet, ConversationViewSet, MessageViewSet

# Create a router and register viewsets
# Using routers.DefaultRouter() - can be extended to NestedDefaultRouter for nested resources
router = routers.DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'conversations', ConversationViewSet, basename='conversation')
router.register(r'messages', MessageViewSet, basename='message')

urlpatterns = [
    path('', include(router.urls)),
]