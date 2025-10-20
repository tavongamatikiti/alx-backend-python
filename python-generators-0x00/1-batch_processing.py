#!/usr/bin/env python3
"""
Batch processing module using generators to fetch and process data in batches.
Demonstrates memory-efficient batch processing with filtering.
"""

import psycopg2
from psycopg2.extras import RealDictCursor


def stream_users_in_batches(batch_size):
    """
    Generator function that fetches rows from user_data table in batches.

    Args:
        batch_size (int): Number of rows to fetch in each batch

    Yields:
        list: Batch of user dictionaries

    Note:
        Uses yield to create a memory-efficient generator that processes
        data in manageable chunks.
    """
    try:
        # Connect to the ALX_prodev database
        connection = psycopg2.connect(
            host="localhost",
            user="postgres",
            password="postgres",
            database="alx_prodev"
        )

        cursor = connection.cursor(cursor_factory=RealDictCursor)

        # Use server-side cursor for large datasets
        cursor.execute("SELECT * FROM user_data")

        # Fetch and yield data in batches
        while True:
            batch = cursor.fetchmany(batch_size)
            if not batch:
                break
            yield [dict(row) for row in batch]

        # Clean up resources
        cursor.close()
        connection.close()

    except psycopg2.Error as e:
        print(f"Database error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")


def batch_processing(batch_size):
    """
    Processes each batch to filter users over the age of 25.

    Args:
        batch_size (int): Number of rows to process in each batch

    Note:
        Uses maximum of 3 loops as required:
        - Loop 1: Iterate over batches from stream_users_in_batches
        - Loop 2: Iterate over users in each batch
        - Loop 3: (Implicit in generator) Fetching batches
    """
    # Loop 1: Iterate over batches
    for batch in stream_users_in_batches(batch_size):
        # Loop 2: Iterate over users in the batch
        for user in batch:
            # Filter users over age 25
            if user['age'] > 25:
                print(user)


if __name__ == "__main__":
    # Test batch processing with batch size of 50
    import sys
    try:
        batch_processing(50)
    except BrokenPipeError:
        sys.stderr.close()
