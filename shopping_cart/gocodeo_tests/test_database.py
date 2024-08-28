import pytest
from unittest import mock
import sqlite3

@pytest.fixture
def mock_sqlite_connect():
    with mock.patch('sqlite3.connect') as mock_connect:
        mock_connection = mock.Mock()
        mock_connect.return_value = mock_connection
        yield mock_connect, mock_connection

@pytest.fixture
def mock_cursor(mock_sqlite_connect):
    mock_connect, mock_connection = mock_sqlite_connect
    mock_cursor = mock.Mock()
    mock_connection.cursor.return_value = mock_cursor
    yield mock_cursor

@pytest.fixture
def mock_db_connection(mock_sqlite_connect):
    from your_module import DatabaseConnection
    db_connection = DatabaseConnection("shopping_cart.db")
    yield db_connection

# happy_path - test_init_with_valid_db_path - Test that the database connection is initialized with a valid path
def test_init_with_valid_db_path():
    db_connection = DatabaseConnection('shopping_cart.db')
    assert db_connection.connection is None
    assert db_connection.db_path == 'shopping_cart.db'

# happy_path - test_connect_successful - Test that the database connection is established successfully
def test_connect_successful(mock_sqlite_connect):
    db_connection = DatabaseConnection('shopping_cart.db')
    db_connection.connect()
    mock_sqlite_connect.assert_called_once_with('shopping_cart.db')
    assert db_connection.connection is not None

# happy_path - test_execute_query_without_params - Test that a query is executed successfully without parameters
def test_execute_query_without_params(mock_cursor, mock_db_connection):
    query = 'CREATE TABLE test (id INTEGER)'
    mock_db_connection.execute(query)
    mock_cursor.execute.assert_called_once_with(query, [])

# happy_path - test_fetchone_returns_single_row - Test that fetchone returns a single row
def test_fetchone_returns_single_row(mock_cursor, mock_db_connection):
    mock_cursor.fetchone.return_value = ('row',)
    query = 'SELECT * FROM test WHERE id = 1'
    result = mock_db_connection.fetchone(query)
    mock_cursor.execute.assert_called_once_with(query, [])
    assert result == ('row',)

# happy_path - test_fetchall_returns_all_rows - Test that fetchall returns all rows
def test_fetchall_returns_all_rows(mock_cursor, mock_db_connection):
    mock_cursor.fetchall.return_value = [('row1',), ('row2',)]
    query = 'SELECT * FROM test'
    results = mock_db_connection.fetchall(query)
    mock_cursor.execute.assert_called_once_with(query, [])
    assert results == [('row1',), ('row2',)]

# edge_case - test_init_with_empty_db_path - Test that initializing with an empty database path raises an error
def test_init_with_empty_db_path():
    with pytest.raises(sqlite3.OperationalError):
        DatabaseConnection('')

# edge_case - test_connect_non_existent_db - Test that connecting to a non-existent database raises an error
def test_connect_non_existent_db():
    with pytest.raises(sqlite3.OperationalError):
        db_connection = DatabaseConnection('non_existent.db')
        db_connection.connect()

# edge_case - test_execute_malformed_query - Test that executing a malformed query raises an error
def test_execute_malformed_query(mock_cursor, mock_db_connection):
    mock_cursor.execute.side_effect = sqlite3.OperationalError
    query = 'MALFORMED QUERY'
    with pytest.raises(sqlite3.OperationalError):
        mock_db_connection.execute(query)

# edge_case - test_fetchone_no_result - Test that fetchone returns None for a non-existent row
def test_fetchone_no_result(mock_cursor, mock_db_connection):
    mock_cursor.fetchone.return_value = None
    query = 'SELECT * FROM test WHERE id = 999'
    result = mock_db_connection.fetchone(query)
    mock_cursor.execute.assert_called_once_with(query, [])
    assert result is None

# edge_case - test_fetchall_empty_table - Test that fetchall returns an empty list for an empty table
def test_fetchall_empty_table(mock_cursor, mock_db_connection):
    mock_cursor.fetchall.return_value = []
    query = 'SELECT * FROM empty_table'
    results = mock_db_connection.fetchall(query)
    mock_cursor.execute.assert_called_once_with(query, [])
    assert results == []

