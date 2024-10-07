import os
import pytest
from unittest import mock
from shopping_cart.database import DatabaseConnection, add_item_to_cart_db

@pytest.fixture
def mock_database_connection():
    with mock.patch('shopping_cart.database.sqlite3.connect') as mock_connect:
        mock_connection = mock.Mock()
        mock_connect.return_value = mock_connection
        
        with mock.patch.object(DatabaseConnection, 'connect', return_value=None) as mock_connect_method, \
             mock.patch.object(DatabaseConnection, 'execute', return_value=None) as mock_execute_method, \
             mock.patch.object(DatabaseConnection, 'fetchone', return_value=None) as mock_fetchone_method, \
             mock.patch.object(DatabaseConnection, 'fetchall', return_value=None) as mock_fetchall_method, \
             mock.patch.object(DatabaseConnection, 'commit', return_value=None) as mock_commit_method, \
             mock.patch.object(DatabaseConnection, 'close', return_value=None) as mock_close_method:
            
            db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "shopping_cart.db")
            database_connection = DatabaseConnection(db_path)
            yield database_connection, mock_connect, mock_connection

@pytest.fixture
def mock_add_item_to_cart_db(mock_database_connection):
    database_connection, mock_connect, mock_connection = mock_database_connection
    with mock.patch('shopping_cart.database.database_connection', database_connection):
        yield database_connection

