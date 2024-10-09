import pytest
from unittest import mock
import sqlite3
from shopping_cart.database import DatabaseConnection, add_item_to_cart_db

@pytest.fixture
def mock_db_connection():
    with mock.patch('shopping_cart.database.sqlite3.connect') as mock_connect:
        mock_connection = mock.Mock()
        mock_connect.return_value = mock_connection
        
        # Mock cursor and its methods
        mock_cursor = mock.Mock()
        mock_connection.cursor.return_value = mock_cursor

        yield mock_connection, mock_cursor

def test_connect_success(mock_db_connection):
    db_connection, _ = mock_db_connection
    database = DatabaseConnection('shopping_cart.db')
    database.connect()
    assert database.connection is db_connection

def test_execute_no_params(mock_db_connection):
    _, mock_cursor = mock_db_connection
    database = DatabaseConnection('shopping_cart.db')
    database.connect()
    database.execute('CREATE TABLE IF NOT EXISTS cart (id INTEGER PRIMARY KEY)')
    mock_cursor.execute.assert_called_once_with('CREATE TABLE IF NOT EXISTS cart (id INTEGER PRIMARY KEY)', [])

def test_execute_with_params(mock_db_connection):
    _, mock_cursor = mock_db_connection
    database = DatabaseConnection('shopping_cart.db')
    database.connect()
    database.execute('INSERT INTO cart (id) VALUES (?)', [1])
    mock_cursor.execute.assert_called_once_with('INSERT INTO cart (id) VALUES (?)', [1])

def test_fetchone_success(mock_db_connection):
    _, mock_cursor = mock_db_connection
    database = DatabaseConnection('shopping_cart.db')
    mock_cursor.fetchone.return_value = [1]
    database.connect()
    result = database.fetchone('SELECT id FROM cart WHERE id = ?', [1])
    assert result == [1]

def test_fetchall_success(mock_db_connection):
    _, mock_cursor = mock_db_connection
    database = DatabaseConnection('shopping_cart.db')
    mock_cursor.fetchall.return_value = [[1]]
    database.connect()
    results = database.fetchall('SELECT id FROM cart')
    assert results == [[1]]

def test_commit_success(mock_db_connection):
    db_connection, _ = mock_db_connection
    database = DatabaseConnection('shopping_cart.db')
    database.connect()
    database.commit()
    db_connection.commit.assert_called_once()

def test_close_success(mock_db_connection):
    db_connection, _ = mock_db_connection
    database = DatabaseConnection('shopping_cart.db')
    database.connect()
    database.close()
    assert database.connection is None

def test_add_item_to_cart_db(mock_db_connection):
    _, mock_cursor = mock_db_connection
    database = DatabaseConnection('shopping_cart.db')
    database.connect()
    add_item_to_cart_db('INSERT INTO cart (id) VALUES (?)', [2])
    mock_cursor.execute.assert_called_once_with('INSERT INTO cart (id) VALUES (?)', [2])
    mock_db_connection[0].commit.assert_called_once()
    mock_db_connection[0].close.assert_called_once()

# happy path - connect - Test that the database connects successfully given a valid path
def test_connect_success(mock_db_connection):
    db_connection, _ = mock_db_connection
    database = DatabaseConnection('shopping_cart.db')
    database.connect()
    assert database.connection is db_connection


# happy path - execute - Test that a query executes successfully without parameters
def test_execute_no_params(mock_db_connection):
    _, mock_cursor = mock_db_connection
    database = DatabaseConnection('shopping_cart.db')
    database.connect()
    database.execute('CREATE TABLE IF NOT EXISTS cart (id INTEGER PRIMARY KEY)')
    mock_cursor.execute.assert_called_once_with('CREATE TABLE IF NOT EXISTS cart (id INTEGER PRIMARY KEY)', [])


# happy path - execute - Test that a query executes successfully with parameters
def test_execute_with_params(mock_db_connection):
    _, mock_cursor = mock_db_connection
    database = DatabaseConnection('shopping_cart.db')
    database.connect()
    database.execute('INSERT INTO cart (id) VALUES (?)', [1])
    mock_cursor.execute.assert_called_once_with('INSERT INTO cart (id) VALUES (?)', [1])


