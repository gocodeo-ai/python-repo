import pytest
from unittest import mock
import sqlite3
from shopping_cart.database import DatabaseConnection, add_item_to_cart_db

@pytest.fixture
def mock_database_connection():
    with mock.patch('shopping_cart.database.sqlite3.connect') as mock_connect:
        mock_conn = mock.Mock()
        mock_connect.return_value = mock_conn
        
        db_connection = DatabaseConnection('valid_path.db')
        db_connection.connect()
        
        yield db_connection, mock_conn

@pytest.fixture
def mock_cursor(mock_database_connection):
    db_connection, mock_conn = mock_database_connection
    mock_cursor = mock.Mock()
    mock_conn.cursor.return_value = mock_cursor
    
    yield mock_cursor

@pytest.fixture
def mock_execute(mock_cursor):
    with mock.patch.object(mock_cursor, 'execute') as mock_execute:
        yield mock_execute

@pytest.fixture
def mock_fetchone(mock_cursor):
    with mock.patch.object(mock_cursor, 'fetchone') as mock_fetchone:
        yield mock_fetchone

@pytest.fixture
def mock_fetchall(mock_cursor):
    with mock.patch.object(mock_cursor, 'fetchall') as mock_fetchall:
        yield mock_fetchall

@pytest.fixture
def mock_commit(mock_database_connection):
    db_connection, mock_conn = mock_database_connection
    with mock.patch.object(mock_conn, 'commit') as mock_commit:
        yield mock_commit

@pytest.fixture
def mock_close(mock_database_connection):
    db_connection, mock_conn = mock_database_connection
    with mock.patch.object(mock_conn, 'close') as mock_close:
        yield mock_close

@pytest.fixture
def mock_add_item_to_cart_db(mock_database_connection):
    with mock.patch('shopping_cart.database.database_connection') as mock_db_conn:
        mock_db_conn.connect.return_value = None
        mock_db_conn.execute.return_value = None
        mock_db_conn.commit.return_value = None
        mock_db_conn.close.return_value = None
        
        yield mock_db_conn

# happy_path - test_init_with_valid_path - Test that the database connection is established successfully with a valid path
def test_init_with_valid_path():
    db_connection = DatabaseConnection('valid_path.db')
    assert db_connection.connection is None
    assert db_connection.db_path == 'valid_path.db'

# happy_path - test_connect_opens_connection - Test that the connection is opened successfully
def test_connect_opens_connection(mock_database_connection):
    db_connection, mock_conn = mock_database_connection
    db_connection.connect()
    assert db_connection.connection is not None
    mock_conn.cursor.assert_called_once()

# happy_path - test_execute_query_without_params - Test that a query is executed without parameters
def test_execute_query_without_params(mock_execute):
    db_connection = DatabaseConnection('valid_path.db')
    db_connection.connect()
    query = 'CREATE TABLE test (id INTEGER)'
    db_connection.execute(query)
    mock_execute.assert_called_once_with(query, [])

# happy_path - test_fetchone_retrieves_single_row - Test that fetchone retrieves a single row
def test_fetchone_retrieves_single_row(mock_fetchone):
    mock_fetchone.return_value = {'id': 1}
    db_connection = DatabaseConnection('valid_path.db')
    db_connection.connect()
    result = db_connection.fetchone('SELECT * FROM test WHERE id=1')
    assert result == {'id': 1}

# happy_path - test_fetchall_retrieves_all_rows - Test that fetchall retrieves all rows
def test_fetchall_retrieves_all_rows(mock_fetchall):
    mock_fetchall.return_value = [{'id': 1}, {'id': 2}]
    db_connection = DatabaseConnection('valid_path.db')
    db_connection.connect()
    results = db_connection.fetchall('SELECT * FROM test')
    assert results == [{'id': 1}, {'id': 2}]

# happy_path - test_commit_saves_changes - Test that commit saves changes to the database
def test_commit_saves_changes(mock_commit):
    db_connection = DatabaseConnection('valid_path.db')
    db_connection.connect()
    db_connection.commit()
    mock_commit.assert_called_once()

# happy_path - test_close_connection - Test that the connection is closed successfully
def test_close_connection(mock_close):
    db_connection = DatabaseConnection('valid_path.db')
    db_connection.connect()
    db_connection.close()
    mock_close.assert_called_once()
    assert db_connection.connection is None

# happy_path - test_add_item_to_cart_db - Test that an item is added to the cart database
def test_add_item_to_cart_db(mock_add_item_to_cart_db):
    query = 'INSERT INTO cart (item) VALUES (?)'
    params = ['apple']
    add_item_to_cart_db(query, params)
    mock_add_item_to_cart_db.connect.assert_called_once()
    mock_add_item_to_cart_db.execute.assert_called_once_with(query, params)
    mock_add_item_to_cart_db.commit.assert_called_once()
    mock_add_item_to_cart_db.close.assert_called_once()

# edge_case - test_init_with_invalid_path - Test that the database connection fails with an invalid path
def test_init_with_invalid_path():
    with pytest.raises(sqlite3.OperationalError):
        DatabaseConnection('invalid_path.db').connect()

# edge_case - test_execute_invalid_sql - Test that execute raises an error for invalid SQL
def test_execute_invalid_sql(mock_execute):
    mock_execute.side_effect = sqlite3.OperationalError
    db_connection = DatabaseConnection('valid_path.db')
    db_connection.connect()
    with pytest.raises(sqlite3.OperationalError):
        db_connection.execute('INVALID SQL')

# edge_case - test_fetchone_no_matching_rows - Test that fetchone returns None for no matching rows
def test_fetchone_no_matching_rows(mock_fetchone):
    mock_fetchone.return_value = None
    db_connection = DatabaseConnection('valid_path.db')
    db_connection.connect()
    result = db_connection.fetchone('SELECT * FROM test WHERE id=999')
    assert result is None

# edge_case - test_fetchall_no_rows - Test that fetchall returns an empty list for no rows
def test_fetchall_no_rows(mock_fetchall):
    mock_fetchall.return_value = []
    db_connection = DatabaseConnection('valid_path.db')
    db_connection.connect()
    results = db_connection.fetchall('SELECT * FROM test WHERE id<0')
    assert results == []

# edge_case - test_commit_no_changes - Test that commit does nothing when no changes are made
def test_commit_no_changes(mock_commit):
    db_connection = DatabaseConnection('valid_path.db')
    db_connection.connect()
    db_connection.commit()
    mock_commit.assert_called_once()

# edge_case - test_close_already_closed_connection - Test that closing an already closed connection does not raise an error
def test_close_already_closed_connection(mock_close):
    db_connection = DatabaseConnection('valid_path.db')
    db_connection.connect()
    db_connection.close()
    db_connection.close()
    mock_close.assert_called_once()
    assert db_connection.connection is None

