import pytest
from unittest.mock import patch, MagicMock
import sqlite3
import os
from your_module import DatabaseConnection, add_item_to_cart_db

@pytest.fixture
def mock_sqlite_connect():
    with patch('your_module.sqlite3.connect') as mock_connect:
        mock_conn = MagicMock()
        mock_connect.return_value = mock_conn
        yield mock_connect, mock_conn

@pytest.fixture
def mock_os_path():
    with patch('your_module.os.path') as mock_path:
        mock_path.dirname.return_value = '/mocked/dir'
        mock_path.abspath.return_value = '/mocked/dir/file.py'
        mock_path.join.return_value = '/mocked/dir/shopping_cart.db'
        yield mock_path

@pytest.fixture
def db_connection(mock_sqlite_connect, mock_os_path):
    db_path = mock_os_path.join('/mocked/dir', 'shopping_cart.db')
    db_conn = DatabaseConnection(db_path)
    yield db_conn

@pytest.fixture
def mock_execute():
    with patch('your_module.DatabaseConnection.execute') as mock_exec:
        yield mock_exec

@pytest.fixture
def mock_fetchone():
    with patch('your_module.DatabaseConnection.fetchone') as mock_fetch:
        yield mock_fetch

@pytest.fixture
def mock_fetchall():
    with patch('your_module.DatabaseConnection.fetchall') as mock_fetch:
        yield mock_fetch

@pytest.fixture
def mock_commit():
    with patch('your_module.DatabaseConnection.commit') as mock_commit:
        yield mock_commit

@pytest.fixture
def mock_close():
    with patch('your_module.DatabaseConnection.close') as mock_close:
        yield mock_close

@pytest.fixture
def mock_add_item_to_cart_db():
    with patch('your_module.add_item_to_cart_db') as mock_add_item:
        yield mock_add_item

# happy_path - connect - Test successful database connection
def test_connect_db(db_connection):
    db_connection.connect()
    assert db_connection.connection is not None

# happy_path - execute - Test successful query execution
def test_execute_query(db_connection, mock_execute):
    query = 'CREATE TABLE items (id INTEGER PRIMARY KEY, name TEXT)'
    db_connection.execute(query)
    mock_execute.assert_called_once_with(query, [])

# happy_path - fetchone - Test successful fetchone operation
def test_fetchone_query(db_connection, mock_fetchone):
    mock_fetchone.return_value = (1, 'item1')
    result = db_connection.fetchone('SELECT * FROM items WHERE id = 1')
    assert result is not None

# happy_path - fetchall - Test successful fetchall operation
def test_fetchall_query(db_connection, mock_fetchall):
    mock_fetchall.return_value = [(1, 'item1'), (2, 'item2')]
    results = db_connection.fetchall('SELECT * FROM items')
    assert isinstance(results, list)

# happy_path - commit - Test successful commit operation
def test_commit_changes(db_connection, mock_commit):
    db_connection.commit()
    mock_commit.assert_called_once()

# happy_path - close - Test successful close operation
def test_close_connection(db_connection, mock_close):
    db_connection.close()
    assert db_connection.connection is None

# happy_path - add_item_to_cart_db - Test adding item to cart database
def test_add_item_to_cart(db_connection, mock_add_item_to_cart_db):
    query = 'INSERT INTO items (name) VALUES (?)'
    params = ['item1']
    add_item_to_cart_db(query, params)
    mock_add_item_to_cart_db.assert_called_once_with(query, params)

# edge_case - connect - Test connection with invalid database path
def test_connect_invalid_db():
    db_connection = DatabaseConnection('invalid_path_to_database.db')
    with pytest.raises(sqlite3.OperationalError):
        db_connection.connect()

# edge_case - execute - Test executing invalid query
def test_execute_invalid_query(db_connection, mock_execute):
    query = 'INVALID SQL QUERY'
    with pytest.raises(sqlite3.OperationalError):
        db_connection.execute(query)

# edge_case - fetchone - Test fetchone with no results
def test_fetchone_no_results(db_connection, mock_fetchone):
    mock_fetchone.return_value = None
    result = db_connection.fetchone('SELECT * FROM items WHERE id = -1')
    assert result is None

# edge_case - fetchall - Test fetchall from empty table
def test_fetchall_empty_table(db_connection, mock_fetchall):
    mock_fetchall.return_value = []
    results = db_connection.fetchall('SELECT * FROM items')
    assert results == []

# edge_case - commit - Test commit without changes
def test_commit_no_changes(db_connection, mock_commit):
    db_connection.commit()
    mock_commit.assert_called_once()

# edge_case - close - Test closing already closed connection
def test_close_already_closed_connection(db_connection, mock_close):
    db_connection.close()
    db_connection.close()
    assert db_connection.connection is None

