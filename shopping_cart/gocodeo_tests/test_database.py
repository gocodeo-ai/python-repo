import pytest
from unittest import mock
from shopping_cart.database import DatabaseConnection, add_item_to_cart_db

@pytest.fixture
def mock_database_connection():
    with mock.patch('shopping_cart.database.sqlite3.connect') as mock_connect:
        mock_connection = mock.Mock()
        mock_connect.return_value = mock_connection
        
        mock_connection.cursor.return_value = mock.Mock()
        mock_cursor = mock_connection.cursor.return_value
        
        mock_cursor.execute = mock.Mock()
        mock_cursor.fetchone = mock.Mock(return_value=None)
        mock_cursor.fetchall = mock.Mock(return_value=[])
        
        mock_connection.commit = mock.Mock()
        mock_connection.close = mock.Mock()
        
        db_connection = DatabaseConnection('valid_path.db')
        db_connection.connection = mock_connection
        
        yield db_connection

        db_connection.close()

@pytest.fixture
def mock_add_item_to_cart_db(mock_database_connection):
    with mock.patch('shopping_cart.database.database_connection', mock_database_connection):
        yield

# happy path - connect - Test that connection to the database is established successfully.
def test_connect_success(mock_database_connection):
    assert mock_database_connection.connection is not None


# happy path - execute - Test that a query is executed without parameters successfully.
def test_execute_query_without_params(mock_database_connection):
    query = 'CREATE TABLE test (id INTEGER)'
    mock_database_connection.execute(query)
    mock_database_connection.connection.cursor.return_value.execute.assert_called_once_with(query, [])


# happy path - fetchone - Test that fetchone returns a single row from the database.
def test_fetchone_single_row(mock_database_connection):
    query = 'SELECT * FROM test WHERE id = 1'
    mock_database_connection.connection.cursor.return_value.fetchone.return_value = ('row',)
    result = mock_database_connection.fetchone(query)
    assert result == ('row',)


# happy path - fetchall - Test that fetchall returns all rows from the database.
def test_fetchall_all_rows(mock_database_connection):
    query = 'SELECT * FROM test'
    mock_database_connection.connection.cursor.return_value.fetchall.return_value = [('row1',), ('row2',)]
    results = mock_database_connection.fetchall(query)
    assert results == [('row1',), ('row2',)]


# happy path - commit - Test that commit saves changes to the database.
def test_commit_changes(mock_database_connection):
    mock_database_connection.commit()
    mock_database_connection.connection.commit.assert_called_once()


# happy path - close - Test that close disconnects the database connection.
def test_close_connection(mock_database_connection):
    mock_database_connection.close()
    mock_database_connection.connection.close.assert_called_once()


# edge case - connect - Test that connect raises an error when the database path is invalid.
def test_connect_invalid_path():
    with mock.patch('shopping_cart.database.sqlite3.connect', side_effect=sqlite3.OperationalError):
        db_connection = DatabaseConnection('invalid_path.db')
        with pytest.raises(sqlite3.OperationalError):
            db_connection.connect()


# edge case - execute - Test that execute raises an error for a malformed query.
def test_execute_malformed_query(mock_database_connection):
    query = 'MALFORMED QUERY'
    mock_database_connection.connection.cursor.return_value.execute.side_effect = sqlite3.OperationalError
    with pytest.raises(sqlite3.OperationalError):
        mock_database_connection.execute(query)


# edge case - fetchone - Test that fetchone returns None when no rows match the query.
def test_fetchone_no_match(mock_database_connection):
    query = 'SELECT * FROM test WHERE id = 999'
    result = mock_database_connection.fetchone(query)
    assert result is None


# edge case - fetchall - Test that fetchall returns an empty list when no rows match the query.
def test_fetchall_no_match(mock_database_connection):
    query = 'SELECT * FROM test WHERE id = 999'
    results = mock_database_connection.fetchall(query)
    assert results == []


# edge case - commit - Test that commit raises an error when there is no active transaction.
def test_commit_no_transaction(mock_database_connection):
    mock_database_connection.connection.commit.side_effect = sqlite3.OperationalError
    with pytest.raises(sqlite3.OperationalError):
        mock_database_connection.commit()


# edge case - close - Test that close raises no error when called multiple times.
def test_close_multiple_times(mock_database_connection):
    mock_database_connection.close()
    mock_database_connection.close()
    mock_database_connection.connection.close.assert_called_once()


