import pytest
from unittest import mock
from shopping_cart.database import DatabaseConnection, add_item_to_cart_db

@pytest.fixture
def mock_database_connection():
    with mock.patch('shopping_cart.database.sqlite3.connect') as mock_connect:
        mock_connection = mock.Mock()
        mock_connect.return_value = mock_connection
        
        mock_connection.cursor.return_value = mock.Mock()
        yield mock_connection

@pytest.fixture
def mock_database_class():
    with mock.patch('shopping_cart.database.DatabaseConnection.__init__', return_value=None) as mock_init:
        with mock.patch('shopping_cart.database.DatabaseConnection.connect') as mock_connect:
            with mock.patch('shopping_cart.database.DatabaseConnection.execute') as mock_execute:
                with mock.patch('shopping_cart.database.DatabaseConnection.fetchone') as mock_fetchone:
                    with mock.patch('shopping_cart.database.DatabaseConnection.fetchall') as mock_fetchall:
                        with mock.patch('shopping_cart.database.DatabaseConnection.commit') as mock_commit:
                            with mock.patch('shopping_cart.database.DatabaseConnection.close') as mock_close:
                                yield (mock_init, mock_connect, mock_execute, mock_fetchone, mock_fetchall, mock_commit, mock_close)

@pytest.fixture
def mock_add_item_to_cart_db():
    with mock.patch('shopping_cart.database.add_item_to_cart_db') as mock_add_item:
        yield mock_add_item

# happy path - connect - Test that the database connection is successfully established
def test_connect_success(mock_database_connection, mock_database_class):
    _, mock_connect, _, _, _, _, _ = mock_database_class
    db_connection = DatabaseConnection('shopping_cart.db')
    db_connection.connect()
    mock_connect.assert_called_once_with('shopping_cart.db')
    assert db_connection.connection is not None


# happy path - execute - Test that a query is executed without parameters
def test_execute_no_params(mock_database_connection, mock_database_class):
    _, _, mock_execute, _, _, _, _ = mock_database_class
    db_connection = DatabaseConnection('shopping_cart.db')
    db_connection.connect()
    db_connection.execute('CREATE TABLE test (id INTEGER)')
    mock_execute.assert_called_once_with('CREATE TABLE test (id INTEGER)', [])


# happy path - execute - Test that a query is executed with parameters
def test_execute_with_params(mock_database_connection, mock_database_class):
    _, _, mock_execute, _, _, _, _ = mock_database_class
    db_connection = DatabaseConnection('shopping_cart.db')
    db_connection.connect()
    db_connection.execute('INSERT INTO test (id) VALUES (?)', [1])
    mock_execute.assert_called_once_with('INSERT INTO test (id) VALUES (?)', [1])


# happy path - fetchone - Test that fetchone returns a single row
def test_fetchone_single_row(mock_database_connection, mock_database_class):
    _, _, _, mock_fetchone, _, _, _ = mock_database_class
    mock_fetchone.return_value = [1]
    db_connection = DatabaseConnection('shopping_cart.db')
    db_connection.connect()
    result = db_connection.fetchone('SELECT id FROM test WHERE id = ?', [1])
    assert result == [1]


# happy path - fetchall - Test that fetchall returns all rows
def test_fetchall_all_rows(mock_database_connection, mock_database_class):
    _, _, _, _, mock_fetchall, _, _ = mock_database_class
    mock_fetchall.return_value = [[1]]
    db_connection = DatabaseConnection('shopping_cart.db')
    db_connection.connect()
    results = db_connection.fetchall('SELECT id FROM test')
    assert results == [[1]]


# happy path - commit - Test that commit is successful after executing a query
def test_commit_success(mock_database_connection, mock_database_class):
    _, _, _, _, _, mock_commit, _ = mock_database_class
    db_connection = DatabaseConnection('shopping_cart.db')
    db_connection.connect()
    db_connection.execute('INSERT INTO test (id) VALUES (?)', [1])
    db_connection.commit()
    mock_commit.assert_called_once()


# edge case - connect - Test that connect raises an error with invalid path
def test_connect_invalid_path(mock_database_connection, mock_database_class):
    _, mock_connect, _, _, _, _, _ = mock_database_class
    mock_connect.side_effect = sqlite3.OperationalError
    db_connection = DatabaseConnection('invalid_path.db')
    with pytest.raises(sqlite3.OperationalError):
        db_connection.connect()


# edge case - execute - Test that execute raises an error with invalid query
def test_execute_invalid_query(mock_database_connection, mock_database_class):
    _, _, mock_execute, _, _, _, _ = mock_database_class
    mock_execute.side_effect = sqlite3.OperationalError
    db_connection = DatabaseConnection('shopping_cart.db')
    db_connection.connect()
    with pytest.raises(sqlite3.OperationalError):
        db_connection.execute('INVALID QUERY')


# edge case - fetchone - Test that fetchone returns None for no match
def test_fetchone_no_match(mock_database_connection, mock_database_class):
    _, _, _, mock_fetchone, _, _, _ = mock_database_class
    mock_fetchone.return_value = None
    db_connection = DatabaseConnection('shopping_cart.db')
    db_connection.connect()
    result = db_connection.fetchone('SELECT id FROM test WHERE id = ?', [999])
    assert result is None


# edge case - fetchall - Test that fetchall returns empty list for no data
def test_fetchall_no_data(mock_database_connection, mock_database_class):
    _, _, _, _, mock_fetchall, _, _ = mock_database_class
    mock_fetchall.return_value = []
    db_connection = DatabaseConnection('shopping_cart.db')
    db_connection.connect()
    results = db_connection.fetchall('SELECT id FROM test WHERE id = ?', [999])
    assert results == []


# edge case - close - Test that close sets connection to None
def test_close_connection(mock_database_connection, mock_database_class):
    _, _, _, _, _, _, mock_close = mock_database_class
    db_connection = DatabaseConnection('shopping_cart.db')
    db_connection.connect()
    db_connection.close()
    mock_close.assert_called_once()
    assert db_connection.connection is None


