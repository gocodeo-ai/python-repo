import pytest
from unittest import mock
import sqlite3

@pytest.fixture
def mock_sqlite():
    with mock.patch('sqlite3.connect') as mock_connect, \
         mock.patch('sqlite3.Cursor') as mock_cursor, \
         mock.patch('sqlite3.Connection') as mock_connection:
        
        mock_conn_instance = mock.Mock()
        mock_cursor_instance = mock.Mock()
        
        mock_connect.return_value = mock_conn_instance
        mock_conn_instance.cursor.return_value = mock_cursor_instance
        
        yield mock_connect, mock_connection, mock_cursor_instance, mock_conn_instance# happy_path - connect - generate test cases on successful connection to the SQLite database.
def test_connect_db(mock_sqlite):
    mock_connect, mock_connection, mock_cursor_instance, mock_conn_instance = mock_sqlite
    assert mock_connect.called
    assert mock_conn_instance is not None

# happy_path - cursor - generate test cases on creating a cursor object successfully.
def test_create_cursor(mock_sqlite):
    mock_connect, mock_connection, mock_cursor_instance, mock_conn_instance = mock_sqlite
    cursor = mock_conn_instance.cursor()
    assert cursor is not None
    assert cursor == mock_cursor_instance

# happy_path - execute - generate test cases on executing a valid SQL command.
def test_execute_drop_table(mock_sqlite):
    mock_connect, mock_connection, mock_cursor_instance, mock_conn_instance = mock_sqlite
    mock_cursor_instance.execute('DROP TABLE IF EXISTS cart;')
    mock_cursor_instance.execute.assert_called_once_with('DROP TABLE IF EXISTS cart;')

# happy_path - commit - generate test cases on committing a transaction successfully.
def test_commit_transaction(mock_sqlite):
    mock_connect, mock_connection, mock_cursor_instance, mock_conn_instance = mock_sqlite
    mock_conn_instance.commit()
    mock_conn_instance.commit.assert_called_once()

# happy_path - close - generate test cases on closing the database connection successfully.
def test_close_connection(mock_sqlite):
    mock_connect, mock_connection, mock_cursor_instance, mock_conn_instance = mock_sqlite
    mock_conn_instance.close()
    mock_conn_instance.close.assert_called_once()

# edge_case - connect - generate test cases on attempting to connect to a non-existing database.
def test_connect_non_existing_db():
    with pytest.raises(sqlite3.Error):
        sqlite3.connect('non_existing.db')

# edge_case - execute - generate test cases on executing an invalid SQL command.
def test_execute_invalid_query(mock_sqlite):
    mock_connect, mock_connection, mock_cursor_instance, mock_conn_instance = mock_sqlite
    with pytest.raises(sqlite3.Error):
        mock_cursor_instance.execute('INVALID SQL COMMAND')

# edge_case - commit - generate test cases on committing a transaction without any prior execution.
def test_commit_without_execution(mock_sqlite):
    mock_connect, mock_connection, mock_cursor_instance, mock_conn_instance = mock_sqlite
    # No prior execution
    with pytest.raises(sqlite3.Error):
        mock_conn_instance.commit()

# edge_case - close - generate test cases on closing an already closed connection.
def test_close_already_closed_connection(mock_sqlite):
    mock_connect, mock_connection, mock_cursor_instance, mock_conn_instance = mock_sqlite
    mock_conn_instance.close()
    with pytest.raises(sqlite3.Error):
        mock_conn_instance.close()

# edge_case - execute - generate test cases on dropping a non-existing table.
def test_execute_drop_non_existing_table(mock_sqlite):
    mock_connect, mock_connection, mock_cursor_instance, mock_conn_instance = mock_sqlite
    mock_cursor_instance.execute('DROP TABLE IF EXISTS non_existing_table;')
    mock_cursor_instance.execute.assert_called_once_with('DROP TABLE IF EXISTS non_existing_table;')

