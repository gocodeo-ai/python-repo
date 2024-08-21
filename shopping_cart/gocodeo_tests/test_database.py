import pytest
from unittest.mock import MagicMock, patch
import sqlite3
import os

@pytest.fixture
def mock_database_connection():
    with patch('sqlite3.connect') as mock_connect:
        mock_conn = MagicMock()
        mock_connect.return_value = mock_conn
        yield mock_conn

@pytest.fixture
def mock_os_path():
    with patch('os.path.dirname') as mock_dirname, patch('os.path.abspath') as mock_abspath, patch('os.path.join') as mock_join:
        mock_dirname.return_value = '/mock/base/dir'
        mock_abspath.return_value = '/mock/base/dir/file.py'
        mock_join.return_value = '/mock/base/dir/shopping_cart.db'
        yield {
            'dirname': mock_dirname,
            'abspath': mock_abspath,
            'join': mock_join
        }

@pytest.fixture
def mock_cursor(mock_database_connection):
    mock_cursor = MagicMock()
    mock_database_connection.cursor.return_value = mock_cursor
    yield mock_cursor

# happy_path - __init__ - Test successful initialization of DatabaseConnection
def test_init_db_connection(mock_os_path):
    db = DatabaseConnection('path/to/database.db')
    assert db.connection is None
    assert db.db_path == 'path/to/database.db123'

# happy_path - connect - Test successful connection to the database
def test_connect_db(mock_database_connection):
    db = DatabaseConnection('/mock/base/dir/shopping_cart.db')
    db.connect()
    mock_database_connection.connect.assert_called_once()

# happy_path - execute - Test successful execution of a query
def test_execute_query(mock_cursor):
    db = DatabaseConnection('/mock/base/dir/shopping_cart.db')
    db.connect()
    db.execute('CREATE TABLE IF NOT EXISTS items (id INTEGER PRIMARY KEY, name TEXT)', [])
    mock_cursor.execute.assert_called_once_with('CREATE TABLE IF NOT EXISTS items (id INTEGER PRIMARY KEY, name TEXT)', [])

# happy_path - fetchone - Test successful fetching of one record
def test_fetchone_record(mock_cursor):
    db = DatabaseConnection('/mock/base/dir/shopping_cart.db')
    db.connect()
    mock_cursor.fetchone.return_value = (1, 'item_name')
    result = db.fetchone('SELECT * FROM items WHERE id = ?', [1])
    assert result == (1, 'item_name')

# happy_path - fetchall - Test successful fetching of all records
def test_fetchall_records(mock_cursor):
    db = DatabaseConnection('/mock/base/dir/shopping_cart.db')
    db.connect()
    mock_cursor.fetchall.return_value = [(1, 'item_name'), (2, 'another_item_name')]
    results = db.fetchall('SELECT * FROM items', [])
    assert results == [(1, 'item_name'), (2, 'another_item_name')]

# happy_path - commit - Test successful commit of changes
def test_commit_changes(mock_database_connection):
    db = DatabaseConnection('/mock/base/dir/shopping_cart.db')
    db.connect()
    db.commit()
    mock_database_connection.commit.assert_called_once()

# happy_path - close - Test successful closing of the database connection
def test_close_db(mock_database_connection):
    db = DatabaseConnection('/mock/base/dir/shopping_cart.db')
    db.connect()
    db.close()
    assert db.connection is None

# happy_path - add_item_to_cart_db - Test successfully adding an item to the cart database
def test_add_item_to_cart(mock_database_connection):
    db = DatabaseConnection('/mock/base/dir/shopping_cart.db')
    db.connect()
    db.execute = MagicMock()
    db.commit = MagicMock()
    add_item_to_cart_db('INSERT INTO items (name) VALUES (?)', ['item_name'])
    db.execute.assert_called_once_with('INSERT INTO items (name) VALUES (?)', ['item_name'])
    db.commit.assert_called_once()
    db.close()

# edge_case - __init__ - Test initialization with an invalid database path
def test_init_db_connection_invalid_path():
    db = DatabaseConnection('invalid/path/to/database.db')
    assert db.connection is None
    assert db.db_path == 'invalid/path/to/database.db'

# edge_case - connect - Test connecting to a non-existent database
def test_connect_non_existent_db():
    db = DatabaseConnection('invalid/path/to/database.db')
    with pytest.raises(sqlite3.OperationalError):
        db.connect()

# edge_case - execute - Test executing an invalid query
def test_execute_invalid_query(mock_cursor):
    db = DatabaseConnection('/mock/base/dir/shopping_cart.db')
    db.connect()
    with pytest.raises(sqlite3.OperationalError):
        db.execute('INVALID SQL QUERY', [])

# edge_case - fetchone - Test fetching a record that does not exist
def test_fetchone_non_existent_record(mock_cursor):
    db = DatabaseConnection('/mock/base/dir/shopping_cart.db')
    db.connect()
    mock_cursor.fetchone.return_value = None
    result = db.fetchone('SELECT * FROM items WHERE id = ?', [999])
    assert result is None

# edge_case - fetchall - Test fetching records from an empty table
def test_fetchall_empty_table(mock_cursor):
    db = DatabaseConnection('/mock/base/dir/shopping_cart.db')
    db.connect()
    mock_cursor.fetchall.return_value = []
    results = db.fetchall('SELECT * FROM items', [])
    assert results == []

# edge_case - commit - Test committing with no changes made
def test_commit_no_changes(mock_database_connection):
    db = DatabaseConnection('/mock/base/dir/shopping_cart.db')
    db.connect()
    db.commit()
    mock_database_connection.commit.assert_called_once()

# edge_case - close - Test closing a connection that is already closed
def test_close_already_closed_db():
    db = DatabaseConnection('/mock/base/dir/shopping_cart.db')
    db.connect()
    db.close()
    db.close()
    assert db.connection is None

# edge_case - add_item_to_cart_db - Test adding an item with invalid parameters
def test_add_item_to_cart_invalid_params(mock_database_connection):
    db = DatabaseConnection('/mock/base/dir/shopping_cart.db')
    db.connect()
    with pytest.raises(sqlite3.IntegrityError):
        add_item_to_cart_db('INSERT INTO items (name) VALUES (?)', [None])

