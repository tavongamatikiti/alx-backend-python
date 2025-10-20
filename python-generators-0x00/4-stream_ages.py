#!/usr/bin/env python3
"""
Memory-efficient aggregation module using generators.
Calculates average age without loading entire dataset into memory.
"""

import psycopg2
from psycopg2.extras import RealDictCursor


def stream_user_ages():
    """
    Generator function that yields user ages one by one from the database.

    Yields:
        int/float: Age of each user

    Note:
        This generator allows memory-efficient processing of ages
        without loading all data into memory at once.
    """
    try:
        # Connect to the ALX_prodev database
        connection = psycopg2.connect(
            host="localhost",
            user="postgres",
            password="postgres",
            database="alx_prodev"
        )

        cursor = connection.cursor()

        # Fetch only age column to minimize memory usage
        cursor.execute("SELECT age FROM user_data")

        # Loop 1: Yield ages one by one
        for row in cursor:
            yield row[0]

        # Clean up resources
        cursor.close()
        connection.close()

    except psycopg2.Error as e:
        print(f"Database error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")


def calculate_average_age():
    """
    Calculates the average age of all users using a generator.

    Returns:
        float: Average age of users

    Note:
        Uses maximum of 2 loops as required:
        - Loop 1: In stream_user_ages() generator
        - Loop 2: In this function to accumulate sum and count
        Does not use SQL AVERAGE function as required.
    """
    total_age = 0
    count = 0

    # Loop 2: Iterate over ages from generator
    for age in stream_user_ages():
        total_age += age
        count += 1

    # Calculate and return average
    if count > 0:
        return total_age / count
    return 0


if __name__ == "__main__":
    # Calculate and print average age
    average_age = calculate_average_age()
    print(f"Average age of users: {average_age:.2f}")
