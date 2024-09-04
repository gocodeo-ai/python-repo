import pytest
from unittest.mock import patch, MagicMock
import sqlite3
import os
from shopping_cart.database import DatabaseConnection, add_item_to_cart_db

@pytest.fixture
def mock_db_connection():
    with patch('shopping_cart.database.DatabaseConnection') as MockDatabaseConnection:
        mock_instance = MockDatabaseConnection.return_value
        mock_instance.connect.return_value = None
        mock_instance.execute.return_value = None
        mock_instance.fetchone.return_value = None
        mock_instance.fetchall.return_value = []
        mock_instance.commit.return_value = None
        mock_instance.close.return_value = None
        yield mock_instance

@pytest.fixture
def mock_sqlite3_connect():
    with patch('shopping_cart.database.sqlite3.connect') as mock_connect:
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_conn
        yield mock_connect, mock_conn, mock_cursor

@pytest.fixture
def mock_os_path():
    with patch('shopping_cart.database.os.path') as mock_path:
        mock_path.dirname.return_value = '/mocked/dir'
        mock_path.abspath.return_value = '/mocked/dir/shopping_cart.db'
        mock_path.join.return_value = '/mocked/dir/shopping_cart.db'
        yield mock_path

# happy_path - test_database_connection_initialization - Test that the database connection is initialized with the correct database path
def test_database_connection_initialization(mock_os_path):
    db_path = '/mocked/dir/shopping_cart.db'
    db_conn = DatabaseConnection(db_path)
    assert db_conn.connection is None
    assert db_conn.db_path == db_path

# happy_path - test_database_connect - Test that the database connection can be established successfully
def test_database_connect(mock_sqlite3_connect):
    db_path = '/mocked/dir/shopping_cart.db'
    db_conn = DatabaseConnection(db_path)
    db_conn.connect()
    mock_sqlite3_connect.assert_called_once_with(db_path)
    assert db_conn.connection is not None

# happy_path - test_execute_query_without_params - Test that a query is executed successfully without parameters
def test_execute_query_without_params(mock_sqlite3_connect):
    _, mock_conn, mock_cursor = mock_sqlite3_connect
    db_conn = DatabaseConnection('/mocked/dir/shopping_cart.db')
    db_conn.connect()
    query = 'CREATE TABLE IF NOT EXISTS cart (id INTEGER PRIMARY KEY)'
    db_conn.execute(query)
    mock_cursor.execute.assert_called_once_with(query, [])

# happy_path - test_fetchone_retrieves_single_row - Test that fetchone retrieves a single row from the database
def test_fetchone_retrieves_single_row(mock_sqlite3_connect):
    _, mock_conn, mock_cursor = mock_sqlite3_connect
    mock_cursor.fetchone.return_value = ('item1',)
    db_conn = DatabaseConnection('/mocked/dir/shopping_cart.db')
    db_conn.connect()
    query = 'SELECT * FROM cart WHERE id = ?'
    result = db_conn.fetchone(query, [1])
    mock_cursor.execute.assert_called_once_with(query, [1])
    assert result == ('item1',)

# happy_path - test_fetchall_retrieves_all_rows - Test that fetchall retrieves all rows from the database
def test_fetchall_retrieves_all_rows(mock_sqlite3_connect):
    _, mock_conn, mock_cursor = mock_sqlite3_connect
    mock_cursor.fetchall.return_value = [('item1',), ('item2',)]
    db_conn = DatabaseConnection('/mocked/dir/shopping_cart.db')
    db_conn.connect()
    query = 'SELECT * FROM cart'
    results = db_conn.fetchall(query)
    mock_cursor.execute.assert_called_once_with(query, [])
    assert results == [('item1',), ('item2',)]

# edge_case - test_execute_malformed_query - Test that execute raises an error when the query is malformed
def test_execute_malformed_query(mock_sqlite3_connect):
    _, mock_conn, mock_cursor = mock_sqlite3_connect
    mock_cursor.execute.side_effect = sqlite3.Error
    db_conn = DatabaseConnection('/mocked/dir/shopping_cart.db')
    db_conn.connect()
    query = 'MALFORMED QUERY'
    with pytest.raises(sqlite3.Error):
        db_conn.execute(query)

# edge_case - test_fetchone_no_matching_rows - Test that fetchone returns None when no rows match the query
def test_fetchone_no_matching_rows(mock_sqlite3_connect):
    _, mock_conn, mock_cursor = mock_sqlite3_connect
    mock_cursor.fetchone.return_value = None
    db_conn = DatabaseConnection('/mocked/dir/shopping_cart.db')
    db_conn.connect()
    query = 'SELECT * FROM cart WHERE id = ?'
    result = db_conn.fetchone(query, [999])
    mock_cursor.execute.assert_called_once_with(query, [999])
    assert result is None

# edge_case - test_fetchall_empty_table - Test that fetchall returns an empty list when no rows are in the table
def test_fetchall_empty_table(mock_sqlite3_connect):
    _, mock_conn, mock_cursor = mock_sqlite3_connect
    mock_cursor.fetchall.return_value = []
    db_conn = DatabaseConnection('/mocked/dir/shopping_cart.db')
    db_conn.connect()
    query = 'SELECT * FROM empty_table'
    results = db_conn.fetchall(query)
    mock_cursor.execute.assert_called_once_with(query, [])
    assert results == []

# edge_case - test_commit_no_changes - Test that commit does nothing when there are no changes to commit
def test_commit_no_changes(mock_sqlite3_connect):
    _, mock_conn, _ = mock_sqlite3_connect
    db_conn = DatabaseConnection('/mocked/dir/shopping_cart.db')
    db_conn.connect()
    db_conn.commit()
    mock_conn.commit.assert_called_once()

# edge_case - test_close_multiple_times - Test that close can be called multiple times without error
def test_close_multiple_times(mock_sqlite3_connect):
    _, mock_conn, _ = mock_sqlite3_connect
    db_conn = DatabaseConnection('/mocked/dir/shopping_cart.db')
    db_conn.connect()
    db_conn.close()
    db_conn.close()
    mock_conn.close.assert_called_once()
    assert db_conn.connection is None

