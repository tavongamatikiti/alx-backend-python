# 0x03. Unittests and Integration Tests

This project focuses on unit testing and integration testing in Python using the `unittest` framework with mocking, parameterization, and fixtures.

## Learning Objectives

At the end of this project, you should be able to explain:

- The difference between unit and integration tests
- Common testing patterns such as mocking, parametrizations, and fixtures
- How to use `unittest.mock` to mock external calls
- How to implement parameterized tests
- How to use fixtures for integration tests

## Requirements

- All files are interpreted/compiled on Ubuntu 18.04 LTS using python3 (version 3.7)
- All files end with a new line
- The first line of all files is exactly `#!/usr/bin/env python3`
- Code follows the pycodestyle style (version 2.5)
- All files are executable
- All modules have documentation
- All classes have documentation
- All functions (inside and outside a class) have documentation
- All functions and coroutines are type-annotated

## Files

### Source Files

- **utils.py** - Generic utilities for github org client
  - `access_nested_map()` - Access nested map with key path
  - `get_json()` - Get JSON from remote URL
  - `memoize()` - Decorator to memoize a method

- **client.py** - Github org client implementation
  - `GithubOrgClient` - A Github organization client class

- **fixtures.py** - Test fixtures data for integration tests
  - `TEST_PAYLOAD` - Sample GitHub API response data

### Test Files

- **test_utils.py** - Unit tests for utils module
  - `TestAccessNestedMap` - Test class for access_nested_map function
    - `test_access_nested_map()` - Parameterized tests for standard inputs
    - `test_access_nested_map_exception()` - Tests for exception handling
  - `TestGetJson` - Test class for get_json function
    - `test_get_json()` - Tests with mocked HTTP calls
  - `TestMemoize` - Test class for memoize decorator
    - `test_memoize()` - Tests memoization functionality

- **test_client.py** - Unit and integration tests for client module
  - `TestGithubOrgClient` - Unit tests for GithubOrgClient class
    - `test_org()` - Tests org property with mocked get_json
    - `test_public_repos_url()` - Tests _public_repos_url property
    - `test_public_repos()` - Tests public_repos method
    - `test_has_license()` - Parameterized tests for has_license method
  - `TestIntegrationGithubOrgClient` - Integration tests
    - `test_public_repos()` - Integration test for public_repos
    - `test_public_repos_with_license()` - Integration test with license filter

## Installation

Install required dependencies:

```bash
python3 -m venv venv
source venv/bin/activate
pip install parameterized requests
```

## Running Tests

### Run all tests in test_utils.py:
```bash
python3 -m unittest test_utils.py
```

### Run all tests in test_client.py:
```bash
python3 -m unittest test_client.py
```

### Run a specific test class:
```bash
python3 -m unittest test_utils.TestAccessNestedMap
```

### Run a specific test method:
```bash
python3 -m unittest test_utils.TestAccessNestedMap.test_access_nested_map
```

### Run all tests with verbose output:
```bash
python3 -m unittest discover -v
```

## Tasks

### Task 0: Parameterize a unit test
Test the `access_nested_map` function with parameterized inputs.

### Task 1: Parameterize a unit test (Exception)
Test that `access_nested_map` raises KeyError for invalid inputs.

### Task 2: Mock HTTP calls
Test `get_json` function using mocked HTTP requests.

### Task 3: Parameterize and patch
Test the `memoize` decorator to ensure it caches results.

### Task 4: Parameterize and patch as decorators
Test `GithubOrgClient.org` with parameterized organization names.

### Task 5: Mocking a property
Test `GithubOrgClient._public_repos_url` property with mocked org data.

### Task 6: More patching
Test `GithubOrgClient.public_repos` method with mocked dependencies.

### Task 7: Parameterize
Test `GithubOrgClient.has_license` static method with parameterized inputs.

### Task 8: Integration test: fixtures
Integration tests for `GithubOrgClient.public_repos` using fixtures.

## Testing Concepts

### Unit Testing
Tests individual functions in isolation by mocking external dependencies. Focuses on testing logic within a single function.

### Integration Testing
Tests code paths end-to-end with minimal mocking. Only low-level external calls (HTTP, database, file I/O) are mocked.

### Mocking
Using `unittest.mock` to replace external dependencies with controlled test objects:
- `@patch()` - Decorator to patch objects
- `Mock()` - Create mock objects
- `PropertyMock()` - Mock properties
- `assert_called_once()` - Verify mock was called once

### Parameterization
Using `@parameterized.expand()` to run the same test with different inputs.

### Fixtures
Test data used in integration tests, defined in `fixtures.py`.

## Repository

- **GitHub repository**: alx-backend-python
- **Directory**: 0x03-Unittests_and_integration_tests

## Author

ALX Backend Python - Unit Testing and Integration Testing Project
