import pytest
from unittest import mock
import sqlite3

@pytest.fixture
def mock_database():
    with mock.patch('sqlite3.connect') as mock_connect:
        mock_conn = mock.Mock()
        mock_cursor = mock.Mock()
        
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        
        yield mock_conn, mock_cursor

        mock_conn.close.assert_called_once()

# happy path - execute - Test that the 'cart' table is successfully dropped if it exists.
def test_drop_table_if_exists(mock_database):
    mock_conn, mock_cursor = mock_database
    
    # Simulate executing the drop table query
    mock_cursor.execute.return_value = None
    
    # Call the function to test
    drop_table_if_exists()
    
    # Check if the drop table query was executed
    mock_cursor.execute.assert_called_with('DROP TABLE IF EXISTS cart;')
    
    # Check if the transaction was committed
    mock_conn.commit.assert_called_once()


# happy path - execute - Test that the 'cart' table is created successfully with all specified columns.
def test_create_cart_table(mock_database):
    mock_conn, mock_cursor = mock_database
    
    # Simulate executing the create table query
    mock_cursor.execute.return_value = None
    
    # Call the function to test
    create_cart_table()
    
    # Check if the create table query was executed
    mock_cursor.execute.assert_called_with('CREATE TABLE cart (id INTEGER PRIMARY KEY, item_id INTEGER, name TEXT, price REAL, quantity INTEGER, category TEXT, user_type TEXT, payment_status);')
    
    # Check if the transaction was committed
    mock_conn.commit.assert_called_once()


# happy path - commit - Test committing the transaction after table creation.
def test_commit_transaction(mock_database):
    mock_conn, mock_cursor = mock_database
    
    # Simulate executing queries
    mock_cursor.execute.return_value = None
    
    # Call the function to test
    commit_transaction()
    
    # Verify commit was called
    mock_conn.commit.assert_called_once()


# happy path - close - Test that the connection to the database is closed successfully.
def test_close_connection(mock_database):
    mock_conn, mock_cursor = mock_database
    
    # Call the function to test
    close_connection()
    
    # Verify close was called
    mock_conn.close.assert_called_once()


# happy path - cursor - Test cursor object creation for executing SQL commands.
def test_create_cursor_object(mock_database):
    mock_conn, mock_cursor = mock_database
    
    # Call the function to test
    create_cursor_object()
    
    # Verify cursor creation
    mock_conn.cursor.assert_called_once()


# edge case - execute - Test dropping a table when no tables exist in the database.
def test_drop_table_no_exist(mock_database):
    mock_conn, mock_cursor = mock_database
    
    # Simulate executing the drop table query
    mock_cursor.execute.return_value = None
    
    # Call the function to test
    drop_table_no_exist()
    
    # Check if the drop table query was executed
    mock_cursor.execute.assert_called_with('DROP TABLE IF EXISTS non_existing_table;')
    
    # Check if the transaction was committed
    mock_conn.commit.assert_called_once()


# edge case - execute - Test creating a table with an already existing name.
def test_create_existing_table_name(mock_database):
    mock_conn, mock_cursor = mock_database
    
    # Simulate raising an error for table already exists
    mock_cursor.execute.side_effect = sqlite3.OperationalError('Table already exists.')
    
    # Call the function to test
    with pytest.raises(sqlite3.OperationalError, match='Table already exists.'):
        create_existing_table_name()


# edge case - execute - Test that creating a table without specifying a primary key results in an error.
def test_create_table_without_primary_key(mock_database):
    mock_conn, mock_cursor = mock_database
    
    # Simulate raising an error for missing primary key
    mock_cursor.execute.side_effect = sqlite3.OperationalError('Primary key required.')
    
    # Call the function to test
    with pytest.raises(sqlite3.OperationalError, match='Primary key required.'):
        create_table_without_primary_key()


# edge case - execute - Test creating a table with invalid SQL syntax.
def test_create_table_invalid_syntax(mock_database):
    mock_conn, mock_cursor = mock_database
    
    # Simulate raising an error for syntax error
    mock_cursor.execute.side_effect = sqlite3.OperationalError('Syntax error in SQL statement.')
    
    # Call the function to test
    with pytest.raises(sqlite3.OperationalError, match='Syntax error in SQL statement.'):
        create_table_invalid_syntax()


# edge case - commit - Test committing a transaction when no changes have been made.
def test_commit_no_changes(mock_database):
    mock_conn, mock_cursor = mock_database
    
    # Simulate executing queries
    mock_cursor.execute.return_value = None
    
    # Call the function to test
    commit_no_changes()
    
    # Verify commit was called
    mock_conn.commit.assert_called_once()


