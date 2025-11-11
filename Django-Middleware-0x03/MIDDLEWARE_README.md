# Django Middleware Project (Django-Middleware-0x03)

A Django messaging application implementing custom middleware for request logging, time-based access control, rate limiting, and role-based permissions.

## Project Overview

This project demonstrates the implementation of custom middleware in Django to handle cross-cutting concerns such as:
- Request/response logging
- Time-based access restrictions
- Rate limiting and abuse prevention
- Role-based access control

## Custom Middleware Implemented

### 1. RequestLoggingMiddleware
**Purpose**: Logs all incoming requests for auditing and debugging

**Features**:
- Logs timestamp, user, and request path
- Writes to `requests.log` file
- Tracks both authenticated and anonymous users

**Log Format**:
```
2025-11-11 01:30:45.123456 - User: john_doe - Path: /api/messages/
2025-11-11 01:30:50.654321 - User: Anonymous - Path: /api/auth/login/
```

### 2. RestrictAccessByTimeMiddleware
**Purpose**: Restricts access to the messaging app during specific hours

**Features**:
- Allowed hours: 9:00 AM - 6:00 PM
- Returns 403 Forbidden outside allowed hours
- Provides informative error messages with current time

**Response Example** (outside hours):
```json
{
  "error": "Access denied",
  "message": "Chat access is only allowed between 09:00 AM and 06:00 PM",
  "current_time": "08:30 PM"
}
```

### 3. OffensiveLanguageMiddleware (Rate Limiting)
**Purpose**: Prevents message spam by limiting requests per IP address

**Features**:
- Limit: 5 POST requests per minute per IP
- Tracks requests in memory by IP address
- Thread-safe implementation
- Automatic cleanup of old request times

**Response Example** (rate limit exceeded):
```json
{
  "error": "Rate limit exceeded",
  "message": "You can only send 5 messages per minute",
  "retry_after": "60 seconds"
}
```

### 4. RolePermissionMiddleware
**Purpose**: Enforces role-based access control

**Features**:
- Only allows 'admin' and 'moderator' roles
- Returns 403 for unauthorized roles
- Exempt paths for login/registration
- Provides clear permission error messages

**Response Example** (insufficient permissions):
```json
{
  "error": "Permission denied",
  "message": "Access restricted to admin or moderator only",
  "your_role": "guest"
}
```

**Exempt Paths** (no role check):
- `/api/auth/login/`
- `/api/auth/register/`
- `/api/auth/token/refresh/`
- `/admin/login/`

## Installation & Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run Migrations
```bash
python manage.py migrate
```

### 3. Create Admin User
```bash
python manage.py createsuperuser
# Set role to 'admin' in database or Django admin
```

### 4. Start Server
```bash
python manage.py runserver
```

## Middleware Configuration

Middleware order in `settings.py` matters! Current order:

```python
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # Custom middleware
    'chats.middleware.RequestLoggingMiddleware',        # First: Log everything
    'chats.middleware.RestrictAccessByTimeMiddleware',  # Second: Time check
    'chats.middleware.RolePermissionMiddleware',        # Third: Role check
    'chats.middleware.OffensiveLanguageMiddleware',     # Fourth: Rate limit
]
```

## Testing the Middleware

### Test 1: Request Logging
```bash
# Make any request
curl http://localhost:8000/api/conversations/

# Check logs
tail requests.log
```

### Test 2: Time Restriction
```bash
# If outside 9 AM - 6 PM
curl http://localhost:8000/api/messages/
# Should return 403 Forbidden
```

### Test 3: Rate Limiting
```bash
# Send 6 POST requests quickly
for i in {1..6}; do
  curl -X POST http://localhost:8000/api/messages/ \
    -H "Authorization: Bearer <token>" \
    -H "Content-Type: application/json" \
    -d '{"conversation": "uuid", "message_body": "Test"}'
done
# 6th request should return 429 Too Many Requests
```

### Test 4: Role Permissions
```bash
# Login as user with 'guest' role
curl -X GET http://localhost:8000/api/conversations/ \
  -H "Authorization: Bearer <token>"
# Should return 403 Permission Denied
```

## Project Structure

```
Django-Middleware-0x03/
├── chats/
│   ├── middleware.py           # All custom middleware classes
│   ├── models.py              # User, Conversation, Message
│   ├── views.py               # API ViewSets
│   ├── permissions.py         # Custom DRF permissions
│   └── ...
├── messaging_app/
│   ├── settings.py            # Middleware configuration
│   └── urls.py                # URL routing
├── requests.log               # Auto-generated log file
├── requirements.txt
└── README.md
```

## Middleware Best Practices Followed

✅ **Small and Focused**: Each middleware has a single responsibility
✅ **Proper Chaining**: All middleware call `get_response(request)` appropriately
✅ **Performance**: Minimal database queries, efficient in-memory tracking
✅ **Thread Safety**: Rate limiter uses locks for concurrent requests
✅ **Clear Errors**: Informative JSON error responses
✅ **Documentation**: Comprehensive docstrings and comments

## API Endpoints

All endpoints from the messaging app are available:

### Authentication
- `POST /api/auth/register/` - Register new user
- `POST /api/auth/login/` - Login with JWT
- `POST /api/auth/logout/` - Logout
- `POST /api/auth/token/refresh/` - Refresh token

### Conversations
- `GET /api/conversations/` - List conversations
- `POST /api/conversations/` - Create conversation
- `GET /api/conversations/{id}/` - Get conversation

### Messages
- `GET /api/messages/` - List messages (paginated, 20/page)
- `POST /api/messages/` - Send message
- `GET /api/messages/{id}/` - Get message

## Debugging & Troubleshooting

### Check Middleware Order
```python
# In Django shell
from django.conf import settings
print(settings.MIDDLEWARE)
```

### View Request Logs
```bash
tail -f requests.log
```

### Test Without Middleware
Comment out middleware in `settings.py` to isolate issues.

### Common Issues

**403 Forbidden outside hours**:
- Normal behavior if outside 9 AM - 6 PM
- Modify `RestrictAccessByTimeMiddleware.start_time` and `end_time` if needed

**429 Rate Limit**:
- Wait 1 minute before retrying
- Or restart server to clear in-memory rate limit data

**401/403 Permission Denied**:
- Ensure user role is 'admin' or 'moderator'
- Update user role in Django admin or database

## Security Considerations

- **Rate Limiting**: Prevents DoS attacks and spam
- **Role Checking**: Ensures only authorized users access resources
- **Request Logging**: Provides audit trail for security analysis
- **Time Restrictions**: Additional layer of access control

## Future Enhancements

Potential improvements:
- [ ] Persistent rate limit storage (Redis/database)
- [ ] Configurable time windows via environment variables
- [ ] IP whitelist/blacklist functionality
- [ ] More granular role permissions
- [ ] Real-time monitoring dashboard
- [ ] Alert system for suspicious activity

## License

This project is part of the ALX Backend Python curriculum.

## Contributing

For questions or issues, please refer to the ALX platform or project documentation.
