"""
Custom middleware for the Django messaging app.

This module contains middleware classes for:
- Request logging
- Time-based access restriction
- Rate limiting (offensive language prevention)
- Role-based permission enforcement
"""

import logging
from datetime import datetime, time
from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin
from collections import defaultdict
from threading import Lock

# Configure logging
logging.basicConfig(
    filename='requests.log',
    level=logging.INFO,
    format='%(message)s'
)
logger = logging.getLogger(__name__)


class RequestLoggingMiddleware:
    """
    Middleware to log each user's request including timestamp, user, and request path.

    Logs format: "{timestamp} - User: {user} - Path: {path}"
    Logs are written to requests.log file.
    """

    def __init__(self, get_response):
        """Initialize the middleware with the get_response callable."""
        self.get_response = get_response

    def __call__(self, request):
        """
        Process the request and log information.

        Args:
            request: The HTTP request object

        Returns:
            The HTTP response object
        """
        # Get user information
        user = request.user if request.user.is_authenticated else 'Anonymous'

        # Log the request
        log_message = f"{datetime.now()} - User: {user} - Path: {request.path}"
        logger.info(log_message)

        # Process the request
        response = self.get_response(request)

        return response


class RestrictAccessByTimeMiddleware:
    """
    Middleware to restrict access to the messaging app during certain hours.

    Access is denied outside of 9:00 AM - 6:00 PM.
    Returns 403 Forbidden during restricted hours.
    """

    def __init__(self, get_response):
        """Initialize the middleware with the get_response callable."""
        self.get_response = get_response
        self.start_time = time(9, 0)  # 9:00 AM
        self.end_time = time(18, 0)   # 6:00 PM

    def __call__(self, request):
        """
        Check current time and restrict access if outside allowed hours.

        Args:
            request: The HTTP request object

        Returns:
            403 Forbidden response or the normal response
        """
        # Get current server time
        current_time = datetime.now().time()

        # Check if current time is within allowed hours
        if not (self.start_time <= current_time <= self.end_time):
            return JsonResponse(
                {
                    'error': 'Access denied',
                    'message': f'Chat access is only allowed between {self.start_time.strftime("%I:%M %p")} and {self.end_time.strftime("%I:%M %p")}',
                    'current_time': current_time.strftime("%I:%M %p")
                },
                status=403
            )

        # Process the request if within allowed hours
        response = self.get_response(request)

        return response


class OffensiveLanguageMiddleware:
    """
    Middleware to implement rate limiting for chat messages.

    Limits the number of POST requests (messages) per IP address to 5 per minute.
    Tracks requests in memory and blocks excess requests.
    """

    # Class-level storage for IP tracking (shared across instances)
    ip_request_times = defaultdict(list)
    lock = Lock()

    def __init__(self, get_response):
        """Initialize the middleware with the get_response callable."""
        self.get_response = get_response
        self.max_requests = 5  # Maximum requests per time window
        self.time_window = 60  # Time window in seconds (1 minute)

    def __call__(self, request):
        """
        Track POST requests by IP and enforce rate limiting.

        Args:
            request: The HTTP request object

        Returns:
            429 Too Many Requests response or the normal response
        """
        # Only apply rate limiting to POST requests
        if request.method == 'POST':
            # Get client IP address
            ip_address = self.get_client_ip(request)
            current_time = datetime.now()

            with self.lock:
                # Get request times for this IP
                request_times = self.ip_request_times[ip_address]

                # Remove old requests outside the time window
                cutoff_time = current_time.timestamp() - self.time_window
                request_times[:] = [
                    req_time for req_time in request_times
                    if req_time > cutoff_time
                ]

                # Check if limit is exceeded
                if len(request_times) >= self.max_requests:
                    return JsonResponse(
                        {
                            'error': 'Rate limit exceeded',
                            'message': f'You can only send {self.max_requests} messages per minute',
                            'retry_after': f'{self.time_window} seconds'
                        },
                        status=429
                    )

                # Add current request time
                request_times.append(current_time.timestamp())

        # Process the request
        response = self.get_response(request)

        return response

    def get_client_ip(self, request):
        """
        Extract the client's IP address from the request.

        Args:
            request: The HTTP request object

        Returns:
            The client's IP address as a string
        """
        # Try to get real IP if behind proxy
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


class RolePermissionMiddleware:
    """
    Middleware to enforce role-based access control.

    Only allows access for users with 'admin' or 'moderator' roles.
    Returns 403 Forbidden for users without proper roles.
    """

    def __init__(self, get_response):
        """Initialize the middleware with the get_response callable."""
        self.get_response = get_response
        self.allowed_roles = ['admin', 'moderator']
        # Paths that don't require role check
        self.exempt_paths = [
            '/api/auth/login/',
            '/api/auth/register/',
            '/api/auth/token/refresh/',
            '/admin/login/',
        ]

    def __call__(self, request):
        """
        Check user role and restrict access if not admin or moderator.

        Args:
            request: The HTTP request object

        Returns:
            403 Forbidden response or the normal response
        """
        # Skip role check for exempt paths
        if any(request.path.startswith(path) for path in self.exempt_paths):
            return self.get_response(request)

        # Check if user is authenticated
        if not request.user.is_authenticated:
            return JsonResponse(
                {
                    'error': 'Authentication required',
                    'message': 'You must be logged in to access this resource'
                },
                status=401
            )

        # Check user role
        user_role = getattr(request.user, 'role', None)

        if user_role not in self.allowed_roles:
            return JsonResponse(
                {
                    'error': 'Permission denied',
                    'message': f'Access restricted to {" or ".join(self.allowed_roles)} only',
                    'your_role': user_role or 'none'
                },
                status=403
            )

        # Process the request if role is allowed
        response = self.get_response(request)

        return response
