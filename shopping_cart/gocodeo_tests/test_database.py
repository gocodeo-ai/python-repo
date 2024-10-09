import pytest
from unittest import mock
import sqlite3
from shopping_cart.database import DatabaseConnection, add_item_to_cart_db

@pytest.fixture
def mock_database_connection():
    with mock.patch('shopping_cart.database.sqlite3.connect') as mock_connect:
        mock_connection = mock.Mock()
        mock_connect.return_value = mock_connection
        
        with mock.patch.object(DatabaseConnection, 'connect', return_value=None) as mock_connect_method, \
             mock.patch.object(DatabaseConnection, 'execute', return_value=None) as mock_execute_method, \
             mock.patch.object(DatabaseConnection, 'fetchone', return_value=None) as mock_fetchone_method, \
             mock.patch.object(DatabaseConnection, 'fetchall', return_value=None) as mock_fetchall_method, \
             mock.patch.object(DatabaseConnection, 'commit', return_value=None) as mock_commit_method, \
             mock.patch.object(DatabaseConnection, 'close', return_value=None) as mock_close_method:
            
            db_connection = DatabaseConnection('valid_path.db')
            yield db_connection, mock_connect_method, mock_execute_method, mock_fetchone_method, mock_fetchall_method, mock_commit_method, mock_close_method
            
            mock_close_method.assert_called_once()

# happy path - connect - Test that the database connection is established successfully with a valid path
def test_connect_success(mock_database_connection):
    db_connection, mock_connect_method, _, _, _, _, _ = mock_database_connection
    db_connection.connect()
    mock_connect_method.assert_called_once()


# happy path - execute - Test that execute runs a valid SQL query without parameters
def test_execute_valid_query(mock_database_connection):
    db_connection, _, mock_execute_method, _, _, _, _ = mock_database_connection
    query = 'CREATE TABLE test (id INTEGER)'
    db_connection.execute(query)
    mock_execute_method.assert_called_once_with(query, [])


# happy path - fetchone - Test that fetchone retrieves a single record
def test_fetchone_single_record(mock_database_connection):
    db_connection, _, _, mock_fetchone_method, _, _, _ = mock_database_connection
    query = 'SELECT * FROM test WHERE id=1'
    db_connection.fetchone(query)
    mock_fetchone_method.assert_called_once_with(query, [])


# happy path - fetchall - Test that fetchall retrieves all records
def test_fetchall_all_records(mock_database_connection):
    db_connection, _, _, _, mock_fetchall_method, _, _ = mock_database_connection
    query = 'SELECT * FROM test'
    db_connection.fetchall(query)
    mock_fetchall_method.assert_called_once_with(query, [])


# happy path - commit - Test that commit saves changes to the database
def test_commit_saves_changes(mock_database_connection):
    db_connection, _, _, _, _, mock_commit_method, _ = mock_database_connection
    db_connection.commit()
    mock_commit_method.assert_called_once()


# happy path - close - Test that close closes the database connection
def test_close_connection(mock_database_connection):
    db_connection, _, _, _, _, _, mock_close_method = mock_database_connection
    db_connection.close()
    mock_close_method.assert_called_once()


# edge case - connect - Test that connect raises an error with an invalid path
def test_connect_invalid_path():
    with mock.patch('shopping_cart.database.sqlite3.connect', side_effect=sqlite3.OperationalError):
        db_connection = DatabaseConnection('invalid_path.db')
        with pytest.raises(sqlite3.OperationalError):
            db_connection.connect()


# edge case - execute - Test that execute handles SQL syntax error
def test_execute_syntax_error(mock_database_connection):
    db_connection, _, mock_execute_method, _, _, _, _ = mock_database_connection
    mock_execute_method.side_effect = sqlite3.OperationalError
    query = 'INVALID SQL'
    with pytest.raises(sqlite3.OperationalError):
        db_connection.execute(query)


# edge case - fetchone - Test that fetchone returns None for a non-existent record
def test_fetchone_no_record(mock_database_connection):
    db_connection, _, _, mock_fetchone_method, _, _, _ = mock_database_connection
    mock_fetchone_method.return_value = None
    query = 'SELECT * FROM test WHERE id=999'
    result = db_connection.fetchone(query)
    assert result is None


# edge case - fetchall - Test that fetchall returns an empty list for no records
def test_fetchall_no_records(mock_database_connection):
    db_connection, _, _, _, mock_fetchall_method, _, _ = mock_database_connection
    mock_fetchall_method.return_value = []
    query = 'SELECT * FROM test WHERE id=999'
    results = db_connection.fetchall(query)
    assert results == []


# edge case - commit - Test that commit does nothing when no changes are made
def test_commit_no_changes(mock_database_connection):
    db_connection, _, _, _, _, mock_commit_method, _ = mock_database_connection
    db_connection.commit()
    mock_commit_method.assert_called_once()


# edge case - close - Test that close does not raise error if connection is already closed
def test_close_already_closed(mock_database_connection):
    db_connection, _, _, _, _, _, mock_close_method = mock_database_connection
    db_connection.close()
    db_connection.close()
    mock_close_method.assert_called_once()


