#!/usr/bin/env python3
"""
Task 4: Using Decorators to Cache Database Queries
Create a decorator that caches query results to avoid redundant database calls.
"""

import time
import sqlite3
import functools


# Global cache dictionary
query_cache = {}


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


def cache_query(func):
    """
    Decorator that caches query results based on the SQL query string.
    Subsequent calls with the same query return cached results.

    Args:
        func: The function to be decorated

    Returns:
        The wrapper function that manages query caching
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Extract the query from arguments
        query = kwargs.get('query') or (args[1] if len(args) > 1 else None)

        # Check if result is in cache
        if query in query_cache:
            print(f"Using cached result for query: {query}")
            return query_cache[query]

        # Execute the function if not cached
        print(f"Executing query and caching result: {query}")
        result = func(*args, **kwargs)

        # Store result in cache
        query_cache[query] = result

        return result

    return wrapper


@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    """
    Fetch users from the database with automatic caching.

    Args:
        conn: Database connection (provided by decorator)
        query: SQL query string

    Returns:
        List of user records
    """
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()


if __name__ == "__main__":
    # First call will cache the result
    print("=" * 50)
    print("First call - will execute query and cache result:")
    users = fetch_users_with_cache(query="SELECT * FROM users")
    print(f"Fetched {len(users)} users\n")

    # Second call will use the cached result
    print("=" * 50)
    print("Second call - will use cached result:")
    users_again = fetch_users_with_cache(query="SELECT * FROM users")
    print(f"Fetched {len(users_again)} users (from cache)")