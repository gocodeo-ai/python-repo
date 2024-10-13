import pytest
from unittest import mock
import sqlite3
from shopping_cart.database import DatabaseConnection, add_item_to_cart_db

@pytest.fixture
def mock_database_connection():
    with mock.patch('shopping_cart.database.sqlite3.connect') as mock_connect:
        mock_connection = mock.Mock()
        mock_connect.return_value = mock_connection
        
        # Mocking the cursor and its methods
        mock_cursor = mock.Mock()
        mock_connection.cursor.return_value = mock_cursor
        
        yield mock_connection, mock_cursor

@pytest.fixture
def db_connection(mock_database_connection):
    connection, cursor = mock_database_connection
    db = DatabaseConnection('valid_db_path.db')
    db.connection = connection
    return db

def test_connect_success(db_connection):
    db_connection.connect()
    assert db_connection.connection is not None

def test_execute_query_no_params(db_connection):
    db_connection.connect()
    db_connection.execute('CREATE TABLE test (id INTEGER)')
    db_connection.commit()
    db_connection.close()

def test_execute_query_with_params(db_connection):
    db_connection.connect()
    db_connection.execute('INSERT INTO test (id) VALUES (?)', [1])
    db_connection.commit()
    db_connection.close()

def test_fetchone_success(db_connection):
    db_connection.connect()
    db_connection.fetchone('SELECT id FROM test WHERE id = ?', [1])
    db_connection.close()

def test_fetchall_success(db_connection):
    db_connection.connect()
    db_connection.fetchall('SELECT id FROM test')
    db_connection.close()

def test_commit_success(db_connection):
    db_connection.connect()
    db_connection.commit()
    db_connection.close()

def test_close_success(db_connection):
    db_connection.connect()
    db_connection.close()
    assert db_connection.connection is None

def test_add_item_to_cart_db(mock_database_connection):
    connection, cursor = mock_database_connection
    add_item_to_cart_db('INSERT INTO cart (item) VALUES (?)', ['apple'])
    cursor.execute.assert_called_once_with('INSERT INTO cart (item) VALUES (?)', ['apple'])

# happy path - connect - Test that the database connection is established successfully
def test_connect_success(db_connection):
    db_connection.connect()
    assert db_connection.connection is not None


# happy path - execute - Test that a query executes without parameters successfully
def test_execute_query_no_params(db_connection):
    db_connection.connect()
    db_connection.execute('CREATE TABLE test (id INTEGER)')
    db_connection.commit()
    db_connection.close()


# happy path - execute - Test that a query executes with parameters successfully
def test_execute_query_with_params(db_connection):
    db_connection.connect()
    db_connection.execute('INSERT INTO test (id) VALUES (?)', [1])
    db_connection.commit()
    db_connection.close()


# happy path - fetchone - Test that fetchone retrieves a single row correctly
def test_fetchone_success(db_connection):
    db_connection.connect()
    result = db_connection.fetchone('SELECT id FROM test WHERE id = ?', [1])
    assert result == [1]
    db_connection.close()


# happy path - fetchall - Test that fetchall retrieves all rows correctly
def test_fetchall_success(db_connection):
    db_connection.connect()
    results = db_connection.fetchall('SELECT id FROM test')
    assert results == [[1]]
    db_connection.close()


# happy path - commit - Test that commit saves changes to the database
def test_commit_success(db_connection):
    db_connection.connect()
    db_connection.commit()
    db_connection.close()


# happy path - close - Test that close closes the database connection
def test_close_success(db_connection):
    db_connection.connect()
    db_connection.close()
    assert db_connection.connection is None


# happy path - add_item_to_cart_db - Test that add_item_to_cart_db adds an item successfully
def test_add_item_to_cart_db_success(mock_database_connection):
    connection, cursor = mock_database_connection
    add_item_to_cart_db('INSERT INTO cart (item) VALUES (?)', ['apple'])
    cursor.execute.assert_called_once_with('INSERT INTO cart (item) VALUES (?)', ['apple'])


# edge case - connect - Test that connect raises an error with an invalid path
def test_connect_invalid_path():
    with pytest.raises(sqlite3.OperationalError):
        db = DatabaseConnection('invalid_path.db')
        db.connect()


# edge case - execute - Test that execute raises an error with invalid SQL
def test_execute_invalid_sql(db_connection):
    db_connection.connect()
    with pytest.raises(sqlite3.OperationalError):
        db_connection.execute('INVALID SQL')


# edge case - fetchone - Test that fetchone returns None when no rows match
def test_fetchone_no_match(db_connection):
    db_connection.connect()
    result = db_connection.fetchone('SELECT id FROM test WHERE id = ?', [999])
    assert result is None
    db_connection.close()


# edge case - fetchall - Test that fetchall returns an empty list when no rows exist
def test_fetchall_no_rows(db_connection):
    db_connection.connect()
    results = db_connection.fetchall('SELECT id FROM empty_table')
    assert results == []
    db_connection.close()


# edge case - close - Test that close handles being called when connection is None
def test_close_no_connection(db_connection):
    db_connection.close()
    assert db_connection.connection is None


# edge case - add_item_to_cart_db - Test that add_item_to_cart_db handles empty parameters correctly
def test_add_item_to_cart_db_empty_params(mock_database_connection):
    connection, cursor = mock_database_connection
    with pytest.raises(sqlite3.IntegrityError):
        add_item_to_cart_db('INSERT INTO cart (item) VALUES (?)', [])


