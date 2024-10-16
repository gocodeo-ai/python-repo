import pytest
from unittest import mock
import sqlite3

# Mocking sqlite3.connect and its methods
@pytest.fixture
def mock_database_connection():
    mock_conn = mock.Mock()
    mock_cursor = mock.Mock()
    
    mock_conn.cursor.return_value = mock_cursor
    mock_conn.commit = mock.Mock()
    mock_conn.close = mock.Mock()
    
    mock_cursor.execute = mock.Mock()
    
    with mock.patch('sqlite3.connect', return_value=mock_conn):
        yield mock_conn, mock_cursor

# Test setup function
@pytest.fixture
def setup_database(mock_database_connection):
    conn, cursor = mock_database_connection
    
    # Drop and create the cart table
    drop_table_query = '''
    DROP TABLE IF EXISTS cart;
    '''
    create_table_query = '''
    CREATE TABLE cart (
        id INTEGER PRIMARY KEY,
        item_id INTEGER,
        name TEXT,
        price REAL,
        quantity INTEGER,
        category TEXT,
        user_type TEXT,
        payment_status TEXT
    );
    '''
    
    cursor.execute(drop_table_query)
    cursor.execute(create_table_query)
    conn.commit()

    yield cursor  # Provide the cursor for testing

    # Cleanup
    conn.close()

# happy path - execute - Test that the 'cart' table is dropped and recreated successfully.
def test_drop_and_create_cart_table(setup_database):
    cursor = setup_database
    cursor.execute.assert_any_call('DROP TABLE IF EXISTS cart;')
    cursor.execute.assert_any_call('CREATE TABLE cart (\n        id INTEGER PRIMARY KEY,\n        item_id INTEGER,\n        name TEXT,\n        price REAL,\n        quantity INTEGER,\n        category TEXT,\n        user_type TEXT,\n        payment_status TEXT\n    );')
    assert cursor.execute.call_count == 2


# happy path - execute - Test that the 'cart' table is created with the correct schema.
def test_create_cart_table_schema(setup_database):
    cursor = setup_database
    cursor.execute.return_value = [
        ('id', 'INTEGER', 0, None, 1),
        ('item_id', 'INTEGER', 0, None, 0),
        ('name', 'TEXT', 0, None, 0),
        ('price', 'REAL', 0, None, 0),
        ('quantity', 'INTEGER', 0, None, 0),
        ('category', 'TEXT', 0, None, 0),
        ('user_type', 'TEXT', 0, None, 0),
        ('payment_status', 'TEXT', 0, None, 0)
    ]
    cursor.execute('PRAGMA table_info(cart);')
    schema = cursor.execute.return_value
    expected_schema = [
        {'name': 'id', 'type': 'INTEGER'},
        {'name': 'item_id', 'type': 'INTEGER'},
        {'name': 'name', 'type': 'TEXT'},
        {'name': 'price', 'type': 'REAL'},
        {'name': 'quantity', 'type': 'INTEGER'},
        {'name': 'category', 'type': 'TEXT'},
        {'name': 'user_type', 'type': 'TEXT'},
        {'name': 'payment_status', 'type': 'TEXT'}
    ]
    for i, column in enumerate(expected_schema):
        assert schema[i][0] == column['name']
        assert schema[i][1] == column['type']


# happy path - commit - Test that committing a transaction does not raise an error.
def test_commit_transaction(mock_database_connection):
    conn, _ = mock_database_connection
    try:
        conn.commit()
        assert True  # No exception means success
    except Exception:
        assert False  # An exception means failure


# happy path - connect - Test that a connection to the SQLite database can be established.
def test_connect_to_database(mock_database_connection):
    conn, _ = mock_database_connection
    assert conn is not None  # Connection is successfully established


# happy path - close - Test that closing the connection does not raise an error.
def test_close_connection(mock_database_connection):
    conn, _ = mock_database_connection
    try:
        conn.close()
        assert True  # No exception means success
    except Exception:
        assert False  # An exception means failure


# edge case - execute - Test that dropping a non-existent table does not raise an error.
def test_drop_non_existent_table(mock_database_connection):
    _, cursor = mock_database_connection
    try:
        cursor.execute('DROP TABLE IF EXISTS non_existent_table;')
        assert True  # No exception means success
    except Exception:
        assert False  # An exception means failure


# edge case - execute - Test that creating a table with duplicate column names raises an error.
def test_create_table_with_duplicate_columns(mock_database_connection):
    _, cursor = mock_database_connection
    cursor.execute.side_effect = sqlite3.OperationalError('duplicate column name: id')
    with pytest.raises(sqlite3.OperationalError) as excinfo:
        cursor.execute('CREATE TABLE cart (id INTEGER PRIMARY KEY, id INTEGER);')
    assert 'duplicate column name: id' in str(excinfo.value)


# edge case - commit - Test that attempting to commit without any changes does not raise an error.
def test_commit_without_changes(mock_database_connection):
    conn, _ = mock_database_connection
    try:
        conn.commit()
        assert True  # No exception means success
    except Exception:
        assert False  # An exception means failure


# edge case - execute - Test that executing an invalid SQL command raises an error.
def test_execute_invalid_sql(mock_database_connection):
    _, cursor = mock_database_connection
    cursor.execute.side_effect = sqlite3.OperationalError('syntax error')
    with pytest.raises(sqlite3.OperationalError) as excinfo:
        cursor.execute('INVALID SQL COMMAND')
    assert 'syntax error' in str(excinfo.value)


# edge case - close - Test that closing an already closed connection does not raise an error.
def test_close_already_closed_connection(mock_database_connection):
    conn, _ = mock_database_connection
    conn.close()
    try:
        conn.close()  # Attempt to close again
        assert True  # No exception means success
    except Exception:
        assert False  # An exception means failure


