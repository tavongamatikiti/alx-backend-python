# Python Decorators for Database Operations

## Project Overview

This project focuses on mastering Python decorators to enhance database operations. Through hands-on tasks, you'll create custom decorators to log queries, handle connections, manage transactions, retry failed operations, and cache query results.

## Learning Objectives

By completing these tasks, you will:

- Deepen your knowledge of Python decorators and how they create reusable, efficient code
- Enhance database management skills by automating repetitive tasks
- Implement robust transaction management techniques to ensure data integrity
- Optimize database queries by leveraging caching mechanisms
- Build resilience into database operations with retry mechanisms
- Apply best practices in database interaction for scalable applications

## Requirements

- Python 3.8 or higher
- SQLite3 database with a `users` table
- Working knowledge of Python decorators and database operations
- Git and GitHub for project submission

## Project Structure

```
python-decorators-0x01/
├── 0-log_queries.py           # Query logging decorator
├── 1-with_db_connection.py    # Connection handler decorator
├── 2-transactional.py         # Transaction management decorator
├── 3-retry_on_failure.py      # Retry mechanism decorator
├── 4-cache_query.py           # Query caching decorator
└── README.md                  # Project documentation
```

## Database Setup

Before running the scripts, create the SQLite database with a users table:

```python
import sqlite3

# Create database and users table
conn = sqlite3.connect('users.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL,
        age INTEGER
    )
''')

# Insert sample data
sample_users = [
    ('Alice Johnson', 'alice@example.com', 28),
    ('Bob Smith', 'bob@example.com', 35),
    ('Charlie Brown', 'charlie@example.com', 42),
]

cursor.executemany('INSERT INTO users (name, email, age) VALUES (?, ?, ?)', sample_users)

conn.commit()
conn.close()

print("Database created and sample data inserted successfully!")
```

## Tasks

### Task 0: Logging Database Queries

**File**: `0-log_queries.py`

**Objective**: Create a decorator that logs SQL queries before execution.

**Features**:
- Logs SQL query string before executing
- Uses `functools.wraps` to preserve function metadata
- Extracts query from function arguments or kwargs

**Usage**:
```bash
python3 0-log_queries.py
```

**Expected Output**:
```
Executing SQL Query: SELECT * FROM users
Fetched 3 users
```

### Task 1: Handle Database Connections

**File**: `1-with_db_connection.py`

**Objective**: Automate database connection handling with a decorator.

**Features**:
- Automatically opens database connection
- Passes connection to decorated function
- Ensures connection is closed (even on errors)
- Eliminates boilerplate connection code

**Usage**:
```bash
python3 1-with_db_connection.py
```

**Expected Output**:
```
(1, 'Alice Johnson', 'alice@example.com', 28)
```

### Task 2: Transaction Management

**File**: `2-transactional.py`

**Objective**: Manage database transactions with automatic commit/rollback.

**Features**:
- Automatically commits transaction on success
- Rolls back transaction on error
- Ensures data consistency
- Combines with `with_db_connection` decorator (stacking)

**Usage**:
```bash
python3 2-transactional.py
```

**Expected Output**:
```
Transaction committed successfully
Email updated successfully
```

### Task 3: Retry Failed Queries

**File**: `3-retry_on_failure.py`

**Objective**: Retry database operations on transient failures.

**Features**:
- Configurable retry count (default: 3)
- Configurable delay between retries (default: 2 seconds)
- Logs each retry attempt
- Re-raises exception if all retries fail
- Resilient against transient database issues

**Usage**:
```bash
python3 3-retry_on_failure.py
```

**Expected Output**:
```
Successfully fetched 3 users
```

### Task 4: Cache Query Results

**File**: `4-cache_query.py`

**Objective**: Cache database query results to avoid redundant calls.

**Features**:
- Caches results based on SQL query string
- Uses global `query_cache` dictionary
- Returns cached results on subsequent calls
- Significant performance improvement for repeated queries

**Usage**:
```bash
python3 4-cache_query.py
```

**Expected Output**:
```
==================================================
First call - will execute query and cache result:
Executing query and caching result: SELECT * FROM users
Fetched 3 users

==================================================
Second call - will use cached result:
Using cached result for query: SELECT * FROM users
Fetched 3 users (from cache)
```

## Key Python Concepts

### Decorators

Decorators are functions that modify the behavior of other functions:

```python
def my_decorator(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Code before function execution
        result = func(*args, **kwargs)
        # Code after function execution
        return result
    return wrapper

@my_decorator
def my_function():
    pass
```

### Decorator Stacking

Multiple decorators can be applied to a single function:

```python
@decorator1
@decorator2
def my_function():
    pass

# Equivalent to:
# my_function = decorator1(decorator2(my_function))
```

**Order matters**: Decorators are applied from bottom to top.

### Parameterized Decorators

Decorators can accept parameters:

```python
def retry(retries=3, delay=2):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Use retries and delay parameters
            pass
        return wrapper
    return decorator

@retry(retries=5, delay=1)
def my_function():
    pass
```

## Best Practices

1. **Always use `@functools.wraps`**: Preserves original function's metadata
2. **Handle exceptions gracefully**: Use try/except blocks in decorators
3. **Close resources properly**: Use try/finally to ensure cleanup
4. **Make decorators reusable**: Avoid hardcoding values
5. **Document decorator behavior**: Clear docstrings are essential
6. **Test edge cases**: Empty results, connection failures, etc.

## Common Pitfalls

1. **Forgetting to return the wrapper**: Decorator must return the wrapper function
2. **Not preserving function metadata**: Use `@functools.wraps(func)`
3. **Resource leaks**: Always close connections in finally blocks
4. **Incorrect decorator stacking order**: Remember bottom-to-top execution
5. **Hardcoded values**: Use parameters for flexibility

## Testing

Run each script individually to test its functionality:

```bash
# Test query logging
python3 0-log_queries.py

# Test connection handling
python3 1-with_db_connection.py

# Test transaction management
python3 2-transactional.py

# Test retry mechanism
python3 3-retry_on_failure.py

# Test query caching
python3 4-cache_query.py
```

## Performance Benefits

### Without Decorators
```python
# Repetitive code for every database operation
conn = sqlite3.connect('users.db')
try:
    cursor = conn.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    conn.commit()
finally:
    conn.close()
```

### With Decorators
```python
# Clean, reusable code
@with_db_connection
@transactional
def fetch_users(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()
```

## Advanced Usage

### Combining Multiple Decorators

```python
@with_db_connection
@retry_on_failure(retries=5, delay=1)
@cache_query
@log_queries
def complex_query(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()
```

This function will:
1. Log the query (innermost decorator)
2. Check cache for results
3. Retry up to 5 times on failure
4. Handle database connection automatically

## Repository Information

- **GitHub Repository**: alx-backend-python
- **Directory**: python-decorators-0x01
- **Files**:
  - 0-log_queries.py
  - 1-with_db_connection.py
  - 2-transactional.py
  - 3-retry_on_failure.py
  - 4-cache_query.py

## Resources

- [Python Decorators - Real Python](https://realpython.com/primer-on-python-decorators/)
- [functools.wraps Documentation](https://docs.python.org/3/library/functools.html#functools.wraps)
- [SQLite3 Python Documentation](https://docs.python.org/3/library/sqlite3.html)

## Author

ALX Backend Python - Python Decorators Project

## License

This project is part of the ALX Software Engineering program.

---

**Happy Coding!** ✨