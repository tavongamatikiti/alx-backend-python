#!/usr/bin/env python3
"""
Task 0: Custom Class-Based Context Manager for Database Connection
Create a class-based context manager to handle opening and closing database connections automatically.
"""

import sqlite3


class DatabaseConnection:
    """
    A context manager for handling SQLite database connections.

    This class implements the context manager protocol using __enter__ and __exit__ methods
    to automatically manage database connection lifecycle.
    """

    def __init__(self, db_name):
        """
        Initialize the DatabaseConnection context manager.

        Args:
            db_name (str): The name/path of the SQLite database file
        """
        self.db_name = db_name
        self.connection = None

    def __enter__(self):
        """
        Enter the context manager - opens the database connection.

        Returns:
            sqlite3.Connection: The database connection object
        """
        self.connection = sqlite3.connect(self.db_name)
        return self.connection

    def __exit__(self, exc_type, exc_value, traceback):
        """
        Exit the context manager - closes the database connection.

        Args:
            exc_type: Exception type if an exception occurred
            exc_value: Exception value if an exception occurred
            traceback: Traceback if an exception occurred

        Returns:
            bool: False to propagate any exceptions that occurred
        """
        if self.connection:
            self.connection.close()
        return False


if __name__ == "__main__":
    # Use the context manager with the 'with' statement
    with DatabaseConnection('users.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        results = cursor.fetchall()

        print("Users in database:")
        print("-" * 60)
        for row in results:
            print(f"ID: {row[0]}, Name: {row[1]}, Email: {row[2]}, Age: {row[3]}")