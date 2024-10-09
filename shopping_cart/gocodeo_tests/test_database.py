import pytest
from unittest import mock
import sqlite3
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
            
            db = DatabaseConnection('valid_db_path')
            yield db, mock_connect, mock_connection, mock_connect_method, mock_execute_method, mock_fetchone_method, mock_fetchall_method, mock_commit_method, mock_close_method

@pytest.fixture
def mock_add_item_to_cart_db():
    with mock.patch('shopping_cart.database.database_connection') as mock_db_connection:
        yield mock_db_connection

# happy path - connect - Test that connection is established with a valid database path
def test_connect_with_valid_db_path(mock_database_connection):
    db, mock_connect, mock_connection, *_ = mock_database_connection
    db.connect()
    mock_connect.assert_called_once_with('valid_db_path')
    assert db.connection is not None


# happy path - execute - Test that execute runs a valid query without parameters
def test_execute_with_valid_query_no_params(mock_database_connection):
    db, _, _, _, mock_execute_method, *_ = mock_database_connection
    db.execute('CREATE TABLE test (id INTEGER)')
    mock_execute_method.assert_called_once_with('CREATE TABLE test (id INTEGER)', [])


# happy path - fetchone - Test that fetchone returns the first row of the result set
def test_fetchone_returns_first_row(mock_database_connection):
    db, _, _, _, _, mock_fetchone_method, *_ = mock_database_connection
    mock_fetchone_method.return_value = 'first_row'
    result = db.fetchone('SELECT * FROM test')
    mock_fetchone_method.assert_called_once_with('SELECT * FROM test', [])
    assert result == 'first_row'


# happy path - fetchall - Test that fetchall returns all rows of the result set
def test_fetchall_returns_all_rows(mock_database_connection):
    db, _, _, _, _, _, mock_fetchall_method, *_ = mock_database_connection
    mock_fetchall_method.return_value = 'all_rows'
    results = db.fetchall('SELECT * FROM test')
    mock_fetchall_method.assert_called_once_with('SELECT * FROM test', [])
    assert results == 'all_rows'


# happy path - commit - Test that commit successfully commits the transaction
def test_commit_successful(mock_database_connection):
    db, _, _, _, _, _, _, mock_commit_method, _ = mock_database_connection
    db.commit()
    mock_commit_method.assert_called_once()


# happy path - close - Test that close successfully closes the connection
def test_close_successful(mock_database_connection):
    db, _, _, _, _, _, _, _, mock_close_method = mock_database_connection
    db.close()
    mock_close_method.assert_called_once()
    assert db.connection is None


# happy path - add_item_to_cart_db - Test that add_item_to_cart_db adds an item successfully
def test_add_item_to_cart_db_success(mock_add_item_to_cart_db):
    mock_db_connection = mock_add_item_to_cart_db
    add_item_to_cart_db('INSERT INTO cart (item) VALUES (?)', ['item1'])
    mock_db_connection.connect.assert_called_once()
    mock_db_connection.execute.assert_called_once_with('INSERT INTO cart (item) VALUES (?)', ['item1'])
    mock_db_connection.commit.assert_called_once()
    mock_db_connection.close.assert_called_once()


# edge case - connect - Test that connection fails with an invalid database path
def test_connect_with_invalid_db_path():
    with mock.patch('shopping_cart.database.sqlite3.connect', side_effect=sqlite3.OperationalError):
        db = DatabaseConnection('invalid_db_path')
        with pytest.raises(sqlite3.OperationalError):
            db.connect()


# edge case - execute - Test that execute raises an error with an invalid query
def test_execute_with_invalid_query(mock_database_connection):
    db, _, _, _, mock_execute_method, *_ = mock_database_connection
    mock_execute_method.side_effect = sqlite3.OperationalError
    with pytest.raises(sqlite3.OperationalError):
        db.execute('INVALID QUERY')


# edge case - fetchone - Test that fetchone raises an error if no connection is established
def test_fetchone_no_connection(mock_database_connection):
    db, _, _, _, _, mock_fetchone_method, *_ = mock_database_connection
    mock_fetchone_method.side_effect = sqlite3.ProgrammingError
    with pytest.raises(sqlite3.ProgrammingError):
        db.fetchone('SELECT * FROM test')


# edge case - fetchall - Test that fetchall raises an error if no connection is established
def test_fetchall_no_connection(mock_database_connection):
    db, _, _, _, _, _, mock_fetchall_method, *_ = mock_database_connection
    mock_fetchall_method.side_effect = sqlite3.ProgrammingError
    with pytest.raises(sqlite3.ProgrammingError):
        db.fetchall('SELECT * FROM test')


# edge case - commit - Test that commit raises an error if no connection is established
def test_commit_no_connection(mock_database_connection):
    db, _, _, _, _, _, _, mock_commit_method, _ = mock_database_connection
    mock_commit_method.side_effect = sqlite3.ProgrammingError
    with pytest.raises(sqlite3.ProgrammingError):
        db.commit()


# edge case - close - Test that close does not raise an error if no connection is established
def test_close_no_connection(mock_database_connection):
    db, _, _, _, _, _, _, _, mock_close_method = mock_database_connection
    db.close()
    mock_close_method.assert_called_once()
    assert db.connection is None


# edge case - add_item_to_cart_db - Test that add_item_to_cart_db raises an error with invalid SQL
def test_add_item_to_cart_db_invalid_sql(mock_add_item_to_cart_db):
    mock_db_connection = mock_add_item_to_cart_db
    mock_db_connection.execute.side_effect = sqlite3.OperationalError
    with pytest.raises(sqlite3.OperationalError):
        add_item_to_cart_db('INVALID SQL', ['item1'])


