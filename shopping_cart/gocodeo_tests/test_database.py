import pytest
from unittest import mock
import sqlite3
import os
from your_module import DatabaseConnection, add_item_to_cart_db

@pytest.fixture
def mock_db_connection():
    with mock.patch('your_module.sqlite3.connect') as mock_connect:
        mock_connection = mock.Mock()
        mock_connect.return_value = mock_connection
        yield mock_connection

@pytest.fixture
def mock_cursor(mock_db_connection):
    mock_cursor = mock.Mock()
    mock_db_connection.cursor.return_value = mock_cursor
    yield mock_cursor

@pytest.fixture
def mock_os_path():
    with mock.patch('your_module.os.path') as mock_path:
        mock_path.dirname.return_value = '/mock/dir'
        mock_path.abspath.return_value = '/mock/dir/shopping_cart.db'
        mock_path.join.return_value = '/mock/dir/shopping_cart.db'
        yield mock_path

# happy_path - test_init_with_valid_db_path - Test that DatabaseConnection initializes with a valid db_path
def test_init_with_valid_db_path():
    db_path = 'valid/path/to/db'
    db_conn = DatabaseConnection(db_path)
    assert db_conn.db_path == 'valid/path/to/db'
    assert db_conn.connection is None


# happy_path - test_connect_establishes_connection - Test that connect method establishes a connection to the database
def test_connect_establishes_connection(mock_db_connection):
    db_conn = DatabaseConnection('valid/path/to/db')
    db_conn.connect()
    mock_db_connection.cursor.assert_called_once()


# happy_path - test_execute_valid_query_without_params - Test that execute runs a valid SQL query without parameters
def test_execute_valid_query_without_params(mock_db_connection, mock_cursor):
    db_conn = DatabaseConnection('valid/path/to/db')
    db_conn.connect()
    db_conn.execute('CREATE TABLE test (id INTEGER)')
    mock_cursor.execute.assert_called_once_with('CREATE TABLE test (id INTEGER)', [])


# happy_path - test_fetchone_retrieves_single_record - Test that fetchone retrieves a single record
def test_fetchone_retrieves_single_record(mock_db_connection, mock_cursor):
    db_conn = DatabaseConnection('valid/path/to/db')
    db_conn.connect()
    mock_cursor.fetchone.return_value = (1,)
    result = db_conn.fetchone('SELECT * FROM test WHERE id = ?', [1])
    mock_cursor.execute.assert_called_once_with('SELECT * FROM test WHERE id = ?', [1])
    assert result == (1,)


# happy_path - test_fetchall_retrieves_multiple_records - Test that fetchall retrieves multiple records
def test_fetchall_retrieves_multiple_records(mock_db_connection, mock_cursor):
    db_conn = DatabaseConnection('valid/path/to/db')
    db_conn.connect()
    mock_cursor.fetchall.return_value = [(1,), (2,)]
    results = db_conn.fetchall('SELECT * FROM test')
    mock_cursor.execute.assert_called_once_with('SELECT * FROM test', [])
    assert results == [(1,), (2,)]


# happy_path - test_commit_saves_changes - Test that commit saves changes to the database
def test_commit_saves_changes(mock_db_connection):
    db_conn = DatabaseConnection('valid/path/to/db')
    db_conn.connect()
    db_conn.commit()
    mock_db_connection.commit.assert_called_once()


# happy_path - test_close_closes_connection - Test that close method closes the database connection
def test_close_closes_connection(mock_db_connection):
    db_conn = DatabaseConnection('valid/path/to/db')
    db_conn.connect()
    db_conn.close()
    mock_db_connection.close.assert_called_once()


# happy_path - test_add_item_to_cart_db_adds_item - Test that add_item_to_cart_db adds an item to the cart
def test_add_item_to_cart_db_adds_item(mock_db_connection, mock_cursor):
    add_item_to_cart_db('INSERT INTO cart (item) VALUES (?)', ['apple'])
    mock_cursor.execute.assert_called_once_with('INSERT INTO cart (item) VALUES (?)', ['apple'])
    mock_db_connection.commit.assert_called_once()


# happy_path - test_init_with_valid_path - Test that the database connection is initialized with the correct path.
def test_init_with_valid_path():
    db_path = 'valid_path.db'
    db_conn = DatabaseConnection(db_path)
    assert db_conn.db_path == 'valid_path.db'
    assert db_conn.connection is None


# happy_path - test_connect_with_valid_path - Test that the connection is successfully established with a valid database path.
def test_connect_with_valid_path(mock_db_connection):
    db_conn = DatabaseConnection('valid/path/to/db')
    db_conn.connect()
    mock_db_connection.cursor.assert_called_once()


# happy_path - test_execute_valid_query_no_params - Test that a valid query is executed successfully without parameters.
def test_execute_valid_query_no_params(mock_db_connection, mock_cursor):
    db_conn = DatabaseConnection('valid/path/to/db')
    db_conn.connect()
    db_conn.execute('CREATE TABLE test (id INTEGER)')
    mock_cursor.execute.assert_called_once_with('CREATE TABLE test (id INTEGER)', [])


# happy_path - test_fetchone_valid_query - Test that fetchone returns a single row from the database when a valid query is provided.
def test_fetchone_valid_query(mock_db_connection, mock_cursor):
    db_conn = DatabaseConnection('valid/path/to/db')
    db_conn.connect()
    mock_cursor.fetchone.return_value = {'id': 1}
    result = db_conn.fetchone('SELECT * FROM test WHERE id = 1')
    mock_cursor.execute.assert_called_once_with('SELECT * FROM test WHERE id = 1', [])
    assert result == {'id': 1}


