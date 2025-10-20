#!/usr/bin/env python3
"""
Task 3: Using Decorators to Retry Database Queries
Create a decorator that retries database operations if they fail due to transient errors.
"""

import time
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


def retry_on_failure(retries=3, delay=2):
    """
    Decorator that retries a function if it raises an exception.

    Args:
        retries: Number of retry attempts (default: 3)
        delay: Delay in seconds between retries (default: 2)

    Returns:
        The decorator function
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempt = 0
            last_exception = None

            while attempt < retries:
                try:
                    # Attempt to execute the function
                    result = func(*args, **kwargs)
                    if attempt > 0:
                        print(f"Success on attempt {attempt + 1}")
                    return result

                except Exception as e:
                    attempt += 1
                    last_exception = e
                    print(f"Attempt {attempt} failed: {e}")

                    if attempt < retries:
                        print(f"Retrying in {delay} seconds...")
                        time.sleep(delay)
                    else:
                        print(f"All {retries} attempts failed")

            # If all retries failed, raise the last exception
            raise last_exception

        return wrapper
    return decorator


@with_db_connection
@retry_on_failure(retries=3, delay=1)
def fetch_users_with_retry(conn):
    """
    Fetch all users from the database with automatic retry on failure.

    Args:
        conn: Database connection (provided by decorator)

    Returns:
        List of user records
    """
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()


if __name__ == "__main__":
    # Attempt to fetch users with automatic retry on failure
    try:
        users = fetch_users_with_retry()
        print(f"Successfully fetched {len(users)} users")
    except Exception as e:
        print(f"Failed to fetch users after retries: {e}")