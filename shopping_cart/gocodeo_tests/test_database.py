import pytest
from unittest import mock
from shopping_cart.database import DatabaseConnection, add_item_to_cart_db

@pytest.fixture
def mock_database_connection():
    with mock.patch('shopping_cart.database.DatabaseConnection.__init__', return_value=None) as mock_init, \
         mock.patch('shopping_cart.database.DatabaseConnection.connect') as mock_connect, \
         mock.patch('shopping_cart.database.DatabaseConnection.execute') as mock_execute, \
         mock.patch('shopping_cart.database.DatabaseConnection.fetchone') as mock_fetchone, \
         mock.patch('shopping_cart.database.DatabaseConnection.fetchall') as mock_fetchall, \
         mock.patch('shopping_cart.database.DatabaseConnection.commit') as mock_commit, \
         mock.patch('shopping_cart.database.DatabaseConnection.close') as mock_close:
        
        mock_init.return_value = None
        mock_connect.return_value = None
        mock_execute.return_value = None
        mock_fetchone.return_value = None
        mock_fetchall.return_value = []
        mock_commit.return_value = None
        mock_close.return_value = None
        
        yield {
            'mock_init': mock_init,
            'mock_connect': mock_connect,
            'mock_execute': mock_execute,
            'mock_fetchone': mock_fetchone,
            'mock_fetchall': mock_fetchall,
            'mock_commit': mock_commit,
            'mock_close': mock_close
        }

@pytest.fixture
def mock_sqlite3():
    with mock.patch('shopping_cart.database.sqlite3.connect') as mock_sqlite_connect:
        mock_connection = mock.Mock()
        mock_cursor = mock.Mock()
        
        mock_sqlite_connect.return_value = mock_connection
        mock_connection.cursor.return_value = mock_cursor
        mock_cursor.execute.return_value = None
        mock_cursor.fetchone.return_value = None
        mock_cursor.fetchall.return_value = []
        mock_connection.commit.return_value = None
        mock_connection.close.return_value = None
        
        yield {
            'mock_sqlite_connect': mock_sqlite_connect,
            'mock_connection': mock_connection,
            'mock_cursor': mock_cursor
        }

# happy_path - test_init_with_correct_path - Test that the database connection is initialized with the correct path
def test_init_with_correct_path(mock_database_connection):
    db_path = 'shopping_cart.db'
    db = DatabaseConnection(db_path)
    assert db.db_path == db_path
    assert db.connection is None
    mock_database_connection['mock_init'].assert_called_once_with(db_path)

# happy_path - test_connect_establishes_connection - Test that connect establishes a connection to the database
def test_connect_establishes_connection(mock_database_connection, mock_sqlite3):
    db_path = 'shopping_cart.db'
    db = DatabaseConnection(db_path)
    db.connect()
    mock_sqlite3['mock_sqlite_connect'].assert_called_once_with(db_path)
    assert db.connection == mock_sqlite3['mock_connection']

# happy_path - test_execute_query_without_params - Test that execute runs a query without parameters
def test_execute_query_without_params(mock_database_connection):
    db = DatabaseConnection('shopping_cart.db')
    db.connect()
    query = 'CREATE TABLE test (id INTEGER)'
    db.execute(query)
    mock_database_connection['mock_execute'].assert_called_once_with(query, [])

# happy_path - test_fetchone_retrieves_single_record - Test that fetchone retrieves a single record
def test_fetchone_retrieves_single_record(mock_database_connection):
    db = DatabaseConnection('shopping_cart.db')
    db.connect()
    query = 'SELECT * FROM test WHERE id = 1'
    result = db.fetchone(query)
    mock_database_connection['mock_fetchone'].assert_called_once_with(query, [])
    assert result is None

# happy_path - test_fetchall_retrieves_all_records - Test that fetchall retrieves all records
def test_fetchall_retrieves_all_records(mock_database_connection):
    db = DatabaseConnection('shopping_cart.db')
    db.connect()
    query = 'SELECT * FROM test'
    results = db.fetchall(query)
    mock_database_connection['mock_fetchall'].assert_called_once_with(query, [])
    assert results == []

# happy_path - test_commit_saves_changes - Test that commit saves the changes to the database
def test_commit_saves_changes(mock_database_connection):
    db = DatabaseConnection('shopping_cart.db')
    db.connect()
    db.commit()
    mock_database_connection['mock_commit'].assert_called_once()

# happy_path - test_close_closes_connection - Test that close properly closes the database connection
def test_close_closes_connection(mock_database_connection):
    db = DatabaseConnection('shopping_cart.db')
    db.connect()
    db.close()
    mock_database_connection['mock_close'].assert_called_once()
    assert db.connection is None

# happy_path - test_add_item_to_cart_db_adds_item - Test that add_item_to_cart_db adds an item to the cart
def test_add_item_to_cart_db_adds_item(mock_database_connection):
    query = 'INSERT INTO cart (item) VALUES (?)'
    params = ['apple']
    add_item_to_cart_db(query, params)
    mock_database_connection['mock_connect'].assert_called_once()
    mock_database_connection['mock_execute'].assert_called_once_with(query, params)
    mock_database_connection['mock_commit'].assert_called_once()
    mock_database_connection['mock_close'].assert_called_once()

# edge_case - test_init_with_empty_path - Test that __init__ handles an empty path
def test_init_with_empty_path(mock_database_connection):
    db_path = ''
    db = DatabaseConnection(db_path)
    assert db.db_path == db_path
    assert db.connection is None
    mock_database_connection['mock_init'].assert_called_once_with(db_path)

# edge_case - test_connect_non_existent_path - Test that connect handles a non-existent database path
def test_connect_non_existent_path(mock_database_connection, mock_sqlite3):
    db_path = '/non/existent/path.db'
    db = DatabaseConnection(db_path)
    with pytest.raises(sqlite3.OperationalError):
        db.connect()
    mock_sqlite3['mock_sqlite_connect'].assert_called_once_with(db_path)

# edge_case - test_execute_malformed_query - Test that execute handles a malformed query
def test_execute_malformed_query(mock_database_connection):
    db = DatabaseConnection('shopping_cart.db')
    db.connect()
    query = 'MALFORMED QUERY'
    with pytest.raises(sqlite3.Error):
        db.execute(query)
    mock_database_connection['mock_execute'].assert_called_once_with(query, [])

# edge_case - test_fetchone_no_results - Test that fetchone handles a query with no results
def test_fetchone_no_results(mock_database_connection):
    db = DatabaseConnection('shopping_cart.db')
    db.connect()
    query = 'SELECT * FROM test WHERE id = -1'
    result = db.fetchone(query)
    mock_database_connection['mock_fetchone'].assert_called_once_with(query, [])
    assert result is None

# edge_case - test_fetchall_no_results - Test that fetchall handles a query with no results
def test_fetchall_no_results(mock_database_connection):
    db = DatabaseConnection('shopping_cart.db')
    db.connect()
    query = 'SELECT * FROM test WHERE id = -1'
    results = db.fetchall(query)
    mock_database_connection['mock_fetchall'].assert_called_once_with(query, [])
    assert results == []

# edge_case - test_close_already_closed_connection - Test that close handles closing an already closed connection
def test_close_already_closed_connection(mock_database_connection):
    db = DatabaseConnection('shopping_cart.db')
    db.connect()
    db.close()
    db.close()
    mock_database_connection['mock_close'].assert_called_once()
    assert db.connection is None

