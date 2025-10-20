#!/usr/bin/env python3
"""
Task 2: Transaction Management Decorator
Create a decorator that manages database transactions with automatic commit/rollback.
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


def transactional(func):
    """
    Decorator that manages database transactions.
    Automatically commits on success or rolls back on error.

    Args:
        func: The function to be decorated

    Returns:
        The wrapper function that manages transactions
    """
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        try:
            # Execute the function
            result = func(conn, *args, **kwargs)

            # Commit the transaction on success
            conn.commit()
            print("Transaction committed successfully")

            return result

        except Exception as e:
            # Rollback the transaction on error
            conn.rollback()
            print(f"Transaction rolled back due to error: {e}")
            raise  # Re-raise the exception

    return wrapper


@with_db_connection
@transactional
def update_user_email(conn, user_id, new_email):
    """
    Update a user's email address.

    Args:
        conn: Database connection (provided by decorator)
        user_id: The ID of the user to update
        new_email: The new email address

    Returns:
        None
    """
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET email = ? WHERE id = ?", (new_email, user_id))


if __name__ == "__main__":
    # Update user's email with automatic transaction handling
    update_user_email(user_id=1, new_email='Crawford_Cartwright@hotmail.com')
    print("Email updated successfully")