#!/usr/bin/env python3
"""
Task 1: Handle Database Connections with a Decorator
Create a decorator that automatically handles opening and closing database connections.
"""

import sqlite3
import functools


def with_db_connection(func):
    """
    Decorator that handles database connection automatically.
    Opens connection, passes it to the function, and closes it afterward.

    Args:
        func: The function to be decorated

    Returns:
        The wrapper function that manages database connections
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Open database connection
        conn = sqlite3.connect('users.db')

        try:
            # Pass connection to the decorated function
            result = func(conn, *args, **kwargs)
            return result
        finally:
            # Always close the connection
            conn.close()

    return wrapper


@with_db_connection
def get_user_by_id(conn, user_id):
    """
    Get a user by their ID.

    Args:
        conn: Database connection (provided by decorator)
        user_id: The ID of the user to fetch

    Returns:
        User record tuple
    """
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    return cursor.fetchone()


if __name__ == "__main__":
    # Fetch user by ID with automatic connection handling
    user = get_user_by_id(user_id=1)
    print(user)