# Python Generators - 0x00

## Project Overview
This project focuses on mastering Python generators to efficiently handle large datasets, process data in batches, and implement memory-efficient computations using PostgreSQL database integration.

## Learning Objectives
- Master Python Generators using the `yield` keyword
- Handle large datasets with batch processing and lazy loading
- Optimize performance through memory-efficient operations
- Integrate Python with PostgreSQL for dynamic data fetching
- Simulate real-world data streaming scenarios

## Requirements
- Python 3.x
- PostgreSQL database server
- `psycopg2` library for PostgreSQL connection
- Understanding of Python generators and the `yield` keyword
- Basic SQL knowledge

## Installation

### 1. Install PostgreSQL
```bash
# macOS
brew install postgresql

# Ubuntu/Debian
sudo apt-get install postgresql postgresql-contrib

# Start PostgreSQL service
brew services start postgresql  # macOS
sudo service postgresql start   # Linux
```

### 2. Install Python Dependencies
```bash
pip install psycopg2-binary
```

### 3. Configure PostgreSQL
Update database credentials in all Python files if needed:
- **Host**: localhost
- **User**: postgres
- **Password**: postgres
- **Database**: alx_prodev (created automatically)

## Project Structure

```
python-generators-0x00/
├── seed.py                    # Database setup and seeding
├── 0-stream_users.py          # Stream users one by one
├── 1-batch_processing.py      # Batch processing with filtering
├── 2-lazy_paginate.py         # Lazy pagination implementation
├── 4-stream_ages.py           # Memory-efficient age aggregation
├── user_data.csv              # Sample user data
└── README.md                  # Project documentation
```

## Tasks

### Task 0: Database Setup (`seed.py`)
Sets up PostgreSQL database and populates it with user data.

**Functions:**
- `connect_db()`: Connects to PostgreSQL server
- `create_database(connection)`: Creates ALX_prodev database
- `connect_to_prodev()`: Connects to ALX_prodev database
- `create_table(connection)`: Creates user_data table
- `insert_data(connection, csv_file)`: Inserts data from CSV

**Database Schema:**
```sql
CREATE TABLE user_data (
    user_id UUID PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    age DECIMAL NOT NULL
);
```

**Usage:**
```bash
python3 seed.py
```

### Task 1: Stream Users Generator (`0-stream_users.py`)
Generator function that streams rows from database one by one.

**Function:**
- `stream_users()`: Yields user dictionaries one at a time

**Constraints:**
- Maximum 1 loop
- Must use `yield` keyword

**Usage:**
```python
from itertools import islice

for user in islice(stream_users(), 6):
    print(user)
```

**Output:**
```python
{'user_id': '...', 'name': 'Dan Altenwerth Jr.', 'email': 'Molly59@gmail.com', 'age': 67}
{'user_id': '...', 'name': 'Glenda Wisozk', 'email': 'Miriam21@gmail.com', 'age': 119}
...
```

### Task 2: Batch Processing (`1-batch_processing.py`)
Fetches and processes data in batches with filtering.

**Functions:**
- `stream_users_in_batches(batch_size)`: Yields batches of users
- `batch_processing(batch_size)`: Filters users over age 25

**Constraints:**
- Maximum 3 loops
- Must use `yield` generator

**Usage:**
```bash
python3 1-batch_processing.py | head -n 5
```

**Output:**
```python
{'user_id': '...', 'name': 'Dan Altenwerth Jr.', 'email': 'Molly59@gmail.com', 'age': 67}
{'user_id': '...', 'name': 'Glenda Wisozk', 'email': 'Miriam21@gmail.com', 'age': 119}
...
```

### Task 3: Lazy Pagination (`2-lazy_paginate.py`)
Implements lazy loading of paginated data.

**Functions:**
- `paginate_users(page_size, offset)`: Fetches a specific page
- `lazy_pagination(page_size)`: Generator for lazy page loading

**Constraints:**
- Only 1 loop
- Must use `yield` generator
- Fetches next page only when needed

**Usage:**
```bash
python3 2-lazy_paginate.py | head -n 7
```

**Output:**
```python
{'user_id': '...', 'name': 'Dan Altenwerth Jr.', 'email': 'Molly59@gmail.com', 'age': 67}
{'user_id': '...', 'name': 'Glenda Wisozk', 'email': 'Miriam21@gmail.com', 'age': 119}
...
```

### Task 4: Memory-Efficient Aggregation (`4-stream_ages.py`)
Calculates average age without loading entire dataset into memory.

**Functions:**
- `stream_user_ages()`: Generator yielding ages one by one
- `calculate_average_age()`: Computes average using generator

**Constraints:**
- Maximum 2 loops
- Cannot use SQL AVERAGE function
- Must use generators for memory efficiency

**Usage:**
```bash
python3 4-stream_ages.py
```

**Output:**
```
Average age of users: 45.23
```

## Key Concepts

### Python Generators
Generators are functions that use `yield` instead of `return`, allowing them to:
- Produce values lazily (on-demand)
- Maintain state between calls
- Use minimal memory for large datasets

### Memory Efficiency
Instead of loading all data at once:
```python
# Bad - loads everything into memory
users = fetch_all_users()  # 1M rows in memory!

# Good - processes one at a time
for user in stream_users():  # Only 1 row in memory
    process(user)
```

### Lazy Evaluation
Data is only fetched when needed:
```python
# Pages are only loaded when iteration reaches them
for page in lazy_pagination(100):
    process_page(page)
```

## Testing

### Test Database Setup
```bash
python3 seed.py
```

### Test Stream Users
```bash
python3 0-stream_users.py
```

### Test Batch Processing
```bash
python3 1-batch_processing.py | head -n 10
```

### Test Lazy Pagination
```bash
python3 2-lazy_paginate.py | head -n 10
```

### Test Age Aggregation
```bash
python3 4-stream_ages.py
```

## Best Practices

1. **Always close database connections** to prevent resource leaks
2. **Use generators for large datasets** to minimize memory usage
3. **Implement proper error handling** for database operations
4. **Use context managers** where possible for automatic cleanup
5. **Follow loop constraints** as specified in each task

## Common Issues & Solutions

### Issue: Connection Refused
```
Solution: Ensure PostgreSQL is running
brew services start postgresql  # macOS
sudo service postgresql start   # Linux
```

### Issue: Authentication Failed
```
Solution: Update credentials in Python files or configure PostgreSQL
- Check postgresql.conf for authentication settings
- Update pg_hba.conf if needed
```

### Issue: Database Already Exists
```
Solution: This is normal - seed.py handles existing databases gracefully
```

## Performance Benefits

### Without Generators (Loading All Data)
- Memory: ~500MB for 1M rows
- Load time: 5-10 seconds
- Unusable for very large datasets

### With Generators (Streaming)
- Memory: ~1KB (single row)
- Load time: Immediate (lazy)
- Scalable to billions of rows

## Repository Information
- **GitHub Repository**: alx-backend-python
- **Directory**: python-generators-0x00
- **Files**: seed.py, 0-stream_users.py, 1-batch_processing.py, 2-lazy_paginate.py, 4-stream_ages.py, README.md

## Author
ALX Backend Python - Python Generators Project

## License
This project is part of the ALX Software Engineering program.
