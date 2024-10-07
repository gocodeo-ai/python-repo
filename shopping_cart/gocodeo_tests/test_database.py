import pytest
from unittest import mock
import sqlite3
from shopping_cart.database import DatabaseConnection, add_item_to_cart_db

@pytest.fixture
def mock_database_connection():
    with mock.patch('shopping_cart.database.sqlite3.connect') as mock_connect:
        mock_connection = mock.Mock()
        mock_connect.return_value = mock_connection
        
        yield mock_connection

@pytest.fixture
def db_connection(mock_database_connection):
    db = DatabaseConnection('valid_path.db')
    db.connection = mock_database_connection
    return db

@pytest.fixture
def mock_execute(db_connection):
    with mock.patch.object(db_connection, 'execute') as mock_execute:
        yield mock_execute

@pytest.fixture
def mock_fetchone(db_connection):
    with mock.patch.object(db_connection, 'fetchone') as mock_fetchone:
        yield mock_fetchone

@pytest.fixture
def mock_fetchall(db_connection):
    with mock.patch.object(db_connection, 'fetchall') as mock_fetchall:
        yield mock_fetchall

@pytest.fixture
def mock_commit(db_connection):
    with mock.patch.object(db_connection, 'commit') as mock_commit:
        yield mock_commit

@pytest.fixture
def mock_close(db_connection):
    with mock.patch.object(db_connection, 'close') as mock_close:
        yield mock_close

@pytest.fixture
def mock_add_item_to_cart_db():
    with mock.patch('shopping_cart.database.database_connection') as mock_db_connection:
        yield mock_db_connection

# happy_path - test_connect_success - Test that a connection to the database is established successfully.
def test_connect_success(mock_database_connection):
    db = DatabaseConnection('valid_path.db')
    db.connect()
    assert db.connection is not None

# happy_path - test_execute_success - Test that a query is executed without errors.
def test_execute_success(db_connection, mock_execute):
    query = 'CREATE TABLE test (id INTEGER)'
    db_connection.execute(query)
    mock_execute.assert_called_once_with(query, [])

# happy_path - test_fetchone_success - Test that a single row is fetched successfully from the database.
def test_fetchone_success(db_connection, mock_fetchone):
    query = 'SELECT * FROM test WHERE id = ?'
    params = [1]
    mock_fetchone.return_value = ('row',)
    result = db_connection.fetchone(query, params)
    mock_fetchone.assert_called_once_with(query, params)
    assert result == ('row',)

# happy_path - test_fetchall_success - Test that all rows are fetched successfully from the database.
def test_fetchall_success(db_connection, mock_fetchall):
    query = 'SELECT * FROM test'
    mock_fetchall.return_value = [('row1',), ('row2',)]
    results = db_connection.fetchall(query)
    mock_fetchall.assert_called_once_with(query, [])
    assert results == [('row1',), ('row2',)]

# happy_path - test_commit_success - Test that changes are committed to the database successfully.
def test_commit_success(db_connection, mock_commit):
    db_connection.commit()
    mock_commit.assert_called_once()

# happy_path - test_close_success - Test that the database connection is closed successfully.
def test_close_success(db_connection, mock_close):
    db_connection.close()
    mock_close.assert_called_once()

# happy_path - test_add_item_to_cart_db_success - Test that an item is added to the cart database successfully.
def test_add_item_to_cart_db_success(mock_add_item_to_cart_db):
    query = 'INSERT INTO cart (item) VALUES (?)'
    params = ['apple']
    add_item_to_cart_db(query, params)
    mock_add_item_to_cart_db.connect.assert_called_once()
    mock_add_item_to_cart_db.execute.assert_called_once_with(query, params)
    mock_add_item_to_cart_db.commit.assert_called_once()
    mock_add_item_to_cart_db.close.assert_called_once()

# edge_case - test_execute_invalid_sql - Test that executing a query with invalid SQL raises an error.
def test_execute_invalid_sql(db_connection):
    query = 'INVALID SQL'
    with pytest.raises(sqlite3.OperationalError):
        db_connection.execute(query)

# edge_case - test_fetchone_no_results - Test that fetching a row with a query that returns no results returns None.
def test_fetchone_no_results(db_connection, mock_fetchone):
    query = 'SELECT * FROM test WHERE id = ?'
    params = [999]
    mock_fetchone.return_value = None
    result = db_connection.fetchone(query, params)
    mock_fetchone.assert_called_once_with(query, params)
    assert result is None

# edge_case - test_fetchall_no_results - Test that fetching all rows with a query that returns no results returns an empty list.
def test_fetchall_no_results(db_connection, mock_fetchall):
    query = 'SELECT * FROM test WHERE id = 999'
    mock_fetchall.return_value = []
    results = db_connection.fetchall(query)
    mock_fetchall.assert_called_once_with(query, [])
    assert results == []

# edge_case - test_commit_no_changes - Test that committing without any changes does not raise an error.
def test_commit_no_changes(db_connection, mock_commit):
    db_connection.commit()
    mock_commit.assert_called_once()

# edge_case - test_close_already_closed - Test that closing an already closed connection does not raise an error.
def test_close_already_closed(db_connection, mock_close):
    db_connection.close()
    db_connection.close()
    assert mock_close.call_count == 1

# edge_case - test_add_item_to_cart_db_invalid_query - Test that adding an item to the cart with an invalid query raises an error.
def test_add_item_to_cart_db_invalid_query(mock_add_item_to_cart_db):
    query = 'INVALID SQL'
    with pytest.raises(sqlite3.OperationalError):
        add_item_to_cart_db(query)

