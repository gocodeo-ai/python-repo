import pytest
from unittest import mock
import sqlite3
import os

@pytest.fixture
def mock_sqlite3_connect():
    with mock.patch('sqlite3.connect') as mock_connect:
        mock_connection = mock.Mock(spec=sqlite3.Connection)
        mock_connect.return_value = mock_connection
        yield mock_connect

@pytest.fixture
def mock_os_path():
    with mock.patch('os.path.dirname') as mock_dirname, \
         mock.patch('os.path.abspath') as mock_abspath, \
         mock.patch('os.path.join') as mock_join:
        
        mock_dirname.return_value = '/mocked/dir'
        mock_abspath.return_value = '/mocked/dir/file.py'
        mock_join.return_value = '/mocked/dir/database.db'
        
        yield mock_dirname, mock_abspath, mock_join

@pytest.fixture
def mock_cursor():
    with mock.patch('sqlite3.Connection.cursor') as mock_cursor:
        mock_cursor_instance = mock.Mock()
        mock_cursor.return_value = mock_cursor_instance
        yield mock_cursor_instance

@pytest.fixture
def mock_db_connection(mock_sqlite3_connect, mock_os_path, mock_cursor):
    from your_module import DatabaseConnection  # Replace 'your_module' with the actual module name
    db_path = '/mocked/dir/database.db'
    db_connection = DatabaseConnection(db_path)
    yield db_connection

# happy_path - __init__ - Test successful initialization of DatabaseConnection
def test_init_db_connection(mock_db_connection):
    assert mock_db_connection.connection is None
    assert mock_db_connection.db_path == 'path/to/database.db'

# happy_path - connect - Test successful connection to database
def test_connect_db(mock_db_connection, mock_sqlite3_connect):
    mock_db_connection.connect()
    mock_sqlite3_connect.assert_called_once_with(mock_db_connection.db_path)

# happy_path - execute - Test successful execution of a query
def test_execute_query(mock_db_connection, mock_cursor):
    query = 'CREATE TABLE IF NOT EXISTS cart (id INTEGER PRIMARY KEY, item TEXT)'
    mock_db_connection.execute(query)
    mock_cursor.execute.assert_called_once_with(query, [])

# happy_path - fetchone - Test successful fetching of one record
def test_fetchone_query(mock_db_connection, mock_cursor):
    mock_cursor.fetchone.return_value = (1, 'example_item')
    result = mock_db_connection.fetchone('SELECT * FROM cart WHERE id = ?', [1])
    assert result == (1, 'example_item')

# happy_path - fetchall - Test successful fetching of all records
def test_fetchall_query(mock_db_connection, mock_cursor):
    mock_cursor.fetchall.return_value = [(1, 'example_item'), (2, 'another_item')]
    results = mock_db_connection.fetchall('SELECT * FROM cart')
    assert results == [(1, 'example_item'), (2, 'another_item')]

# happy_path - commit - Test successful commit of changes
def test_commit_changes(mock_db_connection):
    mock_db_connection.commit()
    mock_db_connection.connection.commit.assert_called_once()

# happy_path - close - Test successful closing of database connection
def test_close_db(mock_db_connection):
    mock_db_connection.close()
    assert mock_db_connection.connection is None

# happy_path - add_item_to_cart_db - Test adding an item to the cart database
def test_add_item_to_cart_db(mock_db_connection):
    query = 'INSERT INTO cart (item) VALUES (?)'
    params = ['new_item']
    mock_db_connection.connect()
    mock_db_connection.execute(query, params)
    mock_db_connection.commit()
    mock_db_connection.close()

# edge_case - __init__ - Test initialization with invalid database path
def test_init_invalid_db_connection():
    db_connection = DatabaseConnection('invalid/path/to/database.db')
    assert db_connection.connection is None
    assert db_connection.db_path == 'invalid/path/to/database.db'

# edge_case - execute - Test executing a malformed query
def test_execute_malformed_query(mock_db_connection, mock_cursor):
    mock_cursor.execute.side_effect = sqlite3.Error
    with pytest.raises(sqlite3.Error):
        mock_db_connection.execute('SELECT * FROM non_existing_table')

# edge_case - fetchone - Test fetching from an empty table
def test_fetchone_empty_table(mock_db_connection, mock_cursor):
    mock_cursor.fetchone.return_value = None
    result = mock_db_connection.fetchone('SELECT * FROM cart WHERE id = ?', [999])
    assert result is None

# edge_case - commit - Test committing without any changes
def test_commit_no_changes(mock_db_connection):
    mock_db_connection.commit()
    mock_db_connection.connection.commit.assert_called_once()

# edge_case - close - Test closing an already closed connection
def test_close_already_closed_db(mock_db_connection):
    mock_db_connection.close()
    mock_db_connection.close()
    assert mock_db_connection.connection is None

# edge_case - add_item_to_cart_db - Test adding an item with invalid parameters
def test_add_item_invalid_params(mock_db_connection):
    with pytest.raises(sqlite3.Error):
        mock_db_connection.add_item_to_cart_db('INSERT INTO cart (item) VALUES (?)', [None])

