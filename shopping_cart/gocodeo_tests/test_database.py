import pytest
import sqlite3
import os
from unittest import mock
from your_module import DatabaseConnection, add_item_to_cart_db

@pytest.fixture
def mock_sqlite_connect():
    with mock.patch('sqlite3.connect') as mock_connect:
        yield mock_connect

@pytest.fixture
def mock_os_path():
    with mock.patch('os.path') as mock_path:
        mock_path.dirname.return_value = '/fake/dir'
        mock_path.abspath.return_value = '/fake/dir/shopping_cart.db'
        mock_path.join.return_value = '/fake/dir/shopping_cart.db'
        yield mock_path

@pytest.fixture
def db_connection(mock_sqlite_connect, mock_os_path):
    db_path = '/fake/dir/shopping_cart.db'
    db_conn = DatabaseConnection(db_path)
    yield db_conn

@pytest.fixture
def mock_cursor():
    mock_cursor = mock.Mock()
    yield mock_cursor

@pytest.fixture
def mock_connection(mock_cursor):
    mock_connection = mock.Mock()
    mock_connection.cursor.return_value = mock_cursor
    yield mock_connection

@pytest.fixture
def setup_database_connection(mock_sqlite_connect, mock_connection):
    mock_sqlite_connect.return_value = mock_connection
    yield mock_sqlite_connect, mock_connection

@pytest.fixture
def setup_add_item_to_cart_db(setup_database_connection):
    mock_sqlite_connect, mock_connection = setup_database_connection
    yield mock_sqlite_connect, mock_connection

# happy_path - __init__ - Test that the database connection is initialized with the correct database path.
def test_init_with_valid_db_path():
    db_path = 'shopping_cart.db'
    db_conn = DatabaseConnection(db_path)
    assert db_conn.connection is None
    assert db_conn.db_path == db_path

# happy_path - connect - Test that the connect method establishes a connection to the database.
def test_connect_establishes_connection(setup_database_connection):
    mock_sqlite_connect, mock_connection = setup_database_connection
    db_conn = DatabaseConnection('/fake/dir/shopping_cart.db')
    db_conn.connect()
    mock_sqlite_connect.assert_called_once_with('/fake/dir/shopping_cart.db')
    assert db_conn.connection == mock_connection

# happy_path - execute - Test that the execute method runs a query without parameters successfully.
def test_execute_query_without_params(setup_database_connection, mock_cursor):
    mock_sqlite_connect, mock_connection = setup_database_connection
    db_conn = DatabaseConnection('/fake/dir/shopping_cart.db')
    db_conn.connect()
    db_conn.execute('CREATE TABLE test (id INTEGER)')
    mock_cursor.execute.assert_called_once_with('CREATE TABLE test (id INTEGER)', [])

# happy_path - fetchone - Test that fetchone retrieves a single record from the database.
def test_fetchone_retrieves_single_record(setup_database_connection, mock_cursor):
    mock_cursor.fetchone.return_value = 1
    mock_sqlite_connect, mock_connection = setup_database_connection
    db_conn = DatabaseConnection('/fake/dir/shopping_cart.db')
    db_conn.connect()
    result = db_conn.fetchone('SELECT 1')
    mock_cursor.execute.assert_called_once_with('SELECT 1', [])
    assert result == 1

# happy_path - fetchall - Test that fetchall retrieves all records from the database.
def test_fetchall_retrieves_all_records(setup_database_connection, mock_cursor):
    mock_cursor.fetchall.return_value = [1, 2, 3]
    mock_sqlite_connect, mock_connection = setup_database_connection
    db_conn = DatabaseConnection('/fake/dir/shopping_cart.db')
    db_conn.connect()
    results = db_conn.fetchall('SELECT * FROM test')
    mock_cursor.execute.assert_called_once_with('SELECT * FROM test', [])
    assert results == [1, 2, 3]

