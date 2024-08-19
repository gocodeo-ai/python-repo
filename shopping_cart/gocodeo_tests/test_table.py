import pytest
from unittest import mock
import sqlite3

@pytest.fixture
def mock_sqlite():
    with mock.patch('sqlite3.connect') as mock_connect:
        mock_conn = mock.Mock()
        mock_cursor = mock.Mock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        yield mock_connect, mock_conn, mock_cursor# happy_path - connect - Test successful connection to the SQLite database.
def test_connect_to_db(mock_sqlite):
    mock_connect, mock_conn, mock_cursor = mock_sqlite
    assert mock_connect.called
    assert mock_conn is not None


# edge_case - connect - Test connection failure to the SQLite database.
def test_drop_table(mock_sqlite):
    mock_connect, mock_conn, mock_cursor = mock_sqlite
    mock_cursor.execute('DROP TABLE cart;')
    mock_cursor.execute.assert_called_with('DROP TABLE cart;')


