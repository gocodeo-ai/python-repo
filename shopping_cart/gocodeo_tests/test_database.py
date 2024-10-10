import pytest
from unittest import mock
from shopping_cart.database import DatabaseConnection, add_item_to_cart_db

@pytest.fixture
def mock_database_connection():
    with mock.patch('shopping_cart.database.sqlite3.connect') as mock_connect:
        mock_connection = mock.Mock()
        mock_connect.return_value = mock_connection
        
        # Mock the methods of the connection object
        mock_cursor = mock.Mock()
        mock_connection.cursor.return_value = mock_cursor
        
        yield {
            'connection': mock_connection,
            'cursor': mock_cursor,
            'mock_connect': mock_connect
        }

@pytest.fixture
def db_connection(mock_database_connection):
    db = DatabaseConnection("valid_db_path.db")
    db.connection = mock_database_connection['connection']
    return db

@pytest.fixture
def setup_database(db_connection):
    db_connection.connect()
    db_connection.execute("CREATE TABLE IF NOT EXISTS test_table (id INTEGER PRIMARY KEY)")
    db_connection.commit()
    yield db_connection
    db_connection.close()

@pytest.fixture
def mock_add_item_to_cart_db(mock_database_connection):
    with mock.patch('shopping_cart.database.database_connection', mock_database_connection['connection']):
        yield

# happy path - connect - Test that the database connection is established successfully
def test_connect_success(mock_database_connection):
    db = DatabaseConnection('valid_db_path.db')
    db.connect()
    mock_database_connection['mock_connect'].assert_called_once_with('valid_db_path.db')
    assert db.connection is not None


# happy path - execute - Test that a query is executed successfully without parameters
def test_execute_no_params(db_connection):
    db_connection.execute('CREATE TABLE IF NOT EXISTS test_table (id INTEGER PRIMARY KEY)')
    db_connection.connection.cursor().execute.assert_called_once_with('CREATE TABLE IF NOT EXISTS test_table (id INTEGER PRIMARY KEY)', [])


# happy path - execute - Test that a query is executed successfully with parameters
def test_execute_with_params(db_connection):
    db_connection.execute('INSERT INTO test_table (id) VALUES (?)', [1])
    db_connection.connection.cursor().execute.assert_called_once_with('INSERT INTO test_table (id) VALUES (?)', [1])


# happy path - fetchone - Test that fetchone returns the correct single result
def test_fetchone_single_result(db_connection):
    db_connection.connection.cursor().execute.return_value.fetchone.return_value = (1,)
    result = db_connection.fetchone('SELECT id FROM test_table WHERE id = 1')
    db_connection.connection.cursor().execute.assert_called_once_with('SELECT id FROM test_table WHERE id = 1', [])
    assert result == (1,)


# happy path - fetchall - Test that fetchall returns all results
def test_fetchall_multiple_results(db_connection):
    db_connection.connection.cursor().execute.return_value.fetchall.return_value = [(1,), (2,), (3,)]
    results = db_connection.fetchall('SELECT id FROM test_table')
    db_connection.connection.cursor().execute.assert_called_once_with('SELECT id FROM test_table', [])
    assert results == [(1,), (2,), (3,)]


# edge case - connect - Test that connecting to a non-existent database path raises an error
def test_connect_invalid_path():
    db = DatabaseConnection('non_existent_path.db')
    with pytest.raises(sqlite3.OperationalError):
        db.connect()


# edge case - execute - Test that executing a query without a connection raises an error
def test_execute_no_connection():
    db = DatabaseConnection('valid_db_path.db')
    with pytest.raises(sqlite3.ProgrammingError):
        db.execute('SELECT * FROM test_table')


# edge case - fetchone - Test that fetchone with no results returns None
def test_fetchone_no_results(db_connection):
    db_connection.connection.cursor().execute.return_value.fetchone.return_value = None
    result = db_connection.fetchone('SELECT id FROM test_table WHERE id = 999')
    db_connection.connection.cursor().execute.assert_called_once_with('SELECT id FROM test_table WHERE id = 999', [])
    assert result is None


# edge case - fetchall - Test that fetchall with no results returns an empty list
def test_fetchall_no_results(db_connection):
    db_connection.connection.cursor().execute.return_value.fetchall.return_value = []
    results = db_connection.fetchall('SELECT id FROM test_table WHERE id = 999')
    db_connection.connection.cursor().execute.assert_called_once_with('SELECT id FROM test_table WHERE id = 999', [])
    assert results == []


# edge case - close - Test that closing an already closed connection does not raise an error
def test_close_already_closed(db_connection):
    db_connection.close()
    db_connection.close()
    assert db_connection.connection is None


