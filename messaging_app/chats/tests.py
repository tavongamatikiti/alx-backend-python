from django.test import TestCase
from django.contrib.auth import get_user_model

User = get_user_model()


class BasicTestCase(TestCase):
    """Basic test case to ensure CI/CD pipeline runs successfully."""

    def test_basic_addition(self):
        """Test basic arithmetic to verify test framework works."""
        self.assertEqual(1 + 1, 2)

    def test_user_creation(self):
        """Test that user can be created."""
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.email, 'test@example.com')
        self.assertTrue(user.check_password('testpass123'))

    def test_user_string_representation(self):
        """Test user string representation."""
        user = User.objects.create_user(
            username='testuser2',
            email='test2@example.com'
        )
        self.assertEqual(str(user), 'testuser2')
