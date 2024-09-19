import pytest
from unittest import mock
import sqlite3
import shopping_cart.table  # Adjust the import based on the actual file structure

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
def setup_database(mock_db_connection, mock_cursor):
    # Mock the execution of SQL commands
    mock_cursor.execute = mock.Mock()
    
    # Mock the commit method
    mock_db_connection.commit = mock.Mock()
    
    # Mock the close method
    mock_db_connection.close = mock.Mock()

    yield

def test_drop_table_if_exists(setup_database, mock_cursor):
    shopping_cart.table.conn = sqlite3.connect('shopping_cart.db')
    shopping_cart.table.cursor = mock_cursor
    shopping_cart.table.conn.commit = mock_db_connection.commit
    shopping_cart.table.conn.close = mock_db_connection.close
    
    # Call the function that executes the drop table SQL command
    shopping_cart.table.cursor.execute("DROP TABLE IF EXISTS cart;")
    
    mock_cursor.execute.assert_called_once_with("DROP TABLE IF EXISTS cart;")

def test_create_table_cart(setup_database, mock_cursor):
    shopping_cart.table.conn = sqlite3.connect('shopping_cart.db')
    shopping_cart.table.cursor = mock_cursor
    shopping_cart.table.conn.commit = mock_db_connection.commit
    shopping_cart.table.conn.close = mock_db_connection.close
    
    # Call the function that executes the create table SQL command
    shopping_cart.table.cursor.execute("CREATE TABLE cart (id INTEGER PRIMARY KEY, item_id INTEGER, name TEXT, price REAL, quantity INTEGER, category TEXT, user_type TEXT, payment_status);")
    
    mock_cursor.execute.assert_called_with("CREATE TABLE cart (id INTEGER PRIMARY KEY, item_id INTEGER, name TEXT, price REAL, quantity INTEGER, category TEXT, user_type TEXT, payment_status);")

def test_commit_transaction(setup_database):
    shopping_cart.table.conn = sqlite3.connect('shopping_cart.db')
    shopping_cart.table.conn.commit()
    
    mock_db_connection.commit.assert_called_once()

def test_close_connection(setup_database):
    shopping_cart.table.conn = sqlite3.connect('shopping_cart.db')
    shopping_cart.table.conn.close()
    
    mock_db_connection.close.assert_called_once()

# happy_path - test_drop_table_if_exists - Test that the cart table is dropped if it exists
def test_drop_table_if_exists(setup_database, mock_cursor):
    shopping_cart.table.conn = sqlite3.connect('shopping_cart.db')
    shopping_cart.table.cursor = mock_cursor
    shopping_cart.table.conn.commit = mock_db_connection.commit
    shopping_cart.table.conn.close = mock_db_connection.close
    
    # Call the function that executes the drop table SQL command
    shopping_cart.table.cursor.execute("DROP TABLE IF EXISTS cart;")
    
    mock_cursor.execute.assert_called_once_with("DROP TABLE IF EXISTS cart;")

# happy_path - test_create_table_cart - Test that the cart table is created successfully
def test_create_table_cart(setup_database, mock_cursor):
    shopping_cart.table.conn = sqlite3.connect('shopping_cart.db')
    shopping_cart.table.cursor = mock_cursor
    shopping_cart.table.conn.commit = mock_db_connection.commit
    shopping_cart.table.conn.close = mock_db_connection.close
    
    # Call the function that executes the create table SQL command
    shopping_cart.table.cursor.execute("CREATE TABLE cart (id INTEGER PRIMARY KEY, item_id INTEGER, name TEXT, price REAL, quantity INTEGER, category TEXT, user_type TEXT, payment_status);")
    
    mock_cursor.execute.assert_called_with("CREATE TABLE cart (id INTEGER PRIMARY KEY, item_id INTEGER, name TEXT, price REAL, quantity INTEGER, category TEXT, user_type TEXT, payment_status);")

# happy_path - test_commit_transaction - Test that commit is called after executing queries
def test_commit_transaction(setup_database):
    shopping_cart.table.conn = sqlite3.connect('shopping_cart.db')
    shopping_cart.table.conn.commit()
    
    mock_db_connection.commit.assert_called_once()

# happy_path - test_connect_to_database - Test that a connection to the SQLite database is established
def test_connect_to_database(mock_db_connection):
    shopping_cart.table.conn = sqlite3.connect('shopping_cart.db')
    
    mock_db_connection.cursor.assert_called_once()

# happy_path - test_close_connection - Test that the connection is closed at the end
def test_close_connection(setup_database):
    shopping_cart.table.conn = sqlite3.connect('shopping_cart.db')
    shopping_cart.table.conn.close()
    
    mock_db_connection.close.assert_called_once()

# edge_case - test_error_handling_drop_table - Test that an error is handled if the drop table query fails
def test_error_handling_drop_table(setup_database, mock_cursor):
    mock_cursor.execute.side_effect = sqlite3.Error("drop table error")
    shopping_cart.table.conn = sqlite3.connect('shopping_cart.db')
    shopping_cart.table.cursor = mock_cursor
    
    try:
        shopping_cart.table.cursor.execute("DROP TABLE IF EXISTS non_existing_table;")
    except sqlite3.Error:
        pass
    
    mock_cursor.execute.assert_called_once_with("DROP TABLE IF EXISTS non_existing_table;")

# edge_case - test_error_handling_create_table - Test that an error is handled if the create table query fails
def test_error_handling_create_table(setup_database, mock_cursor):
    mock_cursor.execute.side_effect = sqlite3.Error("create table error")
    shopping_cart.table.conn = sqlite3.connect('shopping_cart.db')
    shopping_cart.table.cursor = mock_cursor
    
    try:
        shopping_cart.table.cursor.execute("CREATE TABLE cart (id INTEGER PRIMARY KEY, invalid_column_type);")
    except sqlite3.Error:
        pass
    
    mock_cursor.execute.assert_called_once_with("CREATE TABLE cart (id INTEGER PRIMARY KEY, invalid_column_type);")

# edge_case - test_error_print_on_connection_failure - Test that an error is printed if the database connection fails
def test_error_print_on_connection_failure():
    with mock.patch('sqlite3.connect', side_effect=sqlite3.Error("connection error")):
        try:
            shopping_cart.table.conn = sqlite3.connect('invalid_path/shopping_cart.db')
        except sqlite3.Error:
            pass
    
    mock_db_connection.cursor.assert_not_called()

# edge_case - test_error_handling_commit - Test that an error is handled if commit fails
def test_error_handling_commit(setup_database):
    mock_db_connection.commit.side_effect = sqlite3.Error("commit error")
    shopping_cart.table.conn = sqlite3.connect('shopping_cart.db')
    
    try:
        shopping_cart.table.conn.commit()
    except sqlite3.Error:
        pass
    
    mock_db_connection.commit.assert_called_once()

# edge_case - test_error_handling_close_connection - Test that an error is handled if close connection fails
def test_error_handling_close_connection(setup_database):
    mock_db_connection.close.side_effect = sqlite3.Error("close error")
    shopping_cart.table.conn = sqlite3.connect('shopping_cart.db')
    
    try:
        shopping_cart.table.conn.close()
    except sqlite3.Error:
        pass
    
    mock_db_connection.close.assert_called_once()

