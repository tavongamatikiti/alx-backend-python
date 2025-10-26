#!/usr/bin/env python3
"""
Task 1: Reusable Query Context Manager
Create a reusable context manager that takes a query as input and executes it,
managing both connection and query execution.
"""

import sqlite3


class ExecuteQuery:
    """
    A reusable context manager for executing database queries.

    This class manages both the database connection and query execution,
    automatically handling resource cleanup.
    """

    def __init__(self, db_name, query, params=None):
        """
        Initialize the ExecuteQuery context manager.

        Args:
            db_name (str): The name/path of the SQLite database file
            query (str): The SQL query to execute
            params (tuple, optional): Parameters for the query
        """
        self.db_name = db_name
        self.query = query
        self.params = params if params is not None else ()
        self.connection = None
        self.cursor = None
        self.results = None

    def __enter__(self):
        """
        Enter the context manager - opens connection and executes the query.

        Returns:
            list: The results of the query execution
        """
        self.connection = sqlite3.connect(self.db_name)
        self.cursor = self.connection.cursor()
        self.cursor.execute(self.query, self.params)
        self.results = self.cursor.fetchall()
        return self.results

    def __exit__(self, exc_type, exc_value, traceback):
        """
        Exit the context manager - closes cursor and connection.

        Args:
            exc_type: Exception type if an exception occurred
            exc_value: Exception value if an exception occurred
            traceback: Traceback if an exception occurred

        Returns:
            bool: False to propagate any exceptions that occurred
        """
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
        return False


if __name__ == "__main__":
    # Use the ExecuteQuery context manager
    query = "SELECT * FROM users WHERE age > ?"
    param = (25,)

    with ExecuteQuery('users.db', query, param) as results:
        print("Users older than 25:")
        print("-" * 60)
        for row in results:
            print(f"ID: {row[0]}, Name: {row[1]}, Email: {row[2]}, Age: {row[3]}")