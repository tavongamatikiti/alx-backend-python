#!/usr/bin/env python3
"""
Database seeding module for ALX_prodev PostgreSQL database.
This module handles database connection, table creation, and data population.
"""

import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import csv
import uuid


def connect_db():
    """
    Connects to the PostgreSQL database server.

    Returns:
        connection: PostgreSQL connection object or None if connection fails
    """
    try:
        connection = psycopg2.connect(
            host="localhost",
            user="postgres",
            password="postgres",
            database="postgres"
        )
        connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        return connection
    except psycopg2.Error as e:
        print(f"Error connecting to PostgreSQL: {e}")
        return None


def create_database(connection):
    """
    Creates the database ALX_prodev if it does not exist.

    Args:
        connection: PostgreSQL connection object
    """
    try:
        cursor = connection.cursor()

        # Check if database exists
        cursor.execute(
            "SELECT 1 FROM pg_database WHERE datname = 'alx_prodev'"
        )
        exists = cursor.fetchone()

        if not exists:
            cursor.execute("CREATE DATABASE alx_prodev")
            print("Database ALX_prodev created successfully")
        else:
            print("Database ALX_prodev already exists")

        cursor.close()
    except psycopg2.Error as e:
        print(f"Error creating database: {e}")


def connect_to_prodev():
    """
    Connects to the ALX_prodev database in PostgreSQL.

    Returns:
        connection: PostgreSQL connection object to ALX_prodev database
    """
    try:
        connection = psycopg2.connect(
            host="localhost",
            user="postgres",
            password="postgres",
            database="alx_prodev"
        )
        return connection
    except psycopg2.Error as e:
        print(f"Error connecting to ALX_prodev: {e}")
        return None


def create_table(connection):
    """
    Creates a table user_data if it does not exist with the required fields.

    Args:
        connection: PostgreSQL connection object
    """
    try:
        cursor = connection.cursor()

        create_table_query = """
        CREATE TABLE IF NOT EXISTS user_data (
            user_id UUID PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL,
            age DECIMAL NOT NULL
        );
        """

        cursor.execute(create_table_query)

        # Create index on user_id
        cursor.execute(
            "CREATE INDEX IF NOT EXISTS idx_user_id ON user_data(user_id)"
        )

        connection.commit()
        cursor.close()
        print("Table user_data created successfully")
    except psycopg2.Error as e:
        print(f"Error creating table: {e}")
        connection.rollback()


def insert_data(connection, csv_file):
    """
    Inserts data into the database if it does not exist.

    Args:
        connection: PostgreSQL connection object
        csv_file: Path to CSV file containing user data
    """
    try:
        cursor = connection.cursor()

        # Check if data already exists
        cursor.execute("SELECT COUNT(*) FROM user_data")
        count = cursor.fetchone()[0]

        if count > 0:
            print(f"Data already exists ({count} rows). Skipping insert.")
            cursor.close()
            return

        # Read and insert data from CSV
        with open(csv_file, 'r') as file:
            csv_reader = csv.DictReader(file)

            insert_query = """
            INSERT INTO user_data (user_id, name, email, age)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (user_id) DO NOTHING
            """

            rows_inserted = 0
            for row in csv_reader:
                # Generate UUID if not present or convert string UUID
                user_id = row.get('user_id', str(uuid.uuid4()))
                if isinstance(user_id, str) and user_id:
                    # Keep existing UUID from CSV
                    pass
                else:
                    user_id = str(uuid.uuid4())

                cursor.execute(insert_query, (
                    user_id,
                    row['name'],
                    row['email'],
                    float(row['age'])
                ))
                rows_inserted += 1

            connection.commit()
            print(f"Successfully inserted {rows_inserted} rows into user_data")

        cursor.close()
    except FileNotFoundError:
        print(f"Error: CSV file '{csv_file}' not found")
    except psycopg2.Error as e:
        print(f"Error inserting data: {e}")
        connection.rollback()
    except Exception as e:
        print(f"Unexpected error: {e}")
        connection.rollback()


if __name__ == "__main__":
    # Test the database setup
    connection = connect_db()
    if connection:
        create_database(connection)
        connection.close()
        print("Connection successful")

        connection = connect_to_prodev()
        if connection:
            create_table(connection)
            insert_data(connection, 'user_data.csv')
            connection.close()
