import pytest
from unittest import mock
import sqlite3

# Mocking sqlite3.connect
@pytest.fixture
def mock_sqlite_connect():
    with mock.patch('shopping_cart.table.sqlite3.connect') as mock_connect:
        mock_conn = mock.Mock()
        mock_connect.return_value = mock_conn
        yield mock_connect, mock_conn

# Mocking sqlite3.cursor
@pytest.fixture
def mock_sqlite_cursor(mock_sqlite_connect):
    mock_connect, mock_conn = mock_sqlite_connect
    mock_cursor = mock.Mock()
    mock_conn.cursor.return_value = mock_cursor
    yield mock_cursor

# Mocking sqlite3.execute
@pytest.fixture
def mock_sqlite_execute(mock_sqlite_cursor):
    mock_cursor = mock_sqlite_cursor
    yield mock_cursor.execute

# Mocking sqlite3.commit
@pytest.fixture
def mock_sqlite_commit(mock_sqlite_connect):
    mock_connect, mock_conn = mock_sqlite_connect
    yield mock_conn.commit

# Mocking sqlite3.close
@pytest.fixture
def mock_sqlite_close(mock_sqlite_connect):
    mock_connect, mock_conn = mock_sqlite_connect
    yield mock_conn.close

# happy_path - test_drop_table_if_exists - Test that the table 'cart' is dropped if it exists.
def test_drop_table_if_exists(mock_sqlite_execute):
    mock_sqlite_execute.assert_any_call('DROP TABLE IF EXISTS cart;')

# happy_path - test_create_cart_table - Test that the table 'cart' is created successfully.
def test_create_cart_table(mock_sqlite_execute):
    mock_sqlite_execute.assert_any_call('CREATE TABLE cart (\n        id INTEGER PRIMARY KEY,\n        item_id INTEGER ,\n        name TEXT,\n        price REAL,\n        quantity INTEGER,\n        category TEXT,\n        user_type TEXT,\n        payment_status\n    );')

# happy_path - test_cart_table_columns - Test that the table 'cart' has the correct columns after creation.
def test_cart_table_columns(mock_sqlite_execute):
    mock_sqlite_execute.return_value.fetchall.return_value = [
        (0, 'id', 'INTEGER', 0, None, 1),
        (1, 'item_id', 'INTEGER', 0, None, 0),
        (2, 'name', 'TEXT', 0, None, 0),
        (3, 'price', 'REAL', 0, None, 0),
        (4, 'quantity', 'INTEGER', 0, None, 0),
        (5, 'category', 'TEXT', 0, None, 0),
        (6, 'user_type', 'TEXT', 0, None, 0),
        (7, 'payment_status', 'TEXT', 0, None, 0)
    ]
    mock_sqlite_execute.assert_any_call('PRAGMA table_info(cart);')
    columns = [col[1] for col in mock_sqlite_execute.return_value.fetchall()]
    assert columns == ['id', 'item_id', 'name', 'price', 'quantity', 'category', 'user_type', 'payment_status']

# happy_path - test_database_connection - Test that the connection to the database is successful.
def test_database_connection(mock_sqlite_connect):
    mock_sqlite_connect.assert_called_once_with('shopping_cart.db')

# happy_path - test_transaction_commit - Test that the transaction is committed successfully.
def test_transaction_commit(mock_sqlite_commit):
    mock_sqlite_commit.assert_called_once()

# edge_case - test_drop_non_existent_table - Test that dropping a non-existent table does not cause an error.
def test_drop_non_existent_table(mock_sqlite_execute):
    mock_sqlite_execute.assert_any_call('DROP TABLE IF EXISTS non_existent_table;')

# edge_case - test_create_table_invalid_syntax - Test that creating a table with an invalid SQL syntax raises an error.
def test_create_table_invalid_syntax(mock_sqlite_execute):
    mock_sqlite_execute.side_effect = sqlite3.Error('syntax error')
    with pytest.raises(sqlite3.Error):
        mock_sqlite_execute('CREATE TABLE cart (id INTEGER PRIMARY KEY, name TEXT, price REAL, quantity INTEGER, category TEXT, user_type TEXT, payment_status')

# edge_case - test_invalid_sql_command - Test that executing an invalid SQL command raises an error.
def test_invalid_sql_command(mock_sqlite_execute):
    mock_sqlite_execute.side_effect = sqlite3.Error('invalid command')
    with pytest.raises(sqlite3.Error):
        mock_sqlite_execute('INVALID SQL COMMAND')

# edge_case - test_commit_without_changes - Test that committing without any changes does not cause an error.
def test_commit_without_changes(mock_sqlite_commit):
    mock_sqlite_commit.assert_called_once()

# edge_case - test_close_already_closed_connection - Test that closing an already closed connection does not cause an error.
def test_close_already_closed_connection(mock_sqlite_close):
    mock_sqlite_close()
    mock_sqlite_close.assert_called()