# happy_path - commit - Test that commit saves changes to the database.
def test_commit_saves_changes(setup_database_connection):
    mock_sqlite_connect, mock_connection = setup_database_connection
    db_conn = DatabaseConnection('/fake/dir/shopping_cart.db')
    db_conn.connect()
    db_conn.commit()
    mock_connection.commit.assert_called_once()

# happy_path - close - Test that close method closes the database connection.
def test_close_closes_connection(setup_database_connection):
    mock_sqlite_connect, mock_connection = setup_database_connection
    db_conn = DatabaseConnection('/fake/dir/shopping_cart.db')
    db_conn.connect()
    db_conn.close()
    mock_connection.close.assert_called_once()
    assert db_conn.connection is None

# happy_path - add_item_to_cart_db - Test that add_item_to_cart_db adds an item to the cart database.
def test_add_item_to_cart_db_adds_item(setup_add_item_to_cart_db, mock_cursor):
    mock_sqlite_connect, mock_connection = setup_add_item_to_cart_db
    add_item_to_cart_db('INSERT INTO cart (item) VALUES (?)', ['apple'])
    mock_cursor.execute.assert_called_once_with('INSERT INTO cart (item) VALUES (?)', ['apple'])
    mock_connection.commit.assert_called_once()

# edge_case - __init__ - Test that __init__ handles an empty database path gracefully.
def test_init_with_empty_db_path():
    db_path = ''
    db_conn = DatabaseConnection(db_path)
    assert db_conn.connection is None
    assert db_conn.db_path == db_path

# edge_case - connect - Test that connect handles invalid database path by raising an exception.
def test_connect_with_invalid_path_raises_exception(mock_sqlite_connect):
    mock_sqlite_connect.side_effect = sqlite3.OperationalError
    db_conn = DatabaseConnection('invalid_path')
    with pytest.raises(sqlite3.OperationalError):
        db_conn.connect()

# edge_case - execute - Test that execute method handles invalid SQL syntax gracefully.
def test_execute_with_invalid_sql_syntax(setup_database_connection):
    mock_sqlite_connect, mock_connection = setup_database_connection
    mock_cursor = mock_connection.cursor.return_value
    mock_cursor.execute.side_effect = sqlite3.Error
    db_conn = DatabaseConnection('/fake/dir/shopping_cart.db')
    db_conn.connect()
    with pytest.raises(sqlite3.Error):
        db_conn.execute('INVALID SQL')

# edge_case - fetchone - Test that fetchone returns None when no records are found.
def test_fetchone_returns_none_if_no_records(setup_database_connection, mock_cursor):
    mock_cursor.fetchone.return_value = None
    mock_sqlite_connect, mock_connection = setup_database_connection
    db_conn = DatabaseConnection('/fake/dir/shopping_cart.db')
    db_conn.connect()
    result = db_conn.fetchone('SELECT * FROM test WHERE id = 999')
    assert result is None

# edge_case - fetchall - Test that fetchall returns an empty list when no records exist.
def test_fetchall_returns_empty_list_if_no_records(setup_database_connection, mock_cursor):
    mock_cursor.fetchall.return_value = []
    mock_sqlite_connect, mock_connection = setup_database_connection
    db_conn = DatabaseConnection('/fake/dir/shopping_cart.db')
    db_conn.connect()
    results = db_conn.fetchall('SELECT * FROM test WHERE id = 999')
    assert results == []

# edge_case - close - Test that close method does nothing if connection is already closed.
def test_close_does_nothing_if_already_closed():
    db_conn = DatabaseConnection('/fake/dir/shopping_cart.db')
    db_conn.close()
    assert db_conn.connection is None

# edge_case - add_item_to_cart_db - Test that add_item_to_cart_db handles empty query gracefully.
def test_add_item_to_cart_db_with_empty_query(setup_add_item_to_cart_db):
    mock_sqlite_connect, mock_connection = setup_add_item_to_cart_db
    mock_cursor = mock_connection.cursor.return_value
    mock_cursor.execute.side_effect = sqlite3.Error
    with pytest.raises(sqlite3.Error):
        add_item_to_cart_db('', [])

