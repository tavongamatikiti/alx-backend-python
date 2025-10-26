# Django Messaging App

A RESTful API messaging application built with Django and Django REST Framework, featuring user management, conversations, and real-time messaging capabilities.

## Project Overview

This project demonstrates the complete lifecycle of designing and implementing robust RESTful APIs using Django. It includes proper data modeling, database relationships, clean URL routing, and follows Django's best practices for maintainable and production-ready codebases.

## Features

- **User Management**: Custom user model with roles (guest, host, admin)
- **Conversations**: Group or one-on-one chat functionality
- **Messaging**: Send and receive messages within conversations
- **RESTful API**: Clean, well-structured API endpoints
- **UUID Primary Keys**: Enhanced security and scalability
- **Proper Indexing**: Optimized database queries
- **Admin Interface**: Full Django admin integration

## Tech Stack

- **Django 5.2.7**: Backend framework
- **Django REST Framework 3.16.1**: API development
- **SQLite**: Database (development)
- **Python 3.13**: Programming language

## Project Structure

```
messaging_app/
├── messaging_app/          # Project configuration
│   ├── settings.py         # Settings and configuration
│   ├── urls.py             # Main URL routing
│   └── wsgi.py             # WSGI application
├── chats/                  # Main application
│   ├── models.py           # Data models (User, Conversation, Message)
│   ├── serializers.py      # DRF serializers
│   ├── views.py            # ViewSets for API endpoints
│   ├── urls.py             # App-specific URL routing
│   ├── admin.py            # Admin interface configuration
│   └── migrations/         # Database migrations
└── manage.py               # Django management script
```

## Data Models

### User Model
- Extends Django's AbstractUser
- UUID primary key
- Fields: username, email, first_name, last_name, phone_number, role
- Roles: guest, host, admin

### Conversation Model
- UUID primary key
- Many-to-many relationship with Users (participants)
- Tracks conversation creation time

### Message Model
- UUID primary key
- Foreign key to User (sender)
- Foreign key to Conversation
- Message body and timestamp

## Installation & Setup

### 1. Install Dependencies

```bash
pip install django djangorestframework
```

### 2. Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 3. Create Superuser (Optional)

```bash
python manage.py createsuperuser
```

### 4. Run Development Server

```bash
python manage.py runserver
```

The server will start at `http://127.0.0.1:8000/`

## API Endpoints

### Base URL: `/api/`

#### Users
- `GET /api/users/` - List all users
- `POST /api/users/` - Create a new user
- `GET /api/users/{user_id}/` - Retrieve user details
- `PUT /api/users/{user_id}/` - Update user
- `DELETE /api/users/{user_id}/` - Delete user

#### Conversations
- `GET /api/conversations/` - List all conversations
- `POST /api/conversations/` - Create a new conversation
- `GET /api/conversations/{conversation_id}/` - Retrieve conversation with messages
- `POST /api/conversations/{conversation_id}/add_message/` - Add message to conversation

#### Messages
- `GET /api/messages/` - List all messages
- `GET /api/messages/?conversation={conversation_id}` - Filter messages by conversation
- `POST /api/messages/` - Send a new message
- `GET /api/messages/{message_id}/` - Retrieve message details

## API Usage Examples

### Create a User

```bash
curl -X POST http://127.0.0.1:8000/api/users/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "johndoe",
    "email": "john@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "password": "securepassword",
    "role": "guest"
  }'
```

### Create a Conversation

```bash
curl -X POST http://127.0.0.1:8000/api/conversations/ \
  -H "Content-Type: application/json" \
  -d '{
    "participant_ids": ["user-uuid-1", "user-uuid-2"]
  }'
```

### Send a Message

```bash
curl -X POST http://127.0.0.1:8000/api/messages/ \
  -H "Content-Type: application/json" \
  -d '{
    "sender_id": "user-uuid-1",
    "conversation": "conversation-uuid",
    "message_body": "Hello, how are you?"
  }'
```

## Database Schema

### Relationships
- User ↔ Conversation: Many-to-Many (participants)
- User → Message: One-to-Many (sent messages)
- Conversation → Message: One-to-Many (conversation messages)

### Indexes
- Primary keys (all tables)
- Email (users)
- Conversation + sent_at (messages)
- Sender (messages)

## Admin Interface

Access the Django admin at `http://127.0.0.1:8000/admin/`

Features:
- User management with role filtering
- Conversation management with participant selection
- Message management with search and filtering

## Best Practices Implemented

- ✅ Modular app structure
- ✅ Custom user model (AUTH_USER_MODEL)
- ✅ UUID primary keys for security
- ✅ Proper database indexing
- ✅ REST API conventions
- ✅ Nested serializers for relationships
- ✅ ViewSets for DRY code
- ✅ DefaultRouter for automatic URL generation
- ✅ Comprehensive documentation

## Testing

```bash
# Run tests
python manage.py test

# Check for issues
python manage.py check
```

## Future Enhancements

- Add authentication (JWT/Token-based)
- Implement WebSocket support for real-time messaging
- Add message read receipts
- Implement file attachments
- Add conversation typing indicators
- Implement message search functionality

## License

This project is part of the ALX Backend Python curriculum.

## Author

ALX Backend Python Program