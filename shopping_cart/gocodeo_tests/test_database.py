import pytest
from unittest import mock
import sqlite3
import os
from shopping_cart.database import DatabaseConnection, add_item_to_cart_db

@pytest.fixture
def mock_database_connection():
    with mock.patch('shopping_cart.database.sqlite3.connect') as mock_connect:
        mock_connection = mock.Mock()
        mock_connect.return_value = mock_connection
        db_connection = DatabaseConnection('mock_db_path')
        db_connection.connect()
        yield db_connection, mock_connection

@pytest.fixture
def mock_cursor(mock_database_connection):
    db_connection, mock_connection = mock_database_connection
    mock_cursor = mock.Mock()
    mock_connection.cursor.return_value = mock_cursor
    yield mock_cursor

@pytest.fixture
def mock_execute(mock_cursor):
    mock_cursor.execute = mock.Mock()

@pytest.fixture
def mock_commit(mock_database_connection):
    db_connection, mock_connection = mock_database_connection
    mock_connection.commit = mock.Mock()

@pytest.fixture
def mock_close(mock_database_connection):
    db_connection, mock_connection = mock_database_connection
    mock_connection.close = mock.Mock()

@pytest.fixture
def mock_fetchone(mock_cursor):
    mock_cursor.fetchone = mock.Mock()

@pytest.fixture
def mock_fetchall(mock_cursor):
    mock_cursor.fetchall = mock.Mock()

@pytest.fixture
def mock_add_item_to_cart_db(mock_database_connection):
    with mock.patch('shopping_cart.database.database_connection') as mock_db_conn:
        mock_db_conn.connect = mock.Mock()
        mock_db_conn.execute = mock.Mock()
        mock_db_conn.commit = mock.Mock()
        mock_db_conn.close = mock.Mock()
        yield mock_db_conn

# happy path - connect - Test that connection to the database is established successfully
def test_connect_success(mock_database_connection):
    db_connection, mock_connection = mock_database_connection
    assert db_connection.connection is not None
    mock_connection.cursor.assert_not_called()


# happy path - execute - Test that query executes successfully without parameters
def test_execute_query_no_params(mock_execute, mock_commit, mock_close, mock_database_connection):
    db_connection, _ = mock_database_connection
    query = 'CREATE TABLE IF NOT EXISTS cart (id INTEGER PRIMARY KEY)'
    db_connection.execute(query)
    mock_execute.assert_called_once_with(query, [])
    mock_commit.assert_called_once()
    mock_close.assert_called_once()


# happy path - fetchone - Test that fetchone retrieves a single record
def test_fetchone_single_record(mock_fetchone, mock_database_connection):
    db_connection, _ = mock_database_connection
    mock_fetchone.return_value = {'id': 1}
    result = db_connection.fetchone('SELECT * FROM cart WHERE id = ?', [1])
    assert result == {'id': 1}
    mock_fetchone.assert_called_once_with('SELECT * FROM cart WHERE id = ?', [1])


# happy path - fetchall - Test that fetchall retrieves all records
def test_fetchall_all_records(mock_fetchall, mock_database_connection):
    db_connection, _ = mock_database_connection
    mock_fetchall.return_value = [{'id': 1}, {'id': 2}]
    results = db_connection.fetchall('SELECT * FROM cart')
    assert results == [{'id': 1}, {'id': 2}]
    mock_fetchall.assert_called_once_with('SELECT * FROM cart', [])


# happy path - commit - Test that commit saves the transaction
def test_commit_transaction(mock_commit, mock_database_connection):
    db_connection, _ = mock_database_connection
    db_connection.commit()
    mock_commit.assert_called_once()


# happy path - close - Test that close terminates the connection
def test_close_connection(mock_close, mock_database_connection):
    db_connection, _ = mock_database_connection
    db_connection.close()
    mock_close.assert_called_once()


# edge case - connect - Test that connection fails with invalid path
def test_connect_invalid_path():
    with mock.patch('shopping_cart.database.sqlite3.connect', side_effect=sqlite3.OperationalError('unable to open database file')):
        db_connection = DatabaseConnection('invalid_path.db')
        with pytest.raises(sqlite3.OperationalError, match='unable to open database file'):
            db_connection.connect()


# edge case - execute - Test that execute raises error with invalid SQL
def test_execute_invalid_sql(mock_execute, mock_database_connection):
    db_connection, mock_connection = mock_database_connection
    mock_execute.side_effect = sqlite3.OperationalError('syntax error')
    with pytest.raises(sqlite3.OperationalError, match='syntax error'):
        db_connection.execute('INVALID SQL')


# edge case - fetchone - Test that fetchone returns None for non-existing record
def test_fetchone_no_record(mock_fetchone, mock_database_connection):
    db_connection, _ = mock_database_connection
    mock_fetchone.return_value = None
    result = db_connection.fetchone('SELECT * FROM cart WHERE id = ?', [999])
    assert result is None
    mock_fetchone.assert_called_once_with('SELECT * FROM cart WHERE id = ?', [999])


# edge case - fetchall - Test that fetchall returns empty list for empty table
def test_fetchall_empty_table(mock_fetchall, mock_database_connection):
    db_connection, _ = mock_database_connection
    mock_fetchall.return_value = []
    results = db_connection.fetchall('SELECT * FROM empty_table')
    assert results == []
    mock_fetchall.assert_called_once_with('SELECT * FROM empty_table', [])


# edge case - commit - Test that commit does nothing when no changes
def test_commit_no_changes(mock_commit, mock_database_connection):
    db_connection, _ = mock_database_connection
    db_connection.commit()
    mock_commit.assert_called_once()


# edge case - close - Test that close does not fail when already closed
def test_close_already_closed(mock_close, mock_database_connection):
    db_connection, _ = mock_database_connection
    db_connection.close()
    db_connection.close()
    mock_close.assert_called_once()


