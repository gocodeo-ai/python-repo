import pytest
from unittest import mock
import sqlite3

# Mocking the sqlite3 module
@pytest.fixture
def mock_sqlite3():
    with mock.patch('sqlite3.connect') as mock_connect:
        mock_cursor = mock.Mock()
        mock_connect.return_value.cursor.return_value = mock_cursor
        mock_connect.return_value.commit = mock.Mock()
        mock_connect.return_value.close = mock.Mock()
        yield mock_connect, mock_cursor

# Test setup using the mocked dependencies
@pytest.fixture
def setup_database(mock_sqlite3):
    mock_connect, mock_cursor = mock_sqlite3

    # Mock the execution of SQL commands
    mock_cursor.execute = mock.Mock()
    mock_cursor.execute.side_effect = lambda query: None  # Simulate successful execution

    # Mock the commit to simulate a successful transaction
    mock_connect.return_value.commit = mock.Mock()

    # Mock the close method
    mock_connect.return_value.close = mock.Mock()

    return mock_connect, mock_cursor

# happy path - execute - Test that the 'cart' table is created successfully with all columns.
def test_create_cart_table(setup_database):
    mock_connect, mock_cursor = setup_database
    
    # Call the function to create the table
    from shopping_cart.table import create_cart_table
    create_cart_table()
    
    # Check if the create table query was executed
    mock_cursor.execute.assert_any_call('CREATE TABLE cart (id INTEGER PRIMARY KEY, item_id INTEGER, name TEXT, price REAL, quantity INTEGER, category TEXT, user_type TEXT, payment_status)')
    
    # Check if the success message was printed
    mock_connect.return_value.commit.assert_called_once()


# happy path - execute - Test that the 'cart' table is dropped if it exists before creation.
def test_drop_cart_table_if_exists(setup_database):
    mock_connect, mock_cursor = setup_database
    
    # Call the function to drop the table
    from shopping_cart.table import drop_cart_table_if_exists
    drop_cart_table_if_exists()
    
    # Check if the drop table query was executed
    mock_cursor.execute.assert_any_call('DROP TABLE IF EXISTS cart')
    
    # Check if the success status is true
    assert mock_cursor.execute.call_count > 0


# happy path - connect - Test that the connection to the SQLite database is established successfully.
def test_database_connection(mock_sqlite3):
    mock_connect, _ = mock_sqlite3
    
    # Call the function to connect to the database
    from shopping_cart.table import connect_to_database
    connection = connect_to_database('shopping_cart.db')
    
    # Check if the connection was established
    mock_connect.assert_called_with('shopping_cart.db')
    assert connection is not None


# happy path - execute - Test that the SQL commands are executed without any errors.
def test_execute_sql_commands(setup_database):
    mock_connect, mock_cursor = setup_database
    
    # Call the function to execute SQL commands
    from shopping_cart.table import execute_sql_commands
    execute_sql_commands(['DROP TABLE IF EXISTS cart', 'CREATE TABLE cart (id INTEGER PRIMARY KEY, item_id INTEGER, name TEXT, price REAL, quantity INTEGER, category TEXT, user_type TEXT, payment_status)'])
    
    # Check if the SQL commands were executed
    mock_cursor.execute.assert_any_call('DROP TABLE IF EXISTS cart')
    mock_cursor.execute.assert_any_call('CREATE TABLE cart (id INTEGER PRIMARY KEY, item_id INTEGER, name TEXT, price REAL, quantity INTEGER, category TEXT, user_type TEXT, payment_status)')
    
    # Check if the execution status is success
    assert mock_cursor.execute.call_count > 0


# happy path - commit - Test that the transaction is committed successfully.
def test_commit_transaction(setup_database):
    mock_connect, _ = setup_database
    
    # Call the function to commit the transaction
    from shopping_cart.table import commit_transaction
    commit_transaction()
    
    # Check if the transaction was committed
    mock_connect.return_value.commit.assert_called_once()


# edge case - execute - Test that an error is raised if the 'cart' table creation query has syntax errors.
def test_create_table_syntax_error(setup_database):
    mock_connect, mock_cursor = setup_database
    
    # Simulate a syntax error
    mock_cursor.execute.side_effect = sqlite3.Error('syntax error')
    
    # Call the function to create the table
    from shopping_cart.table import create_cart_table_with_error
    with pytest.raises(sqlite3.Error) as excinfo:
        create_cart_table_with_error()
    
    # Check if the error message is as expected
    assert 'syntax error' in str(excinfo.value)


# edge case - connect - Test that an error is raised if the database file path is invalid.
def test_invalid_database_path(mock_sqlite3):
    mock_connect, _ = mock_sqlite3
    
    # Simulate an error when opening the database
    mock_connect.side_effect = sqlite3.Error('unable to open database file')
    
    # Call the function to connect to the database
    from shopping_cart.table import connect_to_database
    with pytest.raises(sqlite3.Error) as excinfo:
        connect_to_database('invalid_path/shopping_cart.db')
    
    # Check if the error message is as expected
    assert 'unable to open database file' in str(excinfo.value)


# edge case - close - Test that the connection is closed even if an error occurs during SQL execution.
def test_connection_closed_on_error(setup_database):
    mock_connect, mock_cursor = setup_database
    
    # Simulate an error during SQL execution
    mock_cursor.execute.side_effect = sqlite3.Error('execution error')
    
    # Call the function to execute SQL commands
    from shopping_cart.table import execute_sql_with_error
    with pytest.raises(sqlite3.Error):
        execute_sql_with_error()
    
    # Check if the connection was closed
    mock_connect.return_value.close.assert_called_once()


# edge case - execute - Test that an error is raised if the 'cart' table already exists without the IF EXISTS clause.
def test_drop_table_without_if_exists(setup_database):
    mock_connect, mock_cursor = setup_database
    
    # Simulate an error for dropping a non-existent table
    mock_cursor.execute.side_effect = sqlite3.Error('no such table: cart')
    
    # Call the function to drop the table
    from shopping_cart.table import drop_table_without_if_exists
    with pytest.raises(sqlite3.Error) as excinfo:
        drop_table_without_if_exists()
    
    # Check if the error message is as expected
    assert 'no such table: cart' in str(excinfo.value)


# edge case - execute - Test that an error is raised if the 'cart' table is created with duplicate column names.
def test_create_table_duplicate_columns(setup_database):
    mock_connect, mock_cursor = setup_database
    
    # Simulate a duplicate column name error
    mock_cursor.execute.side_effect = sqlite3.Error('duplicate column name: id')
    
    # Call the function to create the table
    from shopping_cart.table import create_table_with_duplicate_columns
    with pytest.raises(sqlite3.Error) as excinfo:
        create_table_with_duplicate_columns()
    
    # Check if the error message is as expected
    assert 'duplicate column name: id' in str(excinfo.value)


