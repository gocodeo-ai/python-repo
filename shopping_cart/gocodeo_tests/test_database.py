import pytest
from unittest.mock import patch, MagicMock
import sqlite3
import os
from shopping_cart.database import DatabaseConnection, add_item_to_cart_db

@pytest.fixture
def mock_sqlite3_connect():
    with patch('shopping_cart.database.sqlite3.connect', autospec=True) as mock_connect:
        mock_connection = MagicMock()
        mock_connect.return_value = mock_connection
        yield mock_connect, mock_connection

@pytest.fixture
def mock_os_path():
    with patch('shopping_cart.database.os.path', autospec=True) as mock_path:
        mock_path.dirname.return_value = '/mocked/path'
        mock_path.abspath.return_value = '/mocked/path/shopping_cart.db'
        mock_path.join.return_value = '/mocked/path/shopping_cart.db'
        yield mock_path

@pytest.fixture
def mock_database_connection(mock_sqlite3_connect):
    mock_connect, mock_connection = mock_sqlite3_connect
    db_conn = DatabaseConnection('/mocked/path/shopping_cart.db')
    yield db_conn, mock_connect, mock_connection

@pytest.fixture
def mock_cursor():
    with patch('shopping_cart.database.sqlite3.Cursor', autospec=True) as mock_cursor:
        mock_cursor_instance = mock_cursor.return_value
        yield mock_cursor_instance

@pytest.fixture
def mock_database_methods(mock_database_connection, mock_cursor):
    db_conn, mock_connect, mock_connection = mock_database_connection
    mock_connection.cursor.return_value = mock_cursor
    mock_cursor_instance = mock_cursor
    return db_conn, mock_connect, mock_connection, mock_cursor_instance

# happy_path - test_init_with_valid_path - Test that the database connection is initialized correctly with a valid path
def test_init_with_valid_path(mock_os_path):
    db_conn = DatabaseConnection('shopping_cart.db')
    assert db_conn.connection is None
    assert db_conn.db_path == '/mocked/path/shopping_cart.db'

# happy_path - test_connect_success - Test that the connection is established successfully
def test_connect_success(mock_database_connection):
    db_conn, mock_connect, mock_connection = mock_database_connection
    db_conn.connect()
    mock_connect.assert_called_once_with('/mocked/path/shopping_cart.db')
    assert db_conn.connection == mock_connection

# happy_path - test_execute_query_without_params - Test that a query is executed successfully without parameters
def test_execute_query_without_params(mock_database_methods):
    db_conn, mock_connect, mock_connection, mock_cursor_instance = mock_database_methods
    db_conn.connect()
    db_conn.execute('CREATE TABLE IF NOT EXISTS cart (id INTEGER PRIMARY KEY)')
    mock_cursor_instance.execute.assert_called_once_with('CREATE TABLE IF NOT EXISTS cart (id INTEGER PRIMARY KEY)', [])

# happy_path - test_fetchone_success - Test that a single record is fetched successfully
def test_fetchone_success(mock_database_methods):
    db_conn, mock_connect, mock_connection, mock_cursor_instance = mock_database_methods
    mock_cursor_instance.fetchone.return_value = None
    db_conn.connect()
    result = db_conn.fetchone('SELECT * FROM cart WHERE id = ?', [1])
    mock_cursor_instance.execute.assert_called_once_with('SELECT * FROM cart WHERE id = ?', [1])
    assert result is None

# happy_path - test_fetchall_success - Test that all records are fetched successfully
def test_fetchall_success(mock_database_methods):
    db_conn, mock_connect, mock_connection, mock_cursor_instance = mock_database_methods
    mock_cursor_instance.fetchall.return_value = []
    db_conn.connect()
    results = db_conn.fetchall('SELECT * FROM cart')
    mock_cursor_instance.execute.assert_called_once_with('SELECT * FROM cart', [])
    assert results == []

# happy_path - test_commit_success - Test that changes are committed successfully
def test_commit_success(mock_database_methods):
    db_conn, mock_connect, mock_connection, mock_cursor_instance = mock_database_methods
    db_conn.connect()
    db_conn.commit()
    mock_connection.commit.assert_called_once()

# happy_path - test_close_connection - Test that the connection is closed successfully
def test_close_connection(mock_database_methods):
    db_conn, mock_connect, mock_connection, mock_cursor_instance = mock_database_methods
    db_conn.connect()
    db_conn.close()
    mock_connection.close.assert_called_once()
    assert db_conn.connection is None

# happy_path - test_add_item_to_cart_db_success - Test that an item is added to the cart database successfully
def test_add_item_to_cart_db_success(mock_database_methods):
    db_conn, mock_connect, mock_connection, mock_cursor_instance = mock_database_methods
    add_item_to_cart_db('INSERT INTO cart (id) VALUES (?)', [1])
    mock_cursor_instance.execute.assert_called_once_with('INSERT INTO cart (id) VALUES (?)', [1])
    mock_connection.commit.assert_called_once()
    mock_connection.close.assert_called_once()

# edge_case - test_init_with_invalid_path - Test that initializing with an invalid path raises an error
def test_init_with_invalid_path():
    with pytest.raises(sqlite3.OperationalError):
        DatabaseConnection('/invalid/path/shopping_cart.db').connect()

# edge_case - test_execute_invalid_query - Test that executing an invalid query raises an error
def test_execute_invalid_query(mock_database_methods):
    db_conn, mock_connect, mock_connection, mock_cursor_instance = mock_database_methods
    mock_cursor_instance.execute.side_effect = sqlite3.OperationalError
    db_conn.connect()
    with pytest.raises(sqlite3.OperationalError):
        db_conn.execute('INVALID QUERY')

# edge_case - test_fetchone_non_existent_table - Test that fetching from a non-existent table returns None
def test_fetchone_non_existent_table(mock_database_methods):
    db_conn, mock_connect, mock_connection, mock_cursor_instance = mock_database_methods
    mock_cursor_instance.execute.side_effect = sqlite3.OperationalError
    db_conn.connect()
    with pytest.raises(sqlite3.OperationalError):
        db_conn.fetchone('SELECT * FROM non_existent_table')

# edge_case - test_fetchall_non_existent_table - Test that fetching all from a non-existent table returns an empty list
def test_fetchall_non_existent_table(mock_database_methods):
    db_conn, mock_connect, mock_connection, mock_cursor_instance = mock_database_methods
    mock_cursor_instance.execute.side_effect = sqlite3.OperationalError
    db_conn.connect()
    with pytest.raises(sqlite3.OperationalError):
        db_conn.fetchall('SELECT * FROM non_existent_table')

# edge_case - test_commit_no_changes - Test that committing without any changes does not raise an error
def test_commit_no_changes(mock_database_methods):
    db_conn, mock_connect, mock_connection, mock_cursor_instance = mock_database_methods
    db_conn.connect()
    db_conn.commit()
    mock_connection.commit.assert_called_once()

# edge_case - test_close_already_closed_connection - Test that closing an already closed connection does not raise an error
def test_close_already_closed_connection(mock_database_methods):
    db_conn, mock_connect, mock_connection, mock_cursor_instance = mock_database_methods
    db_conn.connect()
    db_conn.close()
    db_conn.close()
    mock_connection.close.assert_called_once()
    assert db_conn.connection is None

