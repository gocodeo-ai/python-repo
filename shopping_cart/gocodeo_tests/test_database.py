import pytest
from unittest import mock
import sqlite3
import os

@pytest.fixture
def mock_db_connection():
    with mock.patch('sqlite3.connect') as mock_connect:
        mock_connection = mock.Mock()
        mock_cursor = mock.Mock()
        mock_connect.return_value = mock_connection
        mock_connection.cursor.return_value = mock_cursor
        yield mock_connection, mock_cursor

@pytest.fixture
def mock_os_path():
    with mock.patch('os.path.dirname') as mock_dirname, \
         mock.patch('os.path.abspath') as mock_abspath, \
         mock.patch('os.path.join') as mock_join:
        mock_dirname.return_value = 'mock_base_dir'
        mock_abspath.return_value = 'mock_base_dir/__file__'
        mock_join.return_value = 'mock_base_dir/shopping_cart.db'
        yield

@pytest.fixture
def mock_database_connection(mock_db_connection, mock_os_path):
    from your_module import DatabaseConnection
    db_path = 'mock_base_dir/shopping_cart.db'
    db_connection = DatabaseConnection(db_path)
    yield db_connection, mock_db_connection[0], mock_db_connection[1]# happy_path - __init__ - Test successful initialization of DatabaseConnection
def test_database_connection_init(mock_database_connection):
    db_connection, _, _ = mock_database_connection
    assert db_connection.connection is None
    assert db_connection.db_path == 'mock_base_dir/shopping_cart.db'

# happy_path - connect - Test successful connection to the database
def test_database_connection_connect(mock_database_connection):
    db_connection, mock_connection, _ = mock_database_connection
    db_connection.connect()
    mock_connection.cursor.assert_called_once()

# happy_path - execute - Test successful execution of a query
def test_database_connection_execute(mock_database_connection):
    db_connection, mock_connection, mock_cursor = mock_database_connection
    query = 'CREATE TABLE IF NOT EXISTS items (id INTEGER PRIMARY KEY, name TEXT)'
    db_connection.execute(query)
    mock_cursor.execute.assert_called_once_with(query, [])

# happy_path - fetchone - Test successful fetching of one record
def test_database_connection_fetchone(mock_database_connection):
    db_connection, mock_connection, mock_cursor = mock_database_connection
    mock_cursor.fetchone.return_value = (1, 'item_name')
    result = db_connection.fetchone('SELECT * FROM items WHERE id = 1')
    assert result == (1, 'item_name')

# happy_path - fetchall - Test successful fetching of all records
def test_database_connection_fetchall(mock_database_connection):
    db_connection, mock_connection, mock_cursor = mock_database_connection
    mock_cursor.fetchall.return_value = [(1, 'item_name')]
    results = db_connection.fetchall('SELECT * FROM items')
    assert results == [(1, 'item_name')]

# happy_path - commit - Test successful commit of changes
def test_database_connection_commit(mock_database_connection):
    db_connection, mock_connection, _ = mock_database_connection
    db_connection.commit()
    mock_connection.commit.assert_called_once()

# happy_path - close - Test successful closing of the database connection
def test_database_connection_close(mock_database_connection):
    db_connection, mock_connection, _ = mock_database_connection
    db_connection.close()
    assert db_connection.connection is None

# happy_path - add_item_to_cart_db - Test adding an item to the cart database
def test_add_item_to_cart_db(mock_database_connection):
    db_connection, mock_connection, mock_cursor = mock_database_connection
    query = 'INSERT INTO items (name) VALUES (?)'
    params = ['item_name']
    db_connection.execute = mock.Mock()
    db_connection.commit = mock.Mock()
    db_connection.add_item_to_cart_db(query, params)
    db_connection.execute.assert_called_once_with(query, params)
    db_connection.commit.assert_called_once()

# edge_case - __init__ - Test initialization with an invalid database path
def test_database_connection_init_invalid_path():
    with pytest.raises(Exception):
        DatabaseConnection('invalid_path/shopping_cart.db')

# edge_case - connect - Test connection failure
def test_database_connection_connect_failure(mock_database_connection):
    db_connection, mock_connection, _ = mock_database_connection
    mock_connection.side_effect = sqlite3.OperationalError('Connection failed')
    with pytest.raises(sqlite3.OperationalError):
        db_connection.connect()

# edge_case - execute - Test execution of an invalid query
def test_database_connection_execute_invalid_query(mock_database_connection):
    db_connection, _, mock_cursor = mock_database_connection
    mock_cursor.execute.side_effect = sqlite3.OperationalError('Execution failed')
    with pytest.raises(sqlite3.OperationalError):
        db_connection.execute('INVALID QUERY')

# edge_case - fetchone - Test fetching one record from an empty table
def test_database_connection_fetchone_empty_table(mock_database_connection):
    db_connection, mock_connection, mock_cursor = mock_database_connection
    mock_cursor.fetchone.return_value = None
    result = db_connection.fetchone('SELECT * FROM items WHERE id = 999')
    assert result is None

# edge_case - fetchall - Test fetching all records from an empty table
def test_database_connection_fetchall_empty_table(mock_database_connection):
    db_connection, mock_connection, mock_cursor = mock_database_connection
    mock_cursor.fetchall.return_value = []
    results = db_connection.fetchall('SELECT * FROM items')
    assert results == []

# edge_case - commit - Test committing without any changes
def test_database_connection_commit_no_changes(mock_database_connection):
    db_connection, mock_connection, _ = mock_database_connection
    db_connection.commit()
    mock_connection.commit.assert_called_once()

# edge_case - close - Test closing an already closed connection
def test_database_connection_close_already_closed(mock_database_connection):
    db_connection, _, _ = mock_database_connection
    db_connection.close()
    with pytest.raises(Exception):
        db_connection.close()

# edge_case - add_item_to_cart_db - Test adding an item with invalid parameters
def test_add_item_to_cart_db_invalid_params(mock_database_connection):
    db_connection, mock_connection, mock_cursor = mock_database_connection
    query = 'INSERT INTO items (name) VALUES (?)'
    params = [None]
    with pytest.raises(Exception):
        db_connection.add_item_to_cart_db(query, params)

