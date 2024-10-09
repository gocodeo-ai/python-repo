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
        
        mock_cursor = mock.Mock()
        mock_connection.cursor.return_value = mock_cursor
        
        yield mock_connection, mock_cursor

@pytest.fixture
def db_connection(mock_database_connection):
    mock_connection, mock_cursor = mock_database_connection
    db_path = 'valid_path.db'
    database = DatabaseConnection(db_path)
    database.connection = mock_connection
    return database

def test_connect_successful(db_connection, mock_database_connection):
    db_connection.connect()
    assert db_connection.connection is not None

def test_execute_query_without_params(db_connection, mock_database_connection):
    query = 'CREATE TABLE test (id INTEGER)'
    db_connection.execute(query)
    mock_database_connection[1].execute.assert_called_once_with(query, [])

def test_execute_query_with_params(db_connection, mock_database_connection):
    query = 'INSERT INTO test (id) VALUES (?)'
    params = [1]
    db_connection.execute(query, params)
    mock_database_connection[1].execute.assert_called_once_with(query, params)

def test_fetchone_single_result(db_connection, mock_database_connection):
    query = 'SELECT * FROM test WHERE id = ?'
    params = [1]
    db_connection.fetchone(query, params)
    mock_database_connection[1].execute.assert_called_once_with(query, params)

def test_fetchall_multiple_results(db_connection, mock_database_connection):
    query = 'SELECT * FROM test'
    db_connection.fetchall(query)
    mock_database_connection[1].execute.assert_called_once_with(query, [])

def test_commit(db_connection, mock_database_connection):
    db_connection.commit()
    mock_database_connection[0].commit.assert_called_once()

def test_close(db_connection, mock_database_connection):
    db_connection.close()
    mock_database_connection[0].close.assert_called_once()
    assert db_connection.connection is None

def test_add_item_to_cart_db(mock_database_connection):
    query = 'INSERT INTO cart (item) VALUES (?)'
    params = ['item1']
    add_item_to_cart_db(query, params)
    mock_database_connection[1].execute.assert_called_once_with(query, params)
    mock_database_connection[0].commit.assert_called_once()
    mock_database_connection[0].close.assert_called_once()

# happy path - connect - Test that the database connection is established successfully
def test_connect_successful(db_connection):
    db_connection.connect()
    assert db_connection.connection is not None


# happy path - execute - Test that a query executes successfully without parameters
def test_execute_query_without_params(db_connection, mock_database_connection):
    query = 'CREATE TABLE test (id INTEGER)'
    db_connection.execute(query)
    mock_database_connection[1].execute.assert_called_once_with(query, [])


# happy path - execute - Test that a query executes successfully with parameters
def test_execute_query_with_params(db_connection, mock_database_connection):
    query = 'INSERT INTO test (id) VALUES (?)'
    params = [1]
    db_connection.execute(query, params)
    mock_database_connection[1].execute.assert_called_once_with(query, params)


# happy path - fetchone - Test that fetchone returns a single result
def test_fetchone_single_result(db_connection, mock_database_connection):
    query = 'SELECT * FROM test WHERE id = ?'
    params = [1]
    db_connection.fetchone(query, params)
    mock_database_connection[1].execute.assert_called_once_with(query, params)


# happy path - fetchall - Test that fetchall returns multiple results
def test_fetchall_multiple_results(db_connection, mock_database_connection):
    query = 'SELECT * FROM test'
    db_connection.fetchall(query)
    mock_database_connection[1].execute.assert_called_once_with(query, [])


# edge case - connect - Test that connect raises an error with invalid path
def test_connect_invalid_path():
    db_path = 'invalid_path.db'
    database = DatabaseConnection(db_path)
    with pytest.raises(sqlite3.OperationalError):
        database.connect()


# edge case - execute - Test execute with a malformed query
def test_execute_malformed_query(db_connection, mock_database_connection):
    query = 'MALFORMED QUERY'
    with pytest.raises(sqlite3.OperationalError):
        db_connection.execute(query)
    mock_database_connection[1].execute.assert_called_once_with(query, [])


# edge case - fetchone - Test fetchone with no matching records
def test_fetchone_no_matching_records(db_connection, mock_database_connection):
    query = 'SELECT * FROM test WHERE id = ?'
    params = [999]
    result = db_connection.fetchone(query, params)
    mock_database_connection[1].execute.assert_called_once_with(query, params)
    assert result is None


# edge case - fetchall - Test fetchall with an empty table
def test_fetchall_empty_table(db_connection, mock_database_connection):
    query = 'SELECT * FROM test'
    mock_database_connection[1].fetchall.return_value = []
    results = db_connection.fetchall(query)
    mock_database_connection[1].execute.assert_called_once_with(query, [])
    assert results == []


# edge case - close - Test close method on an already closed connection
def test_close_already_closed_connection(db_connection, mock_database_connection):
    db_connection.close()
    db_connection.close()  # Close again
    mock_database_connection[0].close.assert_called_once()
    assert db_connection.connection is None


