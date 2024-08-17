import pytest
import sqlite3
from unittest import mock

@pytest.fixture
def mock_sqlite(monkeypatch):
    mock_conn = mock.MagicMock()
    mock_cursor = mock.MagicMock()

    mock_conn.cursor.return_value = mock_cursor
    mock_conn.commit.return_value = None
    mock_conn.close.return_value = None

    monkeypatch.setattr(sqlite3, 'connect', mock.MagicMock(return_value=mock_conn))

    return mock_conn, mock_cursor# happy_path - create_cart_table - Successfully recreate the cart table in the database
def test_create_cart_table(mock_sqlite):
    mock_conn, mock_cursor = mock_sqlite
    
    # Call the function that creates the cart table
    create_cart_table()
    
    # Assert that the drop table command was executed
    mock_cursor.execute.assert_any_call('''
    DROP TABLE IF EXISTS cart;
    ''')
    
    # Assert that the create table command was executed
    mock_cursor.execute.assert_any_call('''
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
    
    # Assert that commit was called
    mock_conn.commit.assert_called_once()

# edge_case - create_cart_table_error - Handle error when dropping or creating the cart table
def test_create_cart_table_error(mock_sqlite):
    mock_conn, mock_cursor = mock_sqlite
    
    # Simulate an error when executing SQL commands
    mock_cursor.execute.side_effect = sqlite3.Error('SQL error')
    
    # Call the function that creates the cart table
    with pytest.raises(sqlite3.Error):
        create_cart_table()
    
    # Ensure that the error was raised and the connection was closed
    mock_conn.close.assert_called_once()