# happy path - fetchone - Test that fetchone retrieves a single row correctly
def test_fetchone_success(mock_db_connection):
    _, mock_cursor = mock_db_connection
    database = DatabaseConnection('shopping_cart.db')
    mock_cursor.fetchone.return_value = [1]
    database.connect()
    result = database.fetchone('SELECT id FROM cart WHERE id = ?', [1])
    assert result == [1]


# happy path - fetchall - Test that fetchall retrieves multiple rows correctly
def test_fetchall_success(mock_db_connection):
    _, mock_cursor = mock_db_connection
    database = DatabaseConnection('shopping_cart.db')
    mock_cursor.fetchall.return_value = [[1]]
    database.connect()
    results = database.fetchall('SELECT id FROM cart')
    assert results == [[1]]


# happy path - commit - Test that commit saves changes to the database
def test_commit_success(mock_db_connection):
    db_connection, _ = mock_db_connection
    database = DatabaseConnection('shopping_cart.db')
    database.connect()
    database.commit()
    db_connection.commit.assert_called_once()


# happy path - close - Test that close method closes the database connection
def test_close_success(mock_db_connection):
    db_connection, _ = mock_db_connection
    database = DatabaseConnection('shopping_cart.db')
    database.connect()
    database.close()
    assert database.connection is None


# happy path - add_item_to_cart_db - Test that add_item_to_cart_db adds an item successfully
def test_add_item_to_cart_db(mock_db_connection):
    _, mock_cursor = mock_db_connection
    add_item_to_cart_db('INSERT INTO cart (id) VALUES (?)', [2])
    mock_cursor.execute.assert_called_once_with('INSERT INTO cart (id) VALUES (?)', [2])
    mock_db_connection[0].commit.assert_called_once()
    mock_db_connection[0].close.assert_called_once()


# edge case - connect - Test that connecting to a non-existent database path raises an error
def test_connect_invalid_path():
    with pytest.raises(sqlite3.OperationalError):
        database = DatabaseConnection('invalid_path.db')
        database.connect()


# edge case - execute - Test that executing a malformed query raises an error
def test_execute_malformed_query(mock_db_connection):
    _, mock_cursor = mock_db_connection
    mock_cursor.execute.side_effect = sqlite3.OperationalError
    database = DatabaseConnection('shopping_cart.db')
    database.connect()
    with pytest.raises(sqlite3.OperationalError):
        database.execute('MALFORMED QUERY')


# edge case - fetchone - Test that fetchone returns None for a non-existent row
def test_fetchone_no_result(mock_db_connection):
    _, mock_cursor = mock_db_connection
    mock_cursor.fetchone.return_value = None
    database = DatabaseConnection('shopping_cart.db')
    database.connect()
    result = database.fetchone('SELECT id FROM cart WHERE id = ?', [999])
    assert result is None


# edge case - fetchall - Test that fetchall returns an empty list for no results
def test_fetchall_no_results(mock_db_connection):
    _, mock_cursor = mock_db_connection
    mock_cursor.fetchall.return_value = []
    database = DatabaseConnection('shopping_cart.db')
    database.connect()
    results = database.fetchall('SELECT id FROM cart WHERE id = ?', [999])
    assert results == []


# edge case - execute - Test that executing a query without a connection raises an error
def test_execute_no_connection():
    database = DatabaseConnection('shopping_cart.db')
    with pytest.raises(sqlite3.ProgrammingError):
        database.execute('SELECT id FROM cart')


# edge case - commit - Test that commit without a connection raises an error
def test_commit_no_connection():
    database = DatabaseConnection('shopping_cart.db')
    with pytest.raises(sqlite3.ProgrammingError):
        database.commit()


# edge case - close - Test that closing an already closed connection does not raise an error
def test_close_already_closed(mock_db_connection):
    db_connection, _ = mock_db_connection
    database = DatabaseConnection('shopping_cart.db')
    database.connect()
    database.close()
    database.close()
    assert database.connection is None


