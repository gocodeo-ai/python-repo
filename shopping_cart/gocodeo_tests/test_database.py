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
        
        mock_cursor.fetchone.return_value = (1,)
        mock_cursor.fetchall.return_value = [(1,), (2,)]
        
        db_connection = DatabaseConnection('valid_path.db')
        db_connection.connection = mock_connection
        
        yield db_connection

        db_connection.close()

@pytest.fixture
def mock_add_item_to_cart_db(mock_database_connection):
    with mock.patch('shopping_cart.database.database_connection', mock_database_connection):
        yield add_item_to_cart_db

# happy path - connect - Test that a connection can be established with a valid database path
def test_connect_valid_db_path(mock_database_connection):
    assert mock_database_connection.connection is not None


# happy path - execute - Test that a query can be executed without parameters
def test_execute_query_without_params(mock_database_connection):
    mock_database_connection.execute('CREATE TABLE test (id INTEGER PRIMARY KEY)')
    mock_database_connection.connection.cursor().execute.assert_called_with('CREATE TABLE test (id INTEGER PRIMARY KEY)', [])


# happy path - fetchone - Test that fetchone returns the correct result for a single row
def test_fetchone_single_row(mock_database_connection):
    result = mock_database_connection.fetchone('SELECT * FROM test WHERE id = 1')
    assert result == (1,)


# happy path - fetchall - Test that fetchall returns all rows from a table
def test_fetchall_all_rows(mock_database_connection):
    results = mock_database_connection.fetchall('SELECT * FROM test')
    assert results == [(1,), (2,)]


# happy path - close - Test that the connection is closed properly
def test_close_connection(mock_database_connection):
    mock_database_connection.close()
    assert mock_database_connection.connection is None


# happy path - add_item_to_cart_db - Test that an item is added to the cart database
def test_add_item_to_cart_db(mock_add_item_to_cart_db):
    mock_add_item_to_cart_db('INSERT INTO cart (item) VALUES (?)', ['apple'])
    mock_add_item_to_cart_db.connection.cursor().execute.assert_called_with('INSERT INTO cart (item) VALUES (?)', ['apple'])
    mock_add_item_to_cart_db.connection.commit.assert_called_once()


# edge case - execute - Test executing a query on a closed connection
def test_execute_on_closed_connection(mock_database_connection):
    mock_database_connection.close()
    with pytest.raises(sqlite3.OperationalError):
        mock_database_connection.execute('SELECT * FROM test')


# edge case - fetchone - Test fetchone with a query that returns no results
def test_fetchone_no_results(mock_database_connection):
    mock_database_connection.connection.cursor().fetchone.return_value = None
    result = mock_database_connection.fetchone('SELECT * FROM test WHERE id = 999')
    assert result is None


# edge case - fetchall - Test fetchall with a query that returns no results
def test_fetchall_no_results(mock_database_connection):
    mock_database_connection.connection.cursor().fetchall.return_value = []
    results = mock_database_connection.fetchall('SELECT * FROM test WHERE id = 999')
    assert results == []


# edge case - connect - Test connecting with an invalid database path
def test_connect_invalid_db_path():
    with mock.patch('shopping_cart.database.sqlite3.connect', side_effect=sqlite3.OperationalError):
        db_connection = DatabaseConnection('invalid_path.db')
        with pytest.raises(sqlite3.OperationalError):
            db_connection.connect()


# edge case - add_item_to_cart_db - Test adding an item to the cart with invalid SQL syntax
def test_add_item_invalid_sql(mock_add_item_to_cart_db):
    with pytest.raises(sqlite3.OperationalError):
        mock_add_item_to_cart_db('INSERT INTO cart (item VALUES (?)', ['apple'])


