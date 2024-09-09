import pytest
from unittest.mock import patch, MagicMock
import sqlite3
import os
from shopping_cart.database import DatabaseConnection, add_item_to_cart_db

@pytest.fixture
def mock_database_connection():
    with patch('shopping_cart.database.sqlite3.connect') as mock_connect:
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        
        yield mock_conn, mock_cursor

@pytest.fixture
def mock_os_path():
    with patch('shopping_cart.database.os.path') as mock_path:
        mock_path.dirname.return_value = '/mocked/path'
        mock_path.abspath.return_value = '/mocked/path/shopping_cart.database.py'
        mock_path.join.return_value = '/mocked/path/shopping_cart.db'
        yield mock_path

@pytest.fixture
def mock_database_connection_class():
    with patch('shopping_cart.database.DatabaseConnection') as MockDatabaseConnection:
        mock_instance = MockDatabaseConnection.return_value
        mock_instance.connect = MagicMock()
        mock_instance.execute = MagicMock()
        mock_instance.fetchone = MagicMock()
        mock_instance.fetchall = MagicMock()
        mock_instance.commit = MagicMock()
        mock_instance.close = MagicMock()
        yield mock_instance
```

# happy_path - test_connect_with_valid_path - Test that the connection is established when a valid database path is provided
def test_connect_with_valid_path(mock_database_connection_class, mock_os_path):
    db_path = '/mocked/path/shopping_cart.db'
    database_connection = DatabaseConnection(db_path)
    database_connection.connect()
    mock_database_connection_class.connect.assert_called_once()

# happy_path - test_execute_with_parameters - Test that a query is executed successfully with given parameters
def test_execute_with_parameters(mock_database_connection_class, mock_database_connection):
    query = 'INSERT INTO cart (item, quantity) VALUES (?, ?)'
    params = ['apple', 3]
    database_connection.execute(query, params)
    mock_database_connection_class.execute.assert_called_once_with(query, params)

# happy_path - test_fetchone_with_valid_query - Test that fetchone returns the correct single row
def test_fetchone_with_valid_query(mock_database_connection_class, mock_database_connection):
    query = 'SELECT * FROM cart WHERE item = ?'
    params = ['apple']
    mock_database_connection_class.fetchone.return_value = {'item': 'apple', 'quantity': 3}
    result = database_connection.fetchone(query, params)
    mock_database_connection_class.fetchone.assert_called_once_with(query, params)
    assert result == {'item': 'apple', 'quantity': 3}

# happy_path - test_fetchall_with_valid_query - Test that fetchall returns all rows correctly
def test_fetchall_with_valid_query(mock_database_connection_class, mock_database_connection):
    query = 'SELECT * FROM cart'
    mock_database_connection_class.fetchall.return_value = [{'item': 'apple', 'quantity': 3}]
    results = database_connection.fetchall(query)
    mock_database_connection_class.fetchall.assert_called_once_with(query)
    assert results == [{'item': 'apple', 'quantity': 3}]

# happy_path - test_commit_after_insert - Test that commit saves changes to the database
def test_commit_after_insert(mock_database_connection_class, mock_database_connection):
    database_connection.commit()
    mock_database_connection_class.commit.assert_called_once()

# happy_path - test_close_connection - Test that close closes the connection
def test_close_connection(mock_database_connection_class, mock_database_connection):
    database_connection.close()
    mock_database_connection_class.close.assert_called_once()

# edge_case - test_connect_with_invalid_path - Test that an error is raised when trying to connect with an invalid database path
def test_connect_with_invalid_path(mock_database_connection_class, mock_os_path):
    db_path = '/invalid/path/to/db'
    database_connection = DatabaseConnection(db_path)
    with pytest.raises(sqlite3.OperationalError):
        database_connection.connect()

# edge_case - test_execute_with_malformed_query - Test that execute handles a malformed query properly
def test_execute_with_malformed_query(mock_database_connection_class, mock_database_connection):
    query = 'INSERT INTO cart (item, quantity VALUES (?, ?)'
    params = ['apple', 3]
    with pytest.raises(sqlite3.ProgrammingError):
        database_connection.execute(query, params)

# edge_case - test_fetchone_with_no_results - Test that fetchone returns None for a query with no results
def test_fetchone_with_no_results(mock_database_connection_class, mock_database_connection):
    query = 'SELECT * FROM cart WHERE item = ?'
    params = ['nonexistent']
    mock_database_connection_class.fetchone.return_value = None
    result = database_connection.fetchone(query, params)
    mock_database_connection_class.fetchone.assert_called_once_with(query, params)
    assert result is None

# edge_case - test_fetchall_with_no_results - Test that fetchall returns an empty list for a query with no results
def test_fetchall_with_no_results(mock_database_connection_class, mock_database_connection):
    query = 'SELECT * FROM cart WHERE item = ?'
    params = ['nonexistent']
    mock_database_connection_class.fetchall.return_value = []
    results = database_connection.fetchall(query, params)
    mock_database_connection_class.fetchall.assert_called_once_with(query, params)
    assert results == []

# edge_case - test_close_already_closed_connection - Test that closing an already closed connection does not raise an error
def test_close_already_closed_connection(mock_database_connection_class, mock_database_connection):
    database_connection.close()
    database_connection.close()
    mock_database_connection_class.close.assert_called_once()

# edge_case - test_add_item_to_cart_db_with_invalid_query - Test that add_item_to_cart_db raises an error with invalid query
def test_add_item_to_cart_db_with_invalid_query(mock_database_connection_class, mock_database_connection):
    query = 'INSERT INTO cart (item, quantity VALUES (?, ?)'
    params = ['apple', 3]
    with pytest.raises(sqlite3.ProgrammingError):
        add_item_to_cart_db(query, params)

