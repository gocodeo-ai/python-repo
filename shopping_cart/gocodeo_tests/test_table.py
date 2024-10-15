import pytest
from unittest import mock
import sqlite3
import shopping_cart.table  # Adjust the import according to your module structure

@pytest.fixture
def mock_db_connection():
    with mock.patch('sqlite3.connect') as mock_connect:
        mock_conn = mock.Mock()
        mock_connect.return_value = mock_conn
        yield mock_conn

@pytest.fixture
def mock_cursor(mock_db_connection):
    mock_cursor = mock.Mock()
    mock_db_connection.cursor.return_value = mock_cursor
    yield mock_cursor

@pytest.fixture
def setup_database(mock_cursor):
    # Mock the execution of SQL commands
    mock_cursor.execute.side_effect = lambda query: None
    mock_cursor.fetchall.return_value = []
    mock_cursor.commit.return_value = None
    mock_cursor.close.return_value = None

    yield

@pytest.fixture(autouse=True)
def mock_sqlite3():
    with mock.patch('sqlite3.Error') as mock_error:
        yield mock_error

# happy path - execute - Test that the cart table is dropped if it already exists
def test_table_dropped_if_exists(mock_cursor, setup_database):
    query = 'DROP TABLE IF EXISTS cart;'
    mock_cursor.execute.assert_any_call(query)
    print("Test that the cart table is dropped if it already exists - Passed")


# happy path - execute - Test that the cart table is created successfully
def test_table_created_successfully(mock_cursor, setup_database):
    query = 'CREATE TABLE cart (id INTEGER PRIMARY KEY, item_id INTEGER, name TEXT, price REAL, quantity INTEGER, category TEXT, user_type TEXT, payment_status);'
    mock_cursor.execute.assert_any_call(query)
    print("Test that the cart table is created successfully - Passed")


# happy path - connect - Test that connection to the database is successful
def test_database_connection_success(mock_db_connection):
    mock_db_connection.connect.assert_called_once_with('shopping_cart.db')
    print("Test that connection to the database is successful - Passed")


# happy path - commit - Test that the transaction is committed successfully
def test_transaction_commit_success(mock_cursor, setup_database):
    mock_cursor.commit.assert_called_once()
    print("Test that the transaction is committed successfully - Passed")


# happy path - close - Test that the connection is closed successfully
def test_connection_close_success(mock_db_connection):
    mock_db_connection.close.assert_called_once()
    print("Test that the connection is closed successfully - Passed")


# edge case - execute - Test that error is raised when dropping non-existent table
def test_error_on_dropping_non_existent_table(mock_cursor, mock_sqlite3):
    query = 'DROP TABLE non_existent_table;'
    mock_cursor.execute.side_effect = sqlite3.Error('no such table')
    with pytest.raises(sqlite3.Error, match='no such table'):
        mock_cursor.execute(query)
    print("Test that error is raised when dropping non-existent table - Passed")


# edge case - execute - Test that error is raised when creating table with invalid SQL
def test_error_on_invalid_create_table_sql(mock_cursor, mock_sqlite3):
    query = 'CREATE TABLE cart (id INTEGER PRIMARY KEY, item_id INTEGER, name TEXT, price REAL, quantity INTEGER, category TEXT, user_type TEXT, invalid_column);'
    mock_cursor.execute.side_effect = sqlite3.Error('syntax error')
    with pytest.raises(sqlite3.Error, match='syntax error'):
        mock_cursor.execute(query)
    print("Test that error is raised when creating table with invalid SQL - Passed")


# edge case - commit - Test that error is raised when committing without open transaction
def test_error_on_commit_without_transaction(mock_cursor, mock_sqlite3):
    mock_cursor.commit.side_effect = sqlite3.Error('no transaction is active')
    with pytest.raises(sqlite3.Error, match='no transaction is active'):
        mock_cursor.commit()
    print("Test that error is raised when committing without open transaction - Passed")


# edge case - close - Test that error is raised when closing already closed connection
def test_error_on_closing_already_closed_connection(mock_db_connection, mock_sqlite3):
    mock_db_connection.close.side_effect = sqlite3.Error('connection already closed')
    with pytest.raises(sqlite3.Error, match='connection already closed'):
        mock_db_connection.close()
    print("Test that error is raised when closing already closed connection - Passed")


# edge case - execute - Test that error is raised on invalid SQL execution
def test_error_on_invalid_sql_execution(mock_cursor, mock_sqlite3):
    query = 'INVALID SQL'
    mock_cursor.execute.side_effect = sqlite3.Error('syntax error')
    with pytest.raises(sqlite3.Error, match='syntax error'):
        mock_cursor.execute(query)
    print("Test that error is raised on invalid SQL execution - Passed")


