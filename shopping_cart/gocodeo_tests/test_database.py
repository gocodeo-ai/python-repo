import pytest
from unittest import mock
from shopping_cart.database import DatabaseConnection, add_item_to_cart_db

@pytest.fixture
def db_connection_mock():
    with mock.patch('sqlite3.connect') as mock_connect:
        mock_connection = mock.Mock()
        mock_connect.return_value = mock_connection
        
        mock_cursor = mock.Mock()
        mock_connection.cursor.return_value = mock_cursor
        
        yield mock_connection, mock_cursor

@pytest.fixture
def setup_database(db_connection_mock):
    mock_connection, mock_cursor = db_connection_mock
    
    # Mocking the execute method
    mock_cursor.execute = mock.Mock()
    
    # Mocking the fetchone method
    mock_cursor.fetchone = mock.Mock(return_value=(1,))
    
    # Mocking the fetchall method
    mock_cursor.fetchall = mock.Mock(return_value=[(1,), (2,), (3,)])
    
    # Mocking the commit method
    mock_connection.commit = mock.Mock()
    
    yield mock_connection, mock_cursor

@pytest.fixture
def database_connection():
    with mock.patch('shopping_cart.database.DatabaseConnection.__init__', return_value=None):
        db = DatabaseConnection('test_db_path.db')
        db.connect = mock.Mock()
        db.execute = mock.Mock()
        db.fetchone = mock.Mock()
        db.fetchall = mock.Mock()
        db.commit = mock.Mock()
        db.close = mock.Mock()
        yield db

# happy path - connect - Test that the database connection is established correctly
def test_connect_success(database_connection):
    database_connection.connect()
    database_connection.connect.assert_called_once()
    assert database_connection.connection is not None


# happy path - execute - Test that a query executes successfully without parameters
def test_execute_without_params(setup_database):
    mock_connection, mock_cursor = setup_database
    query = 'CREATE TABLE test (id INTEGER)'
    database_connection.execute(query)
    mock_cursor.execute.assert_called_once_with(query, [])


# happy path - execute - Test that a query executes successfully with parameters
def test_execute_with_params(setup_database):
    mock_connection, mock_cursor = setup_database
    query = 'INSERT INTO test (id) VALUES (?)'
    params = [1]
    database_connection.execute(query, params)
    mock_cursor.execute.assert_called_once_with(query, params)


# happy path - fetchone - Test that fetchone retrieves a single row correctly
def test_fetchone_success(setup_database):
    mock_connection, mock_cursor = setup_database
    query = 'SELECT id FROM test WHERE id = ?'
    params = [1]
    result = database_connection.fetchone(query, params)
    mock_cursor.execute.assert_called_once_with(query, params)
    assert result == (1,)


# happy path - fetchall - Test that fetchall retrieves all rows correctly
def test_fetchall_success(setup_database):
    mock_connection, mock_cursor = setup_database
    query = 'SELECT id FROM test'
    results = database_connection.fetchall(query)
    mock_cursor.execute.assert_called_once_with(query, [])
    assert results == [(1,), (2,), (3,)]


# edge case - connect - Test that connect handles invalid database path
def test_connect_invalid_path():
    with mock.patch('sqlite3.connect', side_effect=sqlite3.OperationalError):
        with pytest.raises(sqlite3.OperationalError):
            db = DatabaseConnection('invalid_path.db')
            db.connect()


# edge case - execute - Test that execute handles malformed SQL query
def test_execute_malformed_query(setup_database):
    mock_connection, mock_cursor = setup_database
    query = 'MALFORMED SQL'
    mock_cursor.execute.side_effect = sqlite3.OperationalError
    with pytest.raises(sqlite3.OperationalError):
        database_connection.execute(query)


# edge case - fetchone - Test that fetchone handles query with no results
def test_fetchone_no_results(setup_database):
    mock_connection, mock_cursor = setup_database
    query = 'SELECT id FROM test WHERE id = ?'
    params = [999]
    mock_cursor.fetchone.return_value = None
    result = database_connection.fetchone(query, params)
    mock_cursor.execute.assert_called_once_with(query, params)
    assert result is None


# edge case - fetchall - Test that fetchall handles empty table
def test_fetchall_empty_table(setup_database):
    mock_connection, mock_cursor = setup_database
    query = 'SELECT id FROM empty_table'
    mock_cursor.fetchall.return_value = []
    results = database_connection.fetchall(query)
    mock_cursor.execute.assert_called_once_with(query, [])
    assert results == []


# edge case - close - Test that close handles closing an already closed connection
def test_close_already_closed(database_connection):
    database_connection.close()
    database_connection.close()
    database_connection.close.assert_called()
    assert database_connection.connection is None


