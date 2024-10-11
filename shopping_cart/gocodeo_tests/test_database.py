import pytest
from unittest import mock
import sqlite3
from shopping_cart.database import DatabaseConnection, add_item_to_cart_db

@pytest.fixture
def mock_database_connection():
    with mock.patch('shopping_cart.database.sqlite3.connect') as mock_connect:
        mock_conn = mock.Mock()
        mock_connect.return_value = mock_conn
        
        db_connection = DatabaseConnection("shopping_cart.db")
        db_connection.connect()
        
        yield db_connection, mock_conn

        db_connection.close()

@pytest.fixture
def mock_cursor(mock_database_connection):
    db_connection, mock_conn = mock_database_connection
    mock_cursor = mock.Mock()
    mock_conn.cursor.return_value = mock_cursor
    
    yield mock_cursor

def test_connect_success(mock_database_connection):
    db_connection, mock_conn = mock_database_connection
    assert db_connection.connection is not None

def test_execute_query_no_params(mock_cursor, mock_database_connection):
    db_connection, mock_conn = mock_database_connection
    query = 'CREATE TABLE IF NOT EXISTS cart (id INTEGER PRIMARY KEY)'
    db_connection.execute(query)
    mock_cursor.execute.assert_called_once_with(query, [])

def test_execute_query_with_params(mock_cursor, mock_database_connection):
    db_connection, mock_conn = mock_database_connection
    query = 'INSERT INTO cart (id) VALUES (?)'
    params = [1]
    db_connection.execute(query, params)
    mock_cursor.execute.assert_called_once_with(query, params)

def test_fetchone_success(mock_cursor, mock_database_connection):
    db_connection, mock_conn = mock_database_connection
    query = 'SELECT * FROM cart WHERE id = ?'
    params = [1]
    mock_cursor.fetchone.return_value = ('result',)
    result = db_connection.fetchone(query, params)
    assert result is not None

def test_fetchall_success(mock_cursor, mock_database_connection):
    db_connection, mock_conn = mock_database_connection
    query = 'SELECT * FROM cart'
    mock_cursor.fetchall.return_value = [('result1',), ('result2',)]
    results = db_connection.fetchall(query)
    assert isinstance(results, list)

def test_close_success(mock_database_connection):
    db_connection, mock_conn = mock_database_connection
    db_connection.close()
    assert db_connection.connection is None

def test_add_item_to_cart_success(mock_cursor, mock_database_connection):
    query = 'INSERT INTO cart (id, name) VALUES (?, ?)'
    params = [1, 'apple']
    add_item_to_cart_db(query, params)
    mock_cursor.execute.assert_called_once_with(query, params)

def test_commit_after_insert(mock_database_connection):
    db_connection, mock_conn = mock_database_connection
    db_connection.commit()
    mock_conn.commit.assert_called_once()

def test_execute_without_connection(mock_cursor):
    db_connection = DatabaseConnection("shopping_cart.db")
    with pytest.raises(sqlite3.OperationalError):
        db_connection.execute('SELECT * FROM cart')

def test_fetchone_no_record(mock_cursor, mock_database_connection):
    db_connection, mock_conn = mock_database_connection
    query = 'SELECT * FROM cart WHERE id = ?'
    params = [999]
    mock_cursor.fetchone.return_value = None
    result = db_connection.fetchone(query, params)
    assert result is None

def test_fetchall_empty_table(mock_cursor, mock_database_connection):
    db_connection, mock_conn = mock_database_connection
    query = 'SELECT * FROM cart'
    mock_cursor.fetchall.return_value = []
    results = db_connection.fetchall(query)
    assert results == []

def test_commit_no_changes(mock_database_connection):
    db_connection, mock_conn = mock_database_connection
    db_connection.commit()
    mock_conn.commit.assert_called_once()

def test_close_twice(mock_database_connection):
    db_connection, mock_conn = mock_database_connection
    db_connection.close()
    db_connection.close()  # Second close should not raise an error

