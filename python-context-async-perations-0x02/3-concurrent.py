#!/usr/bin/env python3
"""
Task 2: Concurrent Asynchronous Database Queries
Run multiple database queries concurrently using asyncio.gather.
"""

import asyncio
import aiosqlite


async def async_fetch_users():
    """
    Asynchronously fetch all users from the database.

    Returns:
        list: All users from the users table
    """
    async with aiosqlite.connect('users.db') as db:
        cursor = await db.execute("SELECT * FROM users")
        results = await cursor.fetchall()
        print("All users fetched:")
        print("-" * 60)
        for row in results:
            print(f"ID: {row[0]}, Name: {row[1]}, Email: {row[2]}, Age: {row[3]}")
        return results


async def async_fetch_older_users():
    """
    Asynchronously fetch users older than 40 from the database.

    Returns:
        list: Users with age > 40
    """
    async with aiosqlite.connect('users.db') as db:
        cursor = await db.execute("SELECT * FROM users WHERE age > ?", (40,))
        results = await cursor.fetchall()
        print("\nUsers older than 40:")
        print("-" * 60)
        for row in results:
            print(f"ID: {row[0]}, Name: {row[1]}, Email: {row[2]}, Age: {row[3]}")
        return results


async def fetch_concurrently():
    """
    Execute both fetch operations concurrently using asyncio.gather.

    Returns:
        tuple: Results from both async_fetch_users and async_fetch_older_users
    """
    print("Starting concurrent database queries...\n")
    results = await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )
    print("\n" + "=" * 60)
    print("Both queries completed successfully!")
    print("=" * 60)
    return results


if __name__ == "__main__":
    # Run the concurrent fetch using asyncio.run()
    asyncio.run(fetch_concurrently())