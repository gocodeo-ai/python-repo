import pytest
from unittest import mock
from shopping_cart.database import DatabaseConnection, add_item_to_cart_db

@pytest.fixture
def mock_database_connection():
    with mock.patch('shopping_cart.database.sqlite3.connect') as mock_connect, \
         mock.patch('shopping_cart.database.sqlite3.Connection') as mock_connection, \
         mock.patch.object(DatabaseConnection, '__init__', lambda self, db_path: None), \
         mock.patch.object(DatabaseConnection, 'connect', return_value=None), \
         mock.patch.object(DatabaseConnection, 'execute') as mock_execute, \
         mock.patch.object(DatabaseConnection, 'fetchone') as mock_fetchone, \
         mock.patch.object(DatabaseConnection, 'fetchall') as mock_fetchall, \
         mock.patch.object(DatabaseConnection, 'commit', return_value=None), \
         mock.patch.object(DatabaseConnection, 'close', return_value=None):
        
        instance = DatabaseConnection('mock_db_path')
        instance.connection = mock_connection
        mock_connect.return_value = mock_connection
        yield instance, mock_execute, mock_fetchone, mock_fetchall

@pytest.fixture
def mock_add_item_to_cart_db(mock_database_connection):
    instance, mock_execute, mock_commit, mock_close = mock_database_connection
    yield instance, mock_execute, mock_commit, mock_close

# happy path - connect - Test that connection is established with valid database path
def test_connect_valid_path(mock_database_connection):
    instance, _, _, _ = mock_database_connection
    instance.connect()
    assert instance.connection is not None


# happy path - execute - Test that execute runs a valid query without parameters
def test_execute_valid_query_no_params(mock_database_connection):
    instance, mock_execute, _, _ = mock_database_connection
    query = 'CREATE TABLE test (id INTEGER)'
    instance.execute(query)
    mock_execute.assert_called_once_with(query, [])


# happy path - fetchone - Test that fetchone retrieves one result
def test_fetchone_single_result(mock_database_connection):
    instance, _, mock_fetchone, _ = mock_database_connection
    query = 'SELECT * FROM test WHERE id=1'
    mock_fetchone.return_value = (1, 'item')
    result = instance.fetchone(query)
    assert result == (1, 'item')


# happy path - fetchall - Test that fetchall retrieves multiple results
def test_fetchall_multiple_results(mock_database_connection):
    instance, _, _, mock_fetchall = mock_database_connection
    query = 'SELECT * FROM test'
    mock_fetchall.return_value = [(1, 'item1'), (2, 'item2')]
    results = instance.fetchall(query)
    assert results == [(1, 'item1'), (2, 'item2')]


# happy path - commit - Test that commit saves changes to the database
def test_commit_changes(mock_database_connection):
    instance, _, _, _ = mock_database_connection
    instance.commit()
    instance.connection.commit.assert_called_once()


# happy path - close - Test that close closes the connection
def test_close_connection(mock_database_connection):
    instance, _, _, _ = mock_database_connection
    instance.close()
    instance.connection.close.assert_called_once()


# edge case - connect - Test that connect raises error with invalid path
def test_connect_invalid_path():
    with mock.patch('shopping_cart.database.sqlite3.connect', side_effect=sqlite3.OperationalError):
        instance = DatabaseConnection('invalid_path.db')
        with pytest.raises(sqlite3.OperationalError):
            instance.connect()


# edge case - execute - Test that execute raises error on invalid query
def test_execute_invalid_query(mock_database_connection):
    instance, mock_execute, _, _ = mock_database_connection
    mock_execute.side_effect = sqlite3.OperationalError
    with pytest.raises(sqlite3.OperationalError):
        instance.execute('INVALID QUERY')


# edge case - fetchone - Test that fetchone returns None when no result
def test_fetchone_no_result(mock_database_connection):
    instance, _, mock_fetchone, _ = mock_database_connection
    query = 'SELECT * FROM test WHERE id=999'
    mock_fetchone.return_value = None
    result = instance.fetchone(query)
    assert result is None


# edge case - fetchall - Test that fetchall returns empty list when no results
def test_fetchall_no_results(mock_database_connection):
    instance, _, _, mock_fetchall = mock_database_connection
    query = 'SELECT * FROM test WHERE id=999'
    mock_fetchall.return_value = []
    results = instance.fetchall(query)
    assert results == []


# edge case - close - Test that close does nothing if connection is already closed
def test_close_already_closed(mock_database_connection):
    instance, _, _, _ = mock_database_connection
    instance.connection = None
    instance.close()
    instance.connection.close.assert_not_called()


# edge case - commit - Test that commit raises error if connection is closed
def test_commit_closed_connection(mock_database_connection):
    instance, _, _, _ = mock_database_connection
    instance.connection = None
    with pytest.raises(sqlite3.ProgrammingError):
        instance.commit()


# edge case - execute - generate test cases on executing a query with incorrect parameters
def test_execute_incorrect_params(mock_database_connection):
    instance, mock_execute, _, _ = mock_database_connection
    query = 'SELECT * FROM test WHERE id=?'
    params = ['string_instead_of_integer']
    mock_execute.side_effect = sqlite3.ProgrammingError
    with pytest.raises(sqlite3.ProgrammingError):
        instance.execute(query, params)


# edge case - fetchone - generate test cases on fetchone with incorrect parameters
def test_fetchone_incorrect_params(mock_database_connection):
    instance, _, mock_fetchone, _ = mock_database_connection
    query = 'SELECT * FROM test WHERE id=?'
    params = ['string_instead_of_integer']
    mock_fetchone.side_effect = sqlite3.ProgrammingError
    with pytest.raises(sqlite3.ProgrammingError):
        instance.fetchone(query, params)


