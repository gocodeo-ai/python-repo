import pytest
from unittest import mock
import sqlite3
from shopping_cart.database import DatabaseConnection, add_item_to_cart_db

@pytest.fixture
def mock_database_connection():
    with mock.patch('shopping_cart.database.sqlite3.connect') as mock_connect:
        mock_conn = mock.Mock()
        mock_connect.return_value = mock_conn

        with mock.patch.object(DatabaseConnection, 'commit') as mock_commit, \
             mock.patch.object(DatabaseConnection, 'close') as mock_close, \
             mock.patch.object(DatabaseConnection, 'execute') as mock_execute, \
             mock.patch.object(DatabaseConnection, 'fetchone') as mock_fetchone, \
             mock.patch.object(DatabaseConnection, 'fetchall') as mock_fetchall:
             
            db = DatabaseConnection('valid_db_path')
            db.connect()
            yield db, mock_conn, mock_commit, mock_close, mock_execute, mock_fetchone, mock_fetchall
            
            db.close()

@pytest.fixture
def setup_database(mock_database_connection):
    db, mock_conn, mock_commit, mock_close, mock_execute, mock_fetchone, mock_fetchall = mock_database_connection
    mock_execute.return_value = None
    mock_fetchone.return_value = (1, 'item1')
    mock_fetchall.return_value = [(1, 'item1'), (2, 'item2')]
    return db, mock_conn

@pytest.fixture
def invalid_database_connection():
    with mock.patch('shopping_cart.database.sqlite3.connect', side_effect=sqlite3.OperationalError):
        yield DatabaseConnection('invalid_db_path')

# happy path - connect - Test that connection is successfully established to the database
def test_connect_successful(mock_database_connection):
    db, mock_conn, _, _, _, _, _ = mock_database_connection
    assert db.connection is not None
    mock_conn.cursor.assert_called_once()


# happy path - execute - Test that execute runs a query without parameters
def test_execute_query_without_params(mock_database_connection):
    db, _, _, _, mock_execute, _, _ = mock_database_connection
    query = 'CREATE TABLE test (id INTEGER)'
    db.execute(query)
    mock_execute.assert_called_once_with(query, [])


# happy path - fetchone - Test that fetchone retrieves a single record
def test_fetchone_single_record(setup_database):
    db, _ = setup_database
    result = db.fetchone('SELECT * FROM test WHERE id=1')
    assert result == (1, 'item1')


# happy path - fetchall - Test that fetchall retrieves all records
def test_fetchall_all_records(setup_database):
    db, _ = setup_database
    results = db.fetchall('SELECT * FROM test')
    assert results == [(1, 'item1'), (2, 'item2')]


# happy path - commit - Test that commit saves changes to the database
def test_commit_changes(mock_database_connection):
    db, _, mock_commit, _, _, _, _ = mock_database_connection
    db.commit()
    mock_commit.assert_called_once()


# happy path - close - Test that close closes the database connection
def test_close_connection(mock_database_connection):
    db, _, _, mock_close, _, _, _ = mock_database_connection
    db.close()
    assert db.connection is None
    mock_close.assert_called_once()


# edge case - connect - Test that connect handles invalid database path
def test_connect_invalid_path(invalid_database_connection):
    db = invalid_database_connection
    with pytest.raises(sqlite3.OperationalError):
        db.connect()


# edge case - execute - Test that execute handles invalid SQL syntax
def test_execute_invalid_sql_syntax(mock_database_connection):
    db, _, _, _, mock_execute, _, _ = mock_database_connection
    mock_execute.side_effect = sqlite3.OperationalError
    with pytest.raises(sqlite3.OperationalError):
        db.execute('INVALID SQL')


# edge case - fetchone - Test that fetchone handles no matching records
def test_fetchone_no_matching_records(mock_database_connection):
    db, _, _, _, _, mock_fetchone, _ = mock_database_connection
    mock_fetchone.return_value = None
    result = db.fetchone('SELECT * FROM test WHERE id=999')
    assert result is None


# edge case - fetchall - Test that fetchall handles empty table
def test_fetchall_empty_table(mock_database_connection):
    db, _, _, _, _, _, mock_fetchall = mock_database_connection
    mock_fetchall.return_value = []
    results = db.fetchall('SELECT * FROM empty_table')
    assert results == []


# edge case - close - Test that close handles closing an already closed connection
def test_close_already_closed_connection(mock_database_connection):
    db, _, _, mock_close, _, _, _ = mock_database_connection
    db.close()
    db.close()  # Close again
    mock_close.assert_called_once()


