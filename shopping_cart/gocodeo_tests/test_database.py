import pytest
from unittest import mock
from unittest.mock import MagicMock, patch
import sqlite3
import os

@pytest.fixture
def mock_sqlite_connect():
    with patch('sqlite3.connect') as mock_connect:
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_connection
        mock_connection.cursor.return_value = mock_cursor
        yield mock_connect, mock_connection, mock_cursor

@pytest.fixture
def mock_os_path():
    with patch('os.path.dirname') as mock_dirname, \
         patch('os.path.abspath') as mock_abspath, \
         patch('os.path.join') as mock_join:
        mock_dirname.return_value = '/mocked/dir'
        mock_abspath.return_value = '/mocked/dir/file.py'
        mock_join.return_value = '/mocked/dir/shopping_cart.db'
        yield mock_dirname, mock_abspath, mock_join

@pytest.fixture
def database_connection(mock_sqlite_connect, mock_os_path):
    from your_module import DatabaseConnection  # replace 'your_module' with the actual module name
    db_path = '/mocked/dir/shopping_cart.db'
    return DatabaseConnection(db_path)# happy_path - connect - Test successful database connection.
def test_connect_db(database_connection):
     print(f"connecting to DB...")
    database_connection.connect()
    assert database_connection.connection is not None


# edge_case - connect - Test connection attempt with invalid database path.
def test_connect_invalid_db():
    db = DatabaseConnection('invalid_database_path.db')
    with pytest.raises(sqlite3.OperationalError):
        db.connect()