# happy_path - test_fetchall_valid_query - Test that fetchall returns multiple rows from the database when a valid query is provided.
def test_fetchall_valid_query(mock_db_connection, mock_cursor):
    db_conn = DatabaseConnection('valid/path/to/db')
    db_conn.connect()
    mock_cursor.fetchall.return_value = [{'id': 1}, {'id': 2}]
    results = db_conn.fetchall('SELECT * FROM test')
    mock_cursor.execute.assert_called_once_with('SELECT * FROM test', [])
    assert results == [{'id': 1}, {'id': 2}]


# edge_case - test_init_with_invalid_db_path - Test that DatabaseConnection initializes with an invalid db_path
def test_init_with_invalid_db_path():
    db_path = 'invalid/path/to/db'
    db_conn = DatabaseConnection(db_path)
    assert db_conn.db_path == 'invalid/path/to/db'
    assert db_conn.connection is None


# edge_case - test_connect_fails_with_invalid_db_path - Test that connect method fails with invalid db_path
def test_connect_fails_with_invalid_db_path(mock_db_connection):
    db_conn = DatabaseConnection('invalid/path/to/db')
    with pytest.raises(sqlite3.OperationalError):
        db_conn.connect()


# edge_case - test_execute_invalid_query - Test that execute raises an error with invalid SQL query
def test_execute_invalid_query(mock_db_connection, mock_cursor):
    db_conn = DatabaseConnection('valid/path/to/db')
    db_conn.connect()
    mock_cursor.execute.side_effect = sqlite3.Error
    with pytest.raises(sqlite3.Error):
        db_conn.execute('INVALID SQL')


# edge_case - test_fetchone_returns_none_for_non_existent_record - Test that fetchone returns None for non-existent record
def test_fetchone_returns_none_for_non_existent_record(mock_db_connection, mock_cursor):
    db_conn = DatabaseConnection('valid/path/to/db')
    db_conn.connect()
    mock_cursor.fetchone.return_value = None
    result = db_conn.fetchone('SELECT * FROM test WHERE id = ?', [999])
    mock_cursor.execute.assert_called_once_with('SELECT * FROM test WHERE id = ?', [999])
    assert result is None


# edge_case - test_fetchall_returns_empty_list_for_no_records - Test that fetchall returns empty list for no records
def test_fetchall_returns_empty_list_for_no_records(mock_db_connection, mock_cursor):
    db_conn = DatabaseConnection('valid/path/to/db')
    db_conn.connect()
    mock_cursor.fetchall.return_value = []
    results = db_conn.fetchall('SELECT * FROM test WHERE id > ?', [999])
    mock_cursor.execute.assert_called_once_with('SELECT * FROM test WHERE id > ?', [999])
    assert results == []


# edge_case - test_commit_no_changes - Test that commit does nothing when no changes made
def test_commit_no_changes(mock_db_connection):
    db_conn = DatabaseConnection('valid/path/to/db')
    db_conn.connect()
    db_conn.commit()
    mock_db_connection.commit.assert_called_once()


# edge_case - test_close_handles_already_closed_connection - Test that close method handles already closed connection
def test_close_handles_already_closed_connection(mock_db_connection):
    db_conn = DatabaseConnection('valid/path/to/db')
    db_conn.connect()
    db_conn.close()
    db_conn.close()  # Close again
    mock_db_connection.close.assert_called_once()


# edge_case - test_add_item_to_cart_db_handles_empty_params - Test that add_item_to_cart_db handles empty parameters
def test_add_item_to_cart_db_handles_empty_params(mock_db_connection, mock_cursor):
    with pytest.raises(sqlite3.Error):
        add_item_to_cart_db('INSERT INTO cart (item) VALUES (?)', [])


# edge_case - test_init_with_empty_path - Test that the database connection is initialized with an empty path.
def test_init_with_empty_path():
    db_path = ''
    db_conn = DatabaseConnection(db_path)
    assert db_conn.db_path == ''
    assert db_conn.connection is None


# edge_case - test_connect_with_invalid_path - Test that connect raises an error when the database path is invalid.
def test_connect_with_invalid_path(mock_db_connection):
    db_conn = DatabaseConnection('/invalid/path/to/db')
    with pytest.raises(sqlite3.OperationalError):
        db_conn.connect()


# edge_case - test_execute_invalid_query - Test that execute raises an error when an invalid SQL query is provided.
def test_execute_invalid_query(mock_db_connection, mock_cursor):
    db_conn = DatabaseConnection('valid/path/to/db')
    db_conn.connect()
    mock_cursor.execute.side_effect = sqlite3.OperationalError('near "INVALID": syntax error')
    with pytest.raises(sqlite3.OperationalError) as excinfo:
        db_conn.execute('INVALID SQL')
    assert 'near "INVALID": syntax error' in str(excinfo.value)


# edge_case - test_fetchone_no_matching_rows - Test that fetchone returns None when no matching rows are found.
def test_fetchone_no_matching_rows(mock_db_connection, mock_cursor):
    db_conn = DatabaseConnection('valid/path/to/db')
    db_conn.connect()
    mock_cursor.fetchone.return_value = None
    result = db_conn.fetchone('SELECT * FROM test WHERE id = 999')
    mock_cursor.execute.assert_called_once_with('SELECT * FROM test WHERE id = 999', [])
    assert result is None


# edge_case - test_fetchall_no_rows - Test that fetchall returns an empty list when no rows are found.
def test_fetchall_no_rows(mock_db_connection, mock_cursor):
    db_conn = DatabaseConnection('valid/path/to/db')
    db_conn.connect()
    mock_cursor.fetchall.return_value = []
    results = db_conn.fetchall('SELECT * FROM test WHERE id > 999')
    mock_cursor.execute.assert_called_once_with('SELECT * FROM test WHERE id > 999', [])
    assert results == []


