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
        
        # Mock methods for DatabaseConnection
        mock_cursor.execute = mock.Mock()
        mock_cursor.fetchone = mock.Mock(return_value=None)
        mock_cursor.fetchall = mock.Mock(return_value=[])
        mock_connection.commit = mock.Mock()
        mock_connection.close = mock.Mock()
        
        db_connection = DatabaseConnection('shopping_cart.db')
        db_connection.connection = mock_connection
        
        yield db_connection

        db_connection.close()

@pytest.fixture
def mock_add_item_to_cart_db(mock_database_connection):
    with mock.patch('shopping_cart.database.database_connection', mock_database_connection):
        yield

# happy path - connect - Test that the connection to the database is established successfully.
def test_connect_success(mock_database_connection):
    assert mock_database_connection.connection is not None
    mock_database_connection.connect()
    mock_database_connection.connection.cursor.assert_called_once()


# happy path - execute - Test that a query is executed successfully without parameters.
def test_execute_query_no_params(mock_database_connection):
    query = 'CREATE TABLE test (id INTEGER)'
    mock_database_connection.execute(query)
    mock_database_connection.connection.cursor().execute.assert_called_once_with(query, [])


# happy path - fetchone - Test that a single row is fetched successfully.
def test_fetchone_success(mock_database_connection):
    query = 'SELECT * FROM test WHERE id = ?'
    params = [1]
    result = mock_database_connection.fetchone(query, params)
    mock_database_connection.connection.cursor().execute.assert_called_once_with(query, params)
    assert result is None


# happy path - fetchall - Test that multiple rows are fetched successfully.
def test_fetchall_success(mock_database_connection):
    query = 'SELECT * FROM test'
    results = mock_database_connection.fetchall(query)
    mock_database_connection.connection.cursor().execute.assert_called_once_with(query, [])
    assert results == []


# happy path - commit - Test that changes are committed successfully.
def test_commit_success(mock_database_connection):
    mock_database_connection.commit()
    mock_database_connection.connection.commit.assert_called_once()


# happy path - close - Test that the connection is closed successfully.
def test_close_success(mock_database_connection):
    mock_database_connection.close()
    mock_database_connection.connection.close.assert_called_once()


# edge case - connect - Test that an exception is raised when trying to connect to a non-existent database.
def test_connect_non_existent_db():
    with mock.patch('shopping_cart.database.sqlite3.connect', side_effect=sqlite3.OperationalError):
        db_connection = DatabaseConnection('non_existent.db')
        with pytest.raises(sqlite3.OperationalError):
            db_connection.connect()


# edge case - execute - Test that an exception is raised when executing an invalid query.
def test_execute_invalid_query(mock_database_connection):
    query = 'INVALID SQL'
    mock_database_connection.connection.cursor().execute.side_effect = sqlite3.OperationalError
    with pytest.raises(sqlite3.OperationalError):
        mock_database_connection.execute(query)


# edge case - fetchone - Test that fetchone returns None when no rows match the query.
def test_fetchone_no_match(mock_database_connection):
    query = 'SELECT * FROM test WHERE id = ?'
    params = [999]
    result = mock_database_connection.fetchone(query, params)
    mock_database_connection.connection.cursor().execute.assert_called_once_with(query, params)
    assert result is None


# edge case - fetchall - Test that fetchall returns an empty list when no rows match the query.
def test_fetchall_no_match(mock_database_connection):
    query = 'SELECT * FROM test WHERE id > ?'
    params = [999]
    results = mock_database_connection.fetchall(query, params)
    mock_database_connection.connection.cursor().execute.assert_called_once_with(query, params)
    assert results == []


# edge case - close - Test that closing an already closed connection does not raise an exception.
def test_close_already_closed(mock_database_connection):
    mock_database_connection.close()
    mock_database_connection.close()  # Close again
    mock_database_connection.connection.close.assert_called_once()


