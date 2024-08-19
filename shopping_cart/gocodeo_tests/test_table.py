import pytest
from unittest import mock
import sqlite3

@pytest.fixture
def mock_sqlite_connect():
    with mock.patch('sqlite3.connect') as mock_connect:
        mock_conn = mock.Mock()
        mock_connect.return_value = mock_conn

        mock_cursor = mock.Mock()
        mock_conn.cursor.return_value = mock_cursor

        yield mock_conn, mock_cursor

        mock_conn.close.assert_called_once()

@pytest.fixture
def mock_sqlite_error():
    with mock.patch('sqlite3.connect', side_effect=sqlite3.Error):
        yield

@pytest.fixture
def mock_sqlite_cursor_error():
    with mock.patch('sqlite3.connect') as mock_connect:
        mock_conn = mock.Mock()
        mock_connect.return_value = mock_conn

        mock_conn.cursor.side_effect = sqlite3.Error

        yield mock_conn

@pytest.fixture
def mock_sqlite_execute_error():
    with mock.patch('sqlite3.connect') as mock_connect:
        mock_conn = mock.Mock()
        mock_connect.return_value = mock_conn

        mock_cursor = mock.Mock()
        mock_cursor.execute.side_effect = sqlite3.Error
        mock_conn.cursor.return_value = mock_cursor

        yield mock_conn, mock_cursor# happy_path - connect - Test successful connection to the SQLite database
def test_connect_to_database(mock_sqlite_connect):
    conn, cursor = mock_sqlite_connect
    assert conn is not None
    assert cursor is not None

# happy_path - cursor - Test successful creation of the cursor object
def test_create_cursor(mock_sqlite_connect):
    conn, cursor = mock_sqlite_connect
    assert cursor is not None

# happy_path - execute - Test successful execution of SQL commands
def test_execute_sql_command(mock_sqlite_connect):
    conn, cursor = mock_sqlite_connect
    cursor.execute('DROP TABLE IF EXISTS cart;')
    cursor.execute.assert_called_once_with('DROP TABLE IF EXISTS cart;')

# happy_path - commit - Test successful commit of the transaction
def test_commit_transaction(mock_sqlite_connect):
    conn, cursor = mock_sqlite_connect
    conn.commit()
    conn.commit.assert_called_once()

# happy_path - close - Test successful closing of the database connection
def test_close_connection(mock_sqlite_connect):
    conn, cursor = mock_sqlite_connect
    conn.close()

# edge_case - connect - Test connection failure due to invalid database path
def test_connect_invalid_database(mock_sqlite_error):
    with pytest.raises(sqlite3.Error):
        sqlite3.connect('invalid_path.db')

# edge_case - execute - Test executing invalid SQL command
def test_execute_invalid_sql_command(mock_sqlite_cursor_error):
    conn, cursor = mock_sqlite_cursor_error
    with pytest.raises(sqlite3.Error):
        cursor.execute('INVALID SQL COMMAND;')

# edge_case - commit - Test committing without any changes
def test_commit_without_changes(mock_sqlite_connect):
    conn, cursor = mock_sqlite_connect
    conn.commit()  # No changes made

# edge_case - close - Test closing an already closed connection
def test_close_already_closed_connection(mock_sqlite_connect):
    conn, cursor = mock_sqlite_connect
    conn.close()
    with pytest.raises(sqlite3.Error):
        conn.close()

# edge_case - execute - Test dropping a non-existent table
def test_drop_non_existent_table(mock_sqlite_connect):
    conn, cursor = mock_sqlite_connect
    cursor.execute('DROP TABLE IF EXISTS non_existent_table;')
    cursor.execute.assert_called_once_with('DROP TABLE IF EXISTS non_existent_table;')

