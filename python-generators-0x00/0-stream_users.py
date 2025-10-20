#!/usr/bin/env python3
"""
Generator module to stream users from the database one by one.
Uses Python yield keyword for memory-efficient data streaming.
"""

import psycopg2
from psycopg2.extras import RealDictCursor


def stream_users():
    """
    Generator function that streams rows from user_data table one by one.

    Yields:
        dict: User data dictionary containing user_id, name, email, and age

    Note:
        This function uses only one loop as required and leverages
        the yield keyword to create a memory-efficient generator.
    """
    try:
        # Connect to the ALX_prodev database
        connection = psycopg2.connect(
            host="localhost",
            user="postgres",
            password="postgres",
            database="alx_prodev"
        )

        # Use RealDictCursor to get results as dictionaries
        cursor = connection.cursor(cursor_factory=RealDictCursor)

        # Execute query to fetch all users
        cursor.execute("SELECT * FROM user_data")

        # Yield one row at a time using generator
        for row in cursor:
            yield dict(row)

        # Clean up resources
        cursor.close()
        connection.close()

    except psycopg2.Error as e:
        print(f"Database error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")


if __name__ == "__main__":
    # Test the generator
    from itertools import islice

    print("Streaming first 6 users:")
    for user in islice(stream_users(), 6):
        print(user)
