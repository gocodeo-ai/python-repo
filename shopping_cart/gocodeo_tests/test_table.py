import pytest
from unittest import mock
import sqlite3

@pytest.fixture
def mock_sqlite():
    with mock.patch('sqlite3.connect') as mock_connect:
        mock_conn = mock.Mock()
        mock_cursor = mock.Mock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        yield mock_connect, mock_conn, mock_cursor

@pytest.fixture
def setup_environment(mock_sqlite):
    mock_connect, mock_conn, mock_cursor = mock_sqlite
    yield mock_connect, mock_conn, mock_cursor
    mock_conn.close.assert_called_once()

# happy_path - create_cart_table - Successfully create the cart table in the database
def test_create_cart_table(setup_environment):
    mock_connect, mock_conn, mock_cursor = setup_environment
    
    # Simulate the execution of the create table query
    mock_cursor.execute.assert_called_with('''
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
    ''')
    
    # Check if commit was called
    mock_conn.commit.assert_called_once()

# edge_case - drop_table_if_exists - Handle error when dropping a non-existing table
def test_drop_table_error(setup_environment):
    mock_connect, mock_conn, mock_cursor = setup_environment
    
    # Simulate an error when dropping the table
    mock_cursor.execute.side_effect = sqlite3.Error('Table does not exist')
    
    with pytest.raises(sqlite3.Error):
        mock_cursor.execute('''
        DROP TABLE IF EXISTS cart;
        ''')
        
    # Ensure that the error was raised and the commit was not called
    mock_conn.commit.assert_not_called()

