#!/usr/bin/env python3
"""
Task 0: Logging Database Queries
Create a decorator that logs SQL queries executed by any function.
"""

import sqlite3
import functools


def log_queries(func):
    """
    Decorator that logs SQL queries before executing them.

    Args:
        func: The function to be decorated

    Returns:
        The wrapper function that logs queries
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Extract the query from arguments
        # Query can be in args or kwargs
        query = None

        # Check if 'query' is in kwargs
        if 'query' in kwargs:
            query = kwargs['query']
        # Check if query is the first positional argument
        elif args:
            query = args[0]

        # Log the query
        if query:
            print(f"Executing SQL Query: {query}")

        # Execute the original function
        return func(*args, **kwargs)

    return wrapper


@log_queries
def fetch_all_users(query):
    """
    Fetch all users from the database.

    Args:
        query: SQL query string

    Returns:
        List of user records
    """
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results


if __name__ == "__main__":
    # Fetch users while logging the query
    users = fetch_all_users(query="SELECT * FROM users")
    print(f"Fetched {len(users)} users")