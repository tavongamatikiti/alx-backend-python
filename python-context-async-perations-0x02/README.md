# Python Context Managers & Async Operations

This project demonstrates advanced Python techniques for managing database connections and executing queries using context managers and asynchronous programming.

## Learning Objectives

- Implement class-based context managers using `__enter__` and `__exit__` methods
- Understand resource management and automatic cleanup with context managers
- Master asynchronous database operations using `aiosqlite`
- Implement concurrent query execution with `asyncio.gather`
- Handle database connections and queries in a Pythonic way

## Project Structure

```
python-context-async-perations-0x02/
├── 0-databaseconnection.py    # Task 0: Custom DatabaseConnection context manager
├── 1-execute.py                # Task 1: Reusable ExecuteQuery context manager
├── 3-concurrent.py             # Task 2: Concurrent async database queries
├── users.db                    # SQLite database with test data
└── README.md                   # This file
```

## Requirements

- Python 3.7+
- sqlite3 (included in Python standard library)
- aiosqlite (for async operations)

### Installation

```bash
pip install aiosqlite
```

## Tasks

### Task 0: Custom Class-Based Context Manager

**File:** `0-databaseconnection.py`

Implements a `DatabaseConnection` class that uses `__enter__` and `__exit__` methods to automatically manage database connections.

**Usage:**
```python
with DatabaseConnection('users.db') as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    results = cursor.fetchall()
```

**Run:**
```bash
python3 0-databaseconnection.py
```

### Task 1: Reusable Query Context Manager

**File:** `1-execute.py`

Implements an `ExecuteQuery` class that takes a query and parameters as input, managing both connection and query execution.

**Usage:**
```python
query = "SELECT * FROM users WHERE age > ?"
with ExecuteQuery('users.db', query, (25,)) as results:
    for row in results:
        print(row)
```

**Run:**
```bash
python3 1-execute.py
```

### Task 2: Concurrent Asynchronous Database Queries

**File:** `3-concurrent.py`

Uses `aiosqlite` and `asyncio.gather()` to execute multiple database queries concurrently for improved performance.

**Features:**
- `async_fetch_users()`: Fetches all users
- `async_fetch_older_users()`: Fetches users older than 40
- `fetch_concurrently()`: Executes both queries concurrently

**Run:**
```bash
python3 3-concurrent.py
```

## Database Schema

The `users.db` database contains a `users` table with the following schema:

```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    age INTEGER
);
```

## Key Concepts

### Context Managers
Context managers ensure proper resource acquisition and release using the `with` statement pattern. The `__enter__` method handles resource setup, while `__exit__` guarantees cleanup even if exceptions occur.

### Asynchronous Programming
Using `async/await` syntax with `aiosqlite` enables non-blocking database operations, allowing multiple queries to execute concurrently for improved performance.

### Concurrent Execution
`asyncio.gather()` allows multiple asynchronous operations to run simultaneously, significantly reducing total execution time for independent queries.

## Real-World Use Cases

1. **Web Application Backends**: Context managers ensure database connections are properly closed after each request
2. **Data Processing Pipelines**: Reusable query context managers simplify ETL processes
3. **Analytics Dashboards**: Concurrent async queries provide faster load times
4. **Microservices Architecture**: Async operations enable efficient handling of concurrent requests
5. **Automated Testing**: Context managers ensure proper cleanup of test databases

## Author

ALX Backend Python Program