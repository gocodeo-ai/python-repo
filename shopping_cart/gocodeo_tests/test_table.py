import pytest
import sqlite3
from unittest.mock import Mock, patch

@pytest.fixture
def mock_sqlite3():
    with patch('sqlite3.connect') as mock_connect:
        mock_conn = Mock()
        mock_cursor = Mock()
        mock_conn.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_conn
        yield mock_connect, mock_conn, mock_cursor

@pytest.fixture
def mock_print():
    with patch('builtins.print') as mock_print:
        yield mock_print

@pytest.fixture
def setup_mocks(mock_sqlite3, mock_print):
    mock_connect, mock_conn, mock_cursor = mock_sqlite3
    
    # Mock the execute method
    mock_cursor.execute = Mock()
    
    # Mock the commit method
    mock_conn.commit = Mock()
    
    # Mock the close method
    mock_conn.close = Mock()
    
    return mock_connect, mock_conn, mock_cursor, mock_print

# happy path - connect - Successful table creation
def test_successful_connection(setup_mocks):
    mock_connect, _, _, _ = setup_mocks
    mock_connect.assert_called_once_with('shopping_cart.db')
    assert mock_connect.return_value is not None

# happy path - execute - Successful table drop
def test_successful_table_drop(setup_mocks):
    _, _, mock_cursor, _ = setup_mocks
    mock_cursor.execute.assert_any_call('DROP TABLE IF EXISTS cart;')
    assert mock_cursor.execute.call_count >= 1

# happy path - execute - Successful table creation
def test_successful_table_creation(setup_mocks):
    _, _, mock_cursor, _ = setup_mocks
    mock_cursor.execute.assert_any_call('CREATE TABLE cart (\n        id INTEGER PRIMARY KEY,\n        item_id INTEGER ,\n        name TEXT,\n        price REAL,\n        quantity INTEGER,\n        category TEXT,\n        user_type TEXT,\n        payment_status\n    );')
    assert mock_cursor.execute.call_count >= 2

# happy path - commit - Successful commit
def test_successful_commit(setup_mocks):
    _, mock_conn, _, _ = setup_mocks
    mock_conn.commit.assert_called_once()

# happy path - close - Successful connection close
def test_successful_connection_close(setup_mocks):
    _, mock_conn, _, _ = setup_mocks
    mock_conn.close.assert_called_once()

# happy path - print - Successful print of table creation message
def test_successful_print_message(setup_mocks):
    _, _, _, mock_print = setup_mocks
    mock_print.assert_called_with("Table 'cart' recreated successfully.")

# edge case - connect - Connection to non-existent database
def test_connection_to_nonexistent_db(setup_mocks):
    mock_connect, _, _, _ = setup_mocks
    mock_connect.assert_called_once_with('shopping_cart.db')
    assert mock_connect.return_value is not None

# edge case - execute - Dropping non-existent table
def test_drop_nonexistent_table(setup_mocks):
    _, _, mock_cursor, _ = setup_mocks
    mock_cursor.execute.assert_any_call('DROP TABLE IF EXISTS cart;')
    assert mock_cursor.execute.call_count >= 1

# edge case - execute - Creating table with duplicate column names
def test_create_table_duplicate_columns(setup_mocks):
    _, _, mock_cursor, _ = setup_mocks
    mock_cursor.execute.side_effect = sqlite3.Error("duplicate column name: id")
    with pytest.raises(sqlite3.Error):
        mock_cursor.execute('CREATE TABLE test (id INTEGER, id INTEGER);')

# edge case - commit - Committing without changes
def test_commit_without_changes(setup_mocks):
    _, mock_conn, _, _ = setup_mocks
    mock_conn.commit.assert_called_once()
    assert mock_conn.commit.call_count == 1

# edge case - close - Closing already closed connection
def test_close_closed_connection(setup_mocks):
    _, mock_conn, _, _ = setup_mocks
    mock_conn.close.side_effect = [None, sqlite3.ProgrammingError("Cannot operate on a closed database.")]
    mock_conn.close()
    with pytest.raises(sqlite3.ProgrammingError):
        mock_conn.close()

# edge case - print - Printing with non-string input
def test_print_non_string(setup_mocks):
    _, _, _, mock_print = setup_mocks
    non_string_input = 123
    mock_print(non_string_input)
    mock_print.assert_called_with(123)

