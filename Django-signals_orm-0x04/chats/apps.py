from django.apps import AppConfig


class ChatsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'chats'

    def ready(self):
        """
        Import signal handlers when the application is ready.
        This ensures that signals are registered and listening for events.
        """
        import chats.signals  # noqa: F401
