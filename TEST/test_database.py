import sqlite3
import pytest
from unittest.mock import MagicMock, patch
import json

class DatabaseConnection:
    def __init__(self, db_path):
        self.connection = None
        self.db_path = db_path

    def connect(self):
        self.connection = sqlite3.connect(self.db_path)

    def execute(self, query, params=None):
        if params is None:
            params = []
        cursor = self.connection.cursor()
        cursor.execute(query, params)

    def fetchone(self, query, params=None):
        if params is None:
            params = []
        cursor = self.connection.cursor()
        cursor.execute(query, params)
        result = cursor.fetchone()
        return result

    def fetchall(self, query, params=None):
        if params is None:
            params = []
        cursor = self.connection.cursor()
        cursor.execute(query, params)
        results = cursor.fetchall()
        return results

    def commit(self):
        self.connection.commit()

    def close(self):
        if self.connection:
            self.connection.close()
            self.connection = None

database_connection = DatabaseConnection("shopping_cart.db")

def add_item_to_cart_db(query, params=None):
    if params is None:
        params = []
    database_connection.connect()
    database_connection.execute(query, params)
    database_connection.commit()
    database_connection.close()

@pytest.fixture
def mock_connection():
    mock_connection = MagicMock(spec=sqlite3.Connection)
    mock_cursor = MagicMock(spec=sqlite3.Cursor)
    mock_connection.cursor.return_value = mock_cursor
    return mock_connection

@patch('sqlite3.connect', autospec=True)
@pytest.mark.parametrize("test_data", json.load(open('test_data_database.json'))["test_data_add_item"])
def test_add_item_to_cart_db(mock_connect, mock_connection, test_data):
    mock_connect.return_value = mock_connection
    query = test_data["query"]
    params = test_data.get("params") 
    add_item_to_cart_db(query, params)
    mock_connect.assert_called_once_with("shopping_cart.db")
    mock_connection.cursor.assert_called_once()
    mock_connection.cursor().execute.assert_called_once_with(query, params)
    mock_connection.commit.assert_called_once()
    mock_connection.close.assert_called_once()