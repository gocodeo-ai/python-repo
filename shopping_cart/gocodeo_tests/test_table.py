import pytest
from unittest import mock
import sqlite3
import shopping_cart.table  # Adjust the import based on your actual module structure

@pytest.fixture
def mock_db_setup():
    # Mock the sqlite3.connect method
    mock_connect = mock.patch('sqlite3.connect', return_value=mock.Mock()).start()
    
    # Mock the cursor method
    mock_cursor = mock.Mock()
    mock_connect.return_value.cursor.return_value = mock_cursor
    
    # Mock the execute method of the cursor
    mock_cursor.execute = mock.Mock()
    
    # Mock the commit method of the connection
    mock_connect.return_value.commit = mock.Mock()
    
    # Mock the close method of the connection
    mock_connect.return_value.close = mock.Mock()
    
    yield mock_connect, mock_cursor
    
    # Stop all mocks after the test
    mock.patch.stopall()

# happy path - execute - Test that the cart table is dropped if it exists
def test_drop_table_if_exists(mock_db_setup):
    mock_connect, mock_cursor = mock_db_setup
    query = 'DROP TABLE IF EXISTS cart;'
    # Execute the function that drops the table
    shopping_cart.table.drop_table_if_exists()
    # Assert that the execute method was called with the correct query
    mock_cursor.execute.assert_called_once_with(query)


# happy path - execute - Test that the cart table is created successfully
def test_create_cart_table(mock_db_setup):
    mock_connect, mock_cursor = mock_db_setup
    query = 'CREATE TABLE cart (id INTEGER PRIMARY KEY, item_id INTEGER, name TEXT, price REAL, quantity INTEGER, category TEXT, user_type TEXT, payment_status);'
    # Execute the function that creates the table
    shopping_cart.table.create_cart_table()
    # Assert that the execute method was called with the correct query
    mock_cursor.execute.assert_called_once_with(query)


# happy path - commit - Test that the transaction is committed
def test_commit_transaction(mock_db_setup):
    mock_connect, mock_cursor = mock_db_setup
    # Execute the function that commits the transaction
    shopping_cart.table.commit_transaction()
    # Assert that the commit method was called
    mock_connect.return_value.commit.assert_called_once()


# happy path - cursor - Test that the cursor object is created
def test_create_cursor_object(mock_db_setup):
    mock_connect, mock_cursor = mock_db_setup
    # Execute the function that creates a cursor
    shopping_cart.table.create_cursor_object()
    # Assert that the cursor method was called
    mock_connect.return_value.cursor.assert_called_once()


# happy path - close - Test that the connection is closed successfully
def test_close_connection(mock_db_setup):
    mock_connect, mock_cursor = mock_db_setup
    # Execute the function that closes the connection
    shopping_cart.table.close_connection()
    # Assert that the close method was called
    mock_connect.return_value.close.assert_called_once()


# edge case - execute - Test that dropping a non-existent table does not cause an error
def test_drop_non_existent_table(mock_db_setup):
    mock_connect, mock_cursor = mock_db_setup
    query = 'DROP TABLE IF EXISTS non_existent_table;'
    # Execute the function
    shopping_cart.table.drop_non_existent_table()
    # Assert that the execute method was called with the correct query
    mock_cursor.execute.assert_called_once_with(query)


# edge case - execute - Test that creating a table with an existing name raises an error
def test_create_existing_table(mock_db_setup):
    mock_connect, mock_cursor = mock_db_setup
    query = 'CREATE TABLE cart (id INTEGER PRIMARY KEY);'
    # Simulate an error when trying to create an existing table
    mock_cursor.execute.side_effect = sqlite3.OperationalError
    # Execute the function and assert that an error is raised
    with pytest.raises(sqlite3.OperationalError):
        shopping_cart.table.create_existing_table()
    # Assert that the execute method was called with the correct query
    mock_cursor.execute.assert_called_once_with(query)


# edge case - connect - Test that the database connection fails gracefully if the file path is invalid
def test_invalid_file_path():
    # Mock the connect method to raise an error for invalid path
    with mock.patch('sqlite3.connect', side_effect=sqlite3.OperationalError):
        with pytest.raises(sqlite3.OperationalError):
            shopping_cart.table.connect_invalid_path()


# edge case - commit - Test that committing without any changes does not raise an error
def test_commit_without_changes(mock_db_setup):
    mock_connect, mock_cursor = mock_db_setup
    # Execute the function that commits without changes
    shopping_cart.table.commit_without_changes()
    # Assert that the commit method was called
    mock_connect.return_value.commit.assert_called_once()


# edge case - close - Test that closing an already closed connection does not raise an error
def test_close_already_closed_connection(mock_db_setup):
    mock_connect, mock_cursor = mock_db_setup
    # Close the connection once
    shopping_cart.table.close_connection()
    # Attempt to close it again
    shopping_cart.table.close_connection()
    # Assert that the close method was called twice
    assert mock_connect.return_value.close.call_count == 2


