# Django Messaging App - Authentication & Permissions

A fully-featured messaging application built with Django REST Framework, implementing JWT authentication, custom permissions, pagination, and filtering.

## Features Implemented

### 1. JWT Authentication
- User registration with validation
- Login with username or email
- Token refresh mechanism
- Logout with token blacklisting
- User profile management

### 2. Custom Permissions
- `IsParticipantOfConversation`: Ensures only conversation participants can view/send messages
- `IsMessageSender`: Allows only message senders to edit/delete their messages
- Role-based access control throughout the API

### 3. Pagination
- Messages: 20 per page
- Conversations: 10 per page
- Customizable page sizes

### 4. Filtering
- **Messages**: Filter by conversation, sender, date range, message content
- **Conversations**: Filter by participant, creation date range

## Project Structure

```
messaging_app/
├── chats/
│   ├── auth.py                 # Authentication views and serializers
│   ├── permissions.py          # Custom permission classes
│   ├── pagination.py           # Pagination classes
│   ├── filters.py             # Django-filter classes
│   ├── models.py              # User, Conversation, Message models
│   ├── serializers.py         # DRF serializers
│   ├── views.py               # ViewSets with permissions
│   └── urls.py                # API routes
├── messaging_app/
│   ├── settings.py            # JWT & DRF configuration
│   └── urls.py                # Main URL routing
├── post_man-Collections/
│   └── messaging_app.postman_collection.json
├── requirements.txt
├── manage.py
└── db.sqlite3
```

## Installation

### 1. Set Up Virtual Environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # On macOS/Linux
# or
venv\Scripts\activate     # On Windows
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run Migrations

```bash
python manage.py migrate
```

### 4. Create Superuser (Optional)

```bash
python manage.py createsuperuser
```

### 5. Run Development Server

```bash
python manage.py runserver
```

The API will be available at `http://localhost:8000`

## API Endpoints

### Authentication Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/api/auth/register/` | Register new user | No |
| POST | `/api/auth/login/` | Login and get tokens | No |
| POST | `/api/auth/token/refresh/` | Refresh access token | No |
| POST | `/api/auth/logout/` | Logout (blacklist token) | Yes |
| GET | `/api/auth/profile/` | Get user profile | Yes |
| PUT/PATCH | `/api/auth/profile/` | Update user profile | Yes |

### Conversation Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/conversations/` | List user's conversations | Yes |
| POST | `/api/conversations/` | Create new conversation | Yes |
| GET | `/api/conversations/{id}/` | Get conversation details | Yes |
| PUT/PATCH | `/api/conversations/{id}/` | Update conversation | Yes |
| DELETE | `/api/conversations/{id}/` | Delete conversation | Yes |

### Message Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/messages/` | List messages (paginated, 20/page) | Yes |
| POST | `/api/messages/` | Send new message | Yes |
| GET | `/api/messages/{id}/` | Get message details | Yes |
| PUT/PATCH | `/api/messages/{id}/` | Update message (sender only) | Yes |
| DELETE | `/api/messages/{id}/` | Delete message (sender only) | Yes |

### Filtering Examples

**Filter messages by conversation:**
```
GET /api/messages/?conversation=<conversation_id>
```

**Filter messages by date range:**
```
GET /api/messages/?date_from=2024-01-01&date_to=2024-12-31
```

**Filter messages by sender:**
```
GET /api/messages/?sender=<user_id>
```

**Search messages by content:**
```
GET /api/messages/?message_body=hello
```

**Pagination:**
```
GET /api/messages/?page=2
GET /api/messages/?page_size=50
```

## Usage Examples

### 1. Register a New User

```bash
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "johndoe",
    "email": "john@example.com",
    "password": "SecurePass123!",
    "password_confirm": "SecurePass123!",
    "first_name": "John",
    "last_name": "Doe",
    "role": "guest"
  }'
```

**Response:**
```json
{
  "user": {
    "user_id": "uuid-here",
    "username": "johndoe",
    "email": "john@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "role": "guest"
  },
  "tokens": {
    "refresh": "refresh-token-here",
    "access": "access-token-here"
  },
  "message": "User registered successfully."
}
```

