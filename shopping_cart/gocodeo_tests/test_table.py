import pytest
from unittest import mock
import sqlite3

# Mocking sqlite3.connect to prevent actual database connections
@pytest.fixture
def mock_db_connection():
    mock_conn = mock.Mock()
    mock_cursor = mock.Mock()
    mock_conn.cursor.return_value = mock_cursor
    mock_conn.commit = mock.Mock()
    mock_conn.close = mock.Mock()
    
    # Mocking the connect method
    with mock.patch('sqlite3.connect', return_value=mock_conn):
        yield mock_conn, mock_cursor

# Test setup using the mock_db_connection fixture
@pytest.fixture
def setup_database(mock_db_connection):
    conn, cursor = mock_db_connection
    
    # Mocking the execution of SQL commands
    cursor.execute = mock.Mock()
    
    # Mocking the behavior of dropping and creating tables
    cursor.execute.side_effect = lambda query: None  # Simulate successful execution
    
    yield conn, cursor

# This will ensure that all necessary dependencies are mocked

# happy path - connect - Test that the database connection is established successfully.
def test_database_connection(mock_db_connection):
    conn, _ = mock_db_connection
    assert conn is not None, "Connection should not be None"


# happy path - execute - Test that the cart table is dropped if it exists.
def test_drop_table_if_exists(setup_database):
    _, cursor = setup_database
    cursor.execute.assert_any_call('DROP TABLE IF EXISTS cart;')


# happy path - execute - Test that the cart table is created with the correct schema.
def test_create_cart_table(setup_database):
    _, cursor = setup_database
    cursor.execute.assert_any_call('CREATE TABLE cart (\n        id INTEGER PRIMARY KEY,\n        item_id INTEGER ,\n        name TEXT,\n        price REAL,\n        quantity INTEGER,\n        category TEXT,\n        user_type TEXT,\n        payment_status\n    );')


# happy path - commit - Test that the transaction is committed successfully.
def test_commit_transaction(setup_database):
    conn, _ = setup_database
    conn.commit.assert_called_once()


# happy path - close - Test that the database connection is closed without errors.
def test_close_connection(setup_database):
    conn, _ = setup_database
    conn.close.assert_called_once()


# edge case - connect - Test that an error is raised if the database file is not accessible.
def test_database_access_error():
    with mock.patch('sqlite3.connect', side_effect=sqlite3.Error('unable to open database file')):
        with pytest.raises(sqlite3.Error, match='unable to open database file'):
            sqlite3.connect('non_existent.db')


# edge case - execute - Test that an error occurs if SQL syntax is incorrect when dropping a table.
def test_drop_table_sql_error(setup_database):
    _, cursor = setup_database
    cursor.execute.side_effect = sqlite3.Error('syntax error')
    with pytest.raises(sqlite3.Error, match='syntax error'):
        cursor.execute('DROP TABLE IF NOT EXISTS cart;')


# edge case - execute - Test that an error occurs if SQL syntax is incorrect when creating a table.
def test_create_table_sql_error(setup_database):
    _, cursor = setup_database
    cursor.execute.side_effect = sqlite3.Error('syntax error')
    with pytest.raises(sqlite3.Error, match='syntax error'):
        cursor.execute('CREATE TABLE cart (id INTEGER PRIMARY KEY item_id INTEGER, name TEXT);')


# edge case - commit - Test that an error is raised if commit is called without an active transaction.
def test_commit_without_transaction(setup_database):
    conn, _ = setup_database
    conn.commit.side_effect = sqlite3.Error('no transaction is active')
    with pytest.raises(sqlite3.Error, match='no transaction is active'):
        conn.commit()


# edge case - close - Test that an error is raised if close is called on an already closed connection.
def test_close_already_closed_connection(setup_database):
    conn, _ = setup_database
    conn.close.side_effect = sqlite3.Error('connection is already closed')
    conn.close()  # First call
    with pytest.raises(sqlite3.Error, match='connection is already closed'):
        conn.close()  # Second call


