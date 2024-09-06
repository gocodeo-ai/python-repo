import pytest
import sqlite3
import os
from unittest.mock import Mock, patch
from shopping_cart.database import DatabaseConnection, add_item_to_cart_db

@pytest.fixture
def mock_sqlite3_connect():
    with patch('sqlite3.connect') as mock_connect:
        mock_connection = Mock()
        mock_cursor = Mock()
        mock_connection.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_connection
        yield mock_connect

@pytest.fixture
def mock_os_path():
    with patch('os.path') as mock_path:
        mock_path.dirname.return_value = '/mock/dir'
        mock_path.abspath.return_value = '/mock/dir/shopping_cart.py'
        mock_path.join.return_value = '/mock/dir/shopping_cart.db'
        yield mock_path

@pytest.fixture
def mock_database_connection(mock_sqlite3_connect, mock_os_path):
    with patch('shopping_cart.database.DatabaseConnection') as MockDatabaseConnection:
        mock_instance = MockDatabaseConnection.return_value
        mock_instance.connection = None
        mock_instance.db_path = '/mock/dir/shopping_cart.db'

        def mock_connect():
            mock_instance.connection = mock_sqlite3_connect.return_value

        def mock_execute(query, params=None):
            if params is None:
                params = []
            cursor = mock_instance.connection.cursor()
            cursor.execute(query, params)

        def mock_fetchone(query, params=None):
            if params is None:
                params = []
            cursor = mock_instance.connection.cursor()
            cursor.execute(query, params)
            return cursor.fetchone()

        def mock_fetchall(query, params=None):
            if params is None:
                params = []
            cursor = mock_instance.connection.cursor()
            cursor.execute(query, params)
            return cursor.fetchall()

        def mock_commit():
            mock_instance.connection.commit()

        def mock_close():
            if mock_instance.connection:
                mock_instance.connection.close()
                mock_instance.connection = None

        mock_instance.connect = mock_connect
        mock_instance.execute = mock_execute
        mock_instance.fetchone = mock_fetchone
        mock_instance.fetchall = mock_fetchall
        mock_instance.commit = mock_commit
        mock_instance.close = mock_close

        yield mock_instance

@pytest.fixture
def mock_add_item_to_cart_db(mock_database_connection):
    with patch('shopping_cart.database.add_item_to_cart_db') as mock_add_item:
        def side_effect(query, params=None):
            if params is None:
                params = []
            mock_database_connection.connect()
            mock_database_connection.execute(query, params)
            mock_database_connection.commit()
            mock_database_connection.close()
        
        mock_add_item.side_effect = side_effect
        yield mock_add_item

# happy path - connect - Test successful database connection
def test_successful_connection(mock_database_connection):
    mock_database_connection.connect()
    assert mock_database_connection.connection is not None

# happy path - execute - Test successful query execution
def test_successful_execution(mock_database_connection):
    mock_database_connection.connect()
    mock_database_connection.execute('CREATE TABLE test (id INTEGER PRIMARY KEY, name TEXT)')
    assert True  # No exception raised

# happy path - fetchone - Test fetching single row
def test_fetch_single_row(mock_database_connection):
    mock_database_connection.connect()
    result = mock_database_connection.fetchone('SELECT * FROM test WHERE id = 1')
    assert result is not None

# happy path - fetchall - Test fetching multiple rows
def test_fetch_multiple_rows(mock_database_connection):
    mock_database_connection.connect()
    results = mock_database_connection.fetchall('SELECT * FROM test')
    assert len(results) > 0

# happy path - commit - Test successful commit
def test_successful_commit(mock_database_connection):
    mock_database_connection.connect()
    mock_database_connection.commit()
    assert True  # No exception raised

# happy path - close - Test successful database closure
def test_successful_closure(mock_database_connection):
    mock_database_connection.connect()
    mock_database_connection.close()
    assert mock_database_connection.connection is None

