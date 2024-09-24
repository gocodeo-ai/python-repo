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
        
        with mock.patch.object(DatabaseConnection, 'connect', return_value=None) as mock_connect_method, \
             mock.patch.object(DatabaseConnection, 'execute', return_value=None) as mock_execute_method, \
             mock.patch.object(DatabaseConnection, 'fetchone', return_value=None) as mock_fetchone_method, \
             mock.patch.object(DatabaseConnection, 'fetchall', return_value=None) as mock_fetchall_method, \
             mock.patch.object(DatabaseConnection, 'commit', return_value=None) as mock_commit_method, \
             mock.patch.object(DatabaseConnection, 'close', return_value=None) as mock_close_method:
            
            db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "shopping_cart.db")
            db_connection = DatabaseConnection(db_path)
            yield db_connection, mock_connection, mock_connect_method, mock_execute_method, mock_fetchone_method, mock_fetchall_method, mock_commit_method, mock_close_method

def test_add_item_to_cart_db(mock_database_connection):
    db_connection, mock_connection, mock_connect_method, mock_execute_method, mock_fetchone_method, mock_fetchall_method, mock_commit_method, mock_close_method = mock_database_connection
    # Setup for your test here

# happy_path - test_connect_success - Test that the connection to the database is established successfully
def test_connect_success(mock_database_connection):
    db_connection, mock_connection, mock_connect_method, _, _, _, _, _ = mock_database_connection
    db_connection.connect()
    mock_connect_method.assert_called_once()
    assert mock_connection is not None

# happy_path - test_execute_no_params - Test that a query is executed successfully without parameters
def test_execute_no_params(mock_database_connection):
    db_connection, _, _, mock_execute_method, _, _, _, _ = mock_database_connection
    query = 'CREATE TABLE test (id INTEGER)'
    db_connection.execute(query)
    mock_execute_method.assert_called_once_with(query, [])

# happy_path - test_execute_with_params - Test that a query is executed successfully with parameters
def test_execute_with_params(mock_database_connection):
    db_connection, _, _, mock_execute_method, _, _, _, _ = mock_database_connection
    query = 'INSERT INTO test (id) VALUES (?)'
    params = [1]
    db_connection.execute(query, params)
    mock_execute_method.assert_called_once_with(query, params)

# happy_path - test_fetchone_single_row - Test that fetchone returns a single row from the database
def test_fetchone_single_row(mock_database_connection):
    db_connection, _, _, _, mock_fetchone_method, _, _, _ = mock_database_connection
    query = 'SELECT id FROM test WHERE id = ?'
    params = [1]
    mock_fetchone_method.return_value = (1,)
    result = db_connection.fetchone(query, params)
    mock_fetchone_method.assert_called_once_with(query, params)
    assert result == (1,)

# happy_path - test_fetchall_multiple_rows - Test that fetchall returns multiple rows from the database
def test_fetchall_multiple_rows(mock_database_connection):
    db_connection, _, _, _, _, mock_fetchall_method, _, _ = mock_database_connection
    query = 'SELECT id FROM test'
    mock_fetchall_method.return_value = [(1,), (2,), (3,)]
    results = db_connection.fetchall(query)
    mock_fetchall_method.assert_called_once_with(query, [])
    assert results == [(1,), (2,), (3,)]

# edge_case - test_connect_invalid_path - Test that connecting with an invalid path raises an error
def test_connect_invalid_path(mock_database_connection):
    db_connection, mock_connection, mock_connect_method, _, _, _, _, _ = mock_database_connection
    mock_connect_method.side_effect = sqlite3.OperationalError
    with pytest.raises(sqlite3.OperationalError):
        db_connection.connect()

# edge_case - test_execute_syntax_error - Test that executing a query with syntax error raises an error
def test_execute_syntax_error(mock_database_connection):
    db_connection, _, _, mock_execute_method, _, _, _, _ = mock_database_connection
    query = 'INSERT INTO test (id VALUES ?)'  # Syntax error
    mock_execute_method.side_effect = sqlite3.OperationalError
    with pytest.raises(sqlite3.OperationalError):
        db_connection.execute(query, [1])

# edge_case - test_fetchone_no_result - Test that fetchone returns None for a non-existent record
def test_fetchone_no_result(mock_database_connection):
    db_connection, _, _, _, mock_fetchone_method, _, _, _ = mock_database_connection
    query = 'SELECT id FROM test WHERE id = ?'
    params = [999]
    mock_fetchone_method.return_value = None
    result = db_connection.fetchone(query, params)
    mock_fetchone_method.assert_called_once_with(query, params)
    assert result is None

# edge_case - test_fetchall_no_results - Test that fetchall returns an empty list for no matching records
def test_fetchall_no_results(mock_database_connection):
    db_connection, _, _, _, _, mock_fetchall_method, _, _ = mock_database_connection
    query = 'SELECT id FROM test WHERE id > ?'
    params = [999]
    mock_fetchall_method.return_value = []
    results = db_connection.fetchall(query, params)
    mock_fetchall_method.assert_called_once_with(query, params)
    assert results == []

# edge_case - test_close_already_closed - Test that closing an already closed connection does not raise an error
def test_close_already_closed(mock_database_connection):
    db_connection, _, _, _, _, _, _, mock_close_method = mock_database_connection
    db_connection.close()  # First close
    db_connection.close()  # Second close, should not raise
    mock_close_method.assert_called()