# happy path - connect - Test that a connection to the database is established successfully
def test_connect_success(mock_database_connection):
    db_connection, mock_conn = mock_database_connection
    assert db_connection.connection is not None
    print(f"Connection established: {db_connection.connection}")


# happy path - execute - Test that a query is executed successfully without parameters
def test_execute_query_no_params(mock_cursor, mock_database_connection):
    db_connection, mock_conn = mock_database_connection
    query = 'CREATE TABLE IF NOT EXISTS cart (id INTEGER PRIMARY KEY)'
    db_connection.execute(query)
    mock_cursor.execute.assert_called_once_with(query, [])


# happy path - execute - Test that a query is executed successfully with parameters
def test_execute_query_with_params(mock_cursor, mock_database_connection):
    db_connection, mock_conn = mock_database_connection
    query = 'INSERT INTO cart (id) VALUES (?)'
    params = [1]
    db_connection.execute(query, params)
    mock_cursor.execute.assert_called_once_with(query, params)


# happy path - fetchone - Test that fetchone retrieves a single record successfully
def test_fetchone_success(mock_cursor, mock_database_connection):
    db_connection, mock_conn = mock_database_connection
    query = 'SELECT * FROM cart WHERE id = ?'
    params = [1]
    mock_cursor.fetchone.return_value = ('result',)
    result = db_connection.fetchone(query, params)
    assert result is not None


# happy path - fetchall - Test that fetchall retrieves all records successfully
def test_fetchall_success(mock_cursor, mock_database_connection):
    db_connection, mock_conn = mock_database_connection
    query = 'SELECT * FROM cart'
    mock_cursor.fetchall.return_value = [('result1',), ('result2',)]
    results = db_connection.fetchall(query)
    assert isinstance(results, list)


# edge case - execute - Test that executing a query without a connection raises an exception
def test_execute_without_connection(mock_cursor):
    db_connection = DatabaseConnection("shopping_cart.db")
    with pytest.raises(sqlite3.OperationalError):
        db_connection.execute('SELECT * FROM cart')


# edge case - fetchone - Test that fetchone returns None for non-existent record
def test_fetchone_no_record(mock_cursor, mock_database_connection):
    db_connection, mock_conn = mock_database_connection
    query = 'SELECT * FROM cart WHERE id = ?'
    params = [999]
    mock_cursor.fetchone.return_value = None
    result = db_connection.fetchone(query, params)
    assert result is None


# edge case - fetchall - Test that fetchall returns an empty list for an empty table
def test_fetchall_empty_table(mock_cursor, mock_database_connection):
    db_connection, mock_conn = mock_database_connection
    query = 'SELECT * FROM cart'
    mock_cursor.fetchall.return_value = []
    results = db_connection.fetchall(query)
    assert results == []


# edge case - commit - Test that commit without changes does not raise an error
def test_commit_no_changes(mock_database_connection):
    db_connection, mock_conn = mock_database_connection
    db_connection.commit()
    mock_conn.commit.assert_called_once()


# edge case - close - Test that closing a connection twice does not raise an error
def test_close_twice(mock_database_connection):
    db_connection, mock_conn = mock_database_connection
    db_connection.close()
    db_connection.close()  # Second close should not raise an error


# happy path - close - Test that a connection to the database is closed successfully
def test_close_success(mock_database_connection):
    db_connection, mock_conn = mock_database_connection
    db_connection.close()
    assert db_connection.connection is None


# happy path - add_item_to_cart_db - Test that adding an item to the cart inserts a record successfully
def test_add_item_to_cart_success(mock_cursor, mock_database_connection):
    query = 'INSERT INTO cart (id, name) VALUES (?, ?)'
    params = [1, 'apple']
    add_item_to_cart_db(query, params)
    mock_cursor.execute.assert_called_once_with(query, params)


# happy path - commit - Test that commit after inserting a record is successful
def test_commit_after_insert(mock_database_connection):
    db_connection, mock_conn = mock_database_connection
    db_connection.commit()
    mock_conn.commit.assert_called_once()