### 2. Login

```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username_or_email": "john@example.com",
    "password": "SecurePass123!"
  }'
```

### 3. Create a Conversation

```bash
curl -X POST http://localhost:8000/api/conversations/ \
  -H "Authorization: Bearer <access-token>" \
  -H "Content-Type: application/json" \
  -d '{
    "participants": ["user-id-1", "user-id-2"]
  }'
```

### 4. Send a Message

```bash
curl -X POST http://localhost:8000/api/messages/ \
  -H "Authorization: Bearer <access-token>" \
  -H "Content-Type: application/json" \
  -d '{
    "conversation": "conversation-id",
    "message_body": "Hello, how are you?"
  }'
```

## Security Features

### 1. JWT Token Configuration
- **Access Token Lifetime**: 1 hour
- **Refresh Token Lifetime**: 7 days
- **Token Rotation**: Enabled
- **Blacklist After Rotation**: Enabled
- **Algorithm**: HS256

### 2. Permission Controls
- All endpoints require authentication by default
- Users can only view conversations they participate in
- Users can only send messages in conversations they're part of
- Only message senders can edit/delete their own messages
- Automatic sender assignment prevents impersonation

### 3. Data Validation
- Email uniqueness enforced
- Password confirmation required
- Minimum password length: 8 characters
- Message body validation
- UUID validation for all IDs

## Testing with Postman

1. Import the collection from `post_man-Collections/messaging_app.postman_collection.json`
2. The collection includes:
   - Authentication tests
   - Conversation creation/listing
   - Message sending/filtering
   - Permission enforcement tests
   - Pagination tests

3. Collection variables are automatically set:
   - `access_token`: Auto-saved after login/register
   - `refresh_token`: Auto-saved after login/register
   - `user_id`: Auto-saved after registration
   - `conversation_id`: Auto-saved after creating conversation
   - `message_id`: Auto-saved after sending message

## Database Models

### User Model
- Extends Django's AbstractUser
- UUID primary key
- Fields: username, email, first_name, last_name, phone_number, role
- Roles: guest, host, admin

### Conversation Model
- UUID primary key
- Many-to-many relationship with User (participants)
- Timestamps: created_at

### Message Model
- UUID primary key
- Foreign keys: sender (User), conversation (Conversation)
- Fields: message_body, sent_at
- Indexed for performance

## Key Files Modified/Created

### New Files
- `chats/auth.py` - JWT authentication views
- `chats/permissions.py` - Custom permission classes
- `chats/pagination.py` - Pagination classes
- `chats/filters.py` - Filtering classes
- `post_man-Collections/messaging_app.postman_collection.json` - API tests
- `requirements.txt` - Python dependencies
- `README.md` - This file

### Modified Files
- `messaging_app/settings.py` - JWT & DRF configuration
- `messaging_app/urls.py` - Auth endpoint routing
- `chats/views.py` - Added permissions, pagination, filtering

## Dependencies

```
asgiref==3.10.0
django==5.2.8
django-filter==25.2
djangorestframework==3.16.1
djangorestframework-simplejwt==5.5.1
PyJWT==2.10.1
sqlparse==0.5.3
```

## Requirements Met

✅ **Task 0**: JWT Authentication implemented with login/logout
✅ **Task 1**: Custom permissions (`IsParticipantOfConversation`) applied
✅ **Task 2**: Pagination (20 messages/page) and filtering implemented
✅ **Task 3**: Postman collection created with comprehensive tests
✅ **Task 4**: Ready for manual review

## Additional Features

- Token blacklisting for secure logout
- Automatic sender assignment for security
- Queryset filtering by user participation
- Comprehensive error handling
- API documentation in this README

## Development Notes

- Debug mode is currently ON (change `DEBUG = False` for production)
- SECRET_KEY should be moved to environment variable for production
- Consider adding CORS headers for frontend integration
- Rate limiting can be added for production use

## License

This project is part of the ALX Backend Python curriculum.