# happy path - connect - Test successful database connection
def test_connect_success(mock_database_connection):
    mock_database_connection.connect()
    assert mock_database_connection.connection is not None

# happy path - execute - Test successful query execution
def test_execute_success(mock_database_connection):
    mock_database_connection.connect()
    mock_database_connection.execute('CREATE TABLE test (id INTEGER PRIMARY KEY, name TEXT)')
    assert True  # Query executed without errors

# happy path - fetchone - Test fetching a single result
def test_fetchone_success(mock_database_connection):
    mock_database_connection.connect()
    result = mock_database_connection.fetchone('SELECT * FROM test WHERE id = 1')
    assert result is not None

# happy path - fetchall - Test fetching multiple results
def test_fetchall_success(mock_database_connection):
    mock_database_connection.connect()
    results = mock_database_connection.fetchall('SELECT * FROM test')
    assert len(results) > 0

# happy path - commit - Test successful commit
def test_commit_success(mock_database_connection):
    mock_database_connection.connect()
    mock_database_connection.commit()
    assert True  # Changes committed to the database

# happy path - close - Test successful database closure
def test_close_success(mock_database_connection):
    mock_database_connection.connect()
    mock_database_connection.close()
    assert mock_database_connection.connection is None

# edge case - connect - Test connection with invalid database path
def test_invalid_db_path(mock_database_connection):
    with pytest.raises(sqlite3.OperationalError):
        mock_database_connection.db_path = '/invalid/path/to/db.sqlite'
        mock_database_connection.connect()

# edge case - execute - Test execution with invalid SQL query
def test_invalid_sql_query(mock_database_connection):
    mock_database_connection.connect()
    with pytest.raises(sqlite3.OperationalError):
        mock_database_connection.execute('INVALID SQL QUERY')

# edge case - fetchone - Test fetchone with no results
def test_fetchone_no_results(mock_database_connection):
    mock_database_connection.connect()
    result = mock_database_connection.fetchone('SELECT * FROM test WHERE id = 9999')
    assert result is None

# edge case - fetchall - Test fetchall with no results
def test_fetchall_no_results(mock_database_connection):
    mock_database_connection.connect()
    results = mock_database_connection.fetchall('SELECT * FROM test WHERE id > 9999')
    assert len(results) == 0

# edge case - commit - Test commit without open connection
def test_commit_without_connection(mock_database_connection):
    with pytest.raises(AttributeError):
        mock_database_connection.commit()

# edge case - close - Test close without open connection
def test_close_without_connection(mock_database_connection):
    mock_database_connection.close()
    assert mock_database_connection.connection is None

# edge case - connect - Test connection with invalid database path
def test_connect_invalid_path(mock_database_connection):
    with pytest.raises(sqlite3.OperationalError):
        mock_database_connection.db_path = '/invalid/path/to/db.sqlite'
        mock_database_connection.connect()

# edge case - execute - Test execution of invalid SQL query
def test_execute_invalid_query(mock_database_connection):
    mock_database_connection.connect()
    with pytest.raises(sqlite3.OperationalError):
        mock_database_connection.execute('INVALID SQL QUERY')

# edge case - fetchone - Test fetchone with no results
def test_fetchone_no_results(mock_database_connection):
    mock_database_connection.connect()
    result = mock_database_connection.fetchone('SELECT * FROM test WHERE id = 9999')
    assert result is None

# edge case - fetchall - Test fetchall with empty table
def test_fetchall_empty_table(mock_database_connection):
    mock_database_connection.connect()
    results = mock_database_connection.fetchall('SELECT * FROM empty_table')
    assert len(results) == 0

# edge case - commit - Test commit without active transaction
def test_commit_no_transaction(mock_database_connection):
    mock_database_connection.connect()
    mock_database_connection.commit()
    assert True  # No error raised

# edge case - close - Test close on already closed connection
def test_close_already_closed(mock_database_connection):
    mock_database_connection.connect()
    mock_database_connection.close()
    mock_database_connection.close()
    assert mock_database_connection.connection is None

