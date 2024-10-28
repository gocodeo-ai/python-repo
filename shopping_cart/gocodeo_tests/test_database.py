import pytest
from unittest import mock
from shopping_cart.database import DatabaseConnection, add_item_to_cart_db

@pytest.fixture
def mock_database_connection():
    with mock.patch('shopping_cart.database.sqlite3.connect') as mock_connect:
        mock_connection = mock.Mock()
        mock_connect.return_value = mock_connection
        
        mock_cursor = mock.Mock()
        mock_connection.cursor.return_value = mock_cursor
        
        mock_cursor.fetchone.return_value = None
        mock_cursor.fetchall.return_value = []
        
        db_connection = DatabaseConnection('valid/path/to/db')
        db_connection.connection = mock_connection
        
        yield db_connection

@pytest.fixture
def mock_add_item_to_cart_db(mock_database_connection):
    with mock.patch('shopping_cart.database.database_connection', mock_database_connection):
        yield

# happy path - __init__ - Test that DatabaseConnection can be initialized with a valid database path
def test_init_with_valid_db_path():
    db_path = 'valid/path/to/db'
    db_connection = DatabaseConnection(db_path)
    assert db_connection.connection is None
    assert db_connection.db_path == db_path



# happy path - connect - Test that DatabaseConnection can connect to a database
def test_connect_to_database(mock_database_connection):
    mock_database_connection.connect()
    mock_database_connection.connection.cursor.assert_called_once()



# happy path - execute - Test that execute runs a valid SQL query without parameters
def test_execute_valid_query_no_params(mock_database_connection):
    query = 'CREATE TABLE test (id INTEGER)'
    mock_database_connection.execute(query)
    mock_database_connection.connection.cursor().execute.assert_called_once_with(query, [])



# happy path - fetchone - Test that fetchone retrieves a single row from the database
def test_fetchone_retrieves_single_row(mock_database_connection):
    query = 'SELECT * FROM test WHERE id=1'
    result = mock_database_connection.fetchone(query)
    mock_database_connection.connection.cursor().execute.assert_called_once_with(query, [])
    assert result is None



# happy path - fetchall - Test that fetchall retrieves all rows from the database
def test_fetchall_retrieves_all_rows(mock_database_connection):
    query = 'SELECT * FROM test'
    results = mock_database_connection.fetchall(query)
    mock_database_connection.connection.cursor().execute.assert_called_once_with(query, [])
    assert results == []



# happy path - commit - Test that commit saves changes to the database
def test_commit_saves_changes(mock_database_connection):
    mock_database_connection.commit()
    mock_database_connection.connection.commit.assert_called_once()



# happy path - close - Test that close closes the database connection
def test_close_connection(mock_database_connection):
    mock_database_connection.close()
    mock_database_connection.connection.close.assert_called_once()
    assert mock_database_connection.connection is None



# happy path - add_item_to_cart_db - Test that add_item_to_cart_db adds an item to the cart database
def test_add_item_to_cart_db(mock_add_item_to_cart_db):
    query = 'INSERT INTO cart (item) VALUES (?)'
    params = ['apple']
    add_item_to_cart_db(query, params)
    mock_add_item_to_cart_db.execute.assert_called_once_with(query, params)
    mock_add_item_to_cart_db.connection.commit.assert_called_once()
    mock_add_item_to_cart_db.connection.close.assert_called_once()



# edge case - __init__ - Test that DatabaseConnection raises an error with an invalid database path
def test_init_with_invalid_db_path():
    db_path = 'invalid/path/to/db'
    with pytest.raises(sqlite3.OperationalError):
        DatabaseConnection(db_path).connect()



# edge case - execute - Test that execute raises an error with an invalid SQL query
def test_execute_invalid_query(mock_database_connection):
    query = 'INVALID SQL'
    with pytest.raises(sqlite3.OperationalError):
        mock_database_connection.execute(query)



# edge case - fetchone - Test that fetchone raises an error if not connected to a database
def test_fetchone_without_connection():
    db_connection = DatabaseConnection('valid/path/to/db')
    query = 'SELECT * FROM test'
    with pytest.raises(sqlite3.ProgrammingError):
        db_connection.fetchone(query)



# edge case - fetchall - Test that fetchall raises an error if not connected to a database
def test_fetchall_without_connection():
    db_connection = DatabaseConnection('valid/path/to/db')
    query = 'SELECT * FROM test'
    with pytest.raises(sqlite3.ProgrammingError):
        db_connection.fetchall(query)



# edge case - commit - Test that commit raises an error if not connected to a database
def test_commit_without_connection():
    db_connection = DatabaseConnection('valid/path/to/db')
    with pytest.raises(sqlite3.ProgrammingError):
        db_connection.commit()



# edge case - close - Test that close does nothing if already closed
def test_close_already_closed(mock_database_connection):
    mock_database_connection.close()
    mock_database_connection.close()  # Close again
    mock_database_connection.connection.close.assert_called_once()
    assert mock_database_connection.connection is None



