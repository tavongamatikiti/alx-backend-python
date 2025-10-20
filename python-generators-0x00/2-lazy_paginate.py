#!/usr/bin/env python3
"""
Lazy pagination module using generators.
Simulates fetching paginated data, loading each page only when needed.
"""

import psycopg2
from psycopg2.extras import RealDictCursor


def paginate_users(page_size, offset):
    """
    Fetches a page of users from the database at a specific offset.

    Args:
        page_size (int): Number of users to fetch per page
        offset (int): Starting position for the page

    Returns:
        list: List of user dictionaries for the requested page
    """
    try:
        connection = psycopg2.connect(
            host="localhost",
            user="postgres",
            password="postgres",
            database="alx_prodev"
        )

        cursor = connection.cursor(cursor_factory=RealDictCursor)

        # Fetch page with LIMIT and OFFSET
        cursor.execute(
            f"SELECT * FROM user_data LIMIT {page_size} OFFSET {offset}"
        )

        rows = cursor.fetchall()

        cursor.close()
        connection.close()

        return [dict(row) for row in rows]

    except psycopg2.Error as e:
        print(f"Database error: {e}")
        return []
    except Exception as e:
        print(f"Unexpected error: {e}")
        return []


def lazy_pagination(page_size):
    """
    Generator function that lazily loads paginated data.

    Args:
        page_size (int): Number of users per page

    Yields:
        list: Page of user data

    Note:
        Only fetches the next page when needed, implementing true lazy loading.
        Uses only one loop as required.
    """
    offset = 0

    # Single loop to iterate through pages
    while True:
        # Fetch the next page
        page = paginate_users(page_size, offset)

        # If no more data, stop iteration
        if not page:
            break

        # Yield the current page
        yield page

        # Move to next page
        offset += page_size


if __name__ == "__main__":
    # Test lazy pagination
    import sys

    try:
        for page in lazy_pagination(100):
            for user in page:
                print(user)
    except BrokenPipeError:
        sys.stderr.close()
