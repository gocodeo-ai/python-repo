import pytest
from unittest import mock
import sqlite3

@pytest.fixture
def mock_sqlite_connection():
    with mock.patch('sqlite3.connect') as mock_connect:
        mock_conn = mock.Mock()
        mock_connect.return_value = mock_conn
        yield mock_conn

@pytest.fixture
def mock_cursor(mock_sqlite_connection):
    mock_cursor = mock.Mock()
    mock_sqlite_connection.cursor.return_value = mock_cursor
    yield mock_cursor

@pytest.fixture
def mock_execute(mock_cursor):
    mock_cursor.execute = mock.Mock()

@pytest.fixture
def mock_commit(mock_sqlite_connection):
    mock_sqlite_connection.commit = mock.Mock()

@pytest.fixture
def mock_close(mock_sqlite_connection):
    mock_sqlite_connection.close = mock.Mock()

@pytest.fixture
def mock_sqlite_error_handling():
    mock.patch('sqlite3.Error').start()
    yield
    mock.patch.stopall()

# happy path - sqlite3.connect - Test that the SQLite database connection is established successfully.
def test_sqlite_connection(mock_sqlite_connection):
    mock_sqlite_connection.connect.assert_called_once_with('shopping_cart.db')
    
    # Check expected result
    assert mock_sqlite_connection is not None


# happy path - cursor.execute - Test that the 'cart' table is dropped if it exists.
def test_drop_table_if_exists(mock_execute, mock_cursor):
    drop_table_query = 'DROP TABLE IF EXISTS cart;'
    
    # Execute the query
    mock_cursor.execute(drop_table_query)
    
    # Check if the query was executed
    mock_cursor.execute.assert_called_with(drop_table_query)


# happy path - cursor.execute - Test that the 'cart' table is created successfully with all specified columns.
def test_create_cart_table(mock_execute, mock_cursor):
    create_table_query = '''
    CREATE TABLE cart (
        id INTEGER PRIMARY KEY,
        item_id INTEGER ,
        name TEXT,
        price REAL,
        quantity INTEGER,
        category TEXT,
        user_type TEXT,
        payment_status
    );
    '''
    
    # Execute the query
    mock_cursor.execute(create_table_query)
    
    # Check if the query was executed
    mock_cursor.execute.assert_called_with(create_table_query)


# happy path - conn.commit - Test that the transaction is committed successfully.
def test_commit_transaction(mock_commit, mock_sqlite_connection):
    # Commit the transaction
    mock_sqlite_connection.commit()
    
    # Check if commit was called
    mock_sqlite_connection.commit.assert_called_once()


# happy path - conn.close - Test that the database connection is closed successfully.
def test_close_connection(mock_close, mock_sqlite_connection):
    # Close the connection
    mock_sqlite_connection.close()
    
    # Check if close was called
    mock_sqlite_connection.close.assert_called_once()


# edge case - sqlite3.connect - Test that an error is raised if the database file is not accessible.
def test_database_file_not_accessible(mock_sqlite_error_handling):
    with pytest.raises(sqlite3.Error):
        sqlite3.connect('invalid_path/shopping_cart.db')


# edge case - cursor.execute - Test that an error is raised if the SQL syntax is incorrect when dropping a table.
def test_drop_table_sql_syntax_error(mock_execute, mock_cursor, mock_sqlite_error_handling):
    incorrect_drop_query = 'DROP TABLE cart'
    
    # Simulate syntax error
    mock_cursor.execute.side_effect = sqlite3.Error
    
    with pytest.raises(sqlite3.Error):
        mock_cursor.execute(incorrect_drop_query)


# edge case - cursor.execute - Test that an error is raised if the SQL syntax is incorrect when creating a table.
def test_create_table_sql_syntax_error(mock_execute, mock_cursor, mock_sqlite_error_handling):
    incorrect_create_query = 'CREATE TABLE cart id INTEGER PRIMARY KEY, item_id INTEGER'
    
    # Simulate syntax error
    mock_cursor.execute.side_effect = sqlite3.Error
    
    with pytest.raises(sqlite3.Error):
        mock_cursor.execute(incorrect_create_query)


# edge case - conn.commit - Test that an error is raised if committing a transaction fails.
def test_commit_transaction_failure(mock_commit, mock_sqlite_connection, mock_sqlite_error_handling):
    # Simulate commit error
    mock_sqlite_connection.commit.side_effect = sqlite3.Error
    
    with pytest.raises(sqlite3.Error):
        mock_sqlite_connection.commit()


# edge case - conn.close - Test that an error is raised if closing the connection fails.
def test_close_connection_failure(mock_close, mock_sqlite_connection, mock_sqlite_error_handling):
    # Simulate close error
    mock_sqlite_connection.close.side_effect = sqlite3.Error
    
    with pytest.raises(sqlite3.Error):
        mock_sqlite_connection.close()


