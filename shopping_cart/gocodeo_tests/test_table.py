import pytest
from unittest import mock
import sqlite3

@pytest.fixture
def mock_db_setup():
    # Mock the sqlite3.connect method
    mock_connect = mock.Mock(return_value=mock.Mock())
    mock_cursor = mock.Mock()
    mock_connect.return_value.cursor.return_value = mock_cursor
    
    # Patch the sqlite3 module
    with mock.patch('sqlite3.connect', mock_connect):
        yield mock_connect, mock_cursor

@pytest.fixture
def mock_commit():
    # Mock the commit method
    mock_commit = mock.Mock()
    with mock.patch('sqlite3.Connection.commit', mock_commit):
        yield mock_commit

@pytest.fixture
def mock_close():
    # Mock the close method
    mock_close = mock.Mock()
    with mock.patch('sqlite3.Connection.close', mock_close):
        yield mock_close

@pytest.fixture
def mock_execute():
    # Mock the execute method
    mock_execute = mock.Mock()
    with mock.patch('sqlite3.Cursor.execute', mock_execute):
        yield mock_execute

# happy path - sqlite3.connect - Test that the database connection is established successfully.
def test_db_connection_success(mock_db_setup):
    mock_connect, _ = mock_db_setup
    conn = sqlite3.connect('shopping_cart.db')
    mock_connect.assert_called_once_with('shopping_cart.db')
    assert conn is not None
    assert conn.cursor() is not None


# happy path - cursor.execute - Test that the cart table is dropped successfully if it exists.
def test_drop_table_if_exists(mock_db_setup, mock_execute):
    _, mock_cursor = mock_db_setup
    drop_table_query = 'DROP TABLE IF EXISTS cart;'
    mock_cursor.execute(drop_table_query)
    mock_execute.assert_called_with(drop_table_query)


# happy path - cursor.execute - Test that the cart table is created successfully with the correct schema.
def test_create_cart_table(mock_db_setup, mock_execute):
    _, mock_cursor = mock_db_setup
    create_table_query = '''
    CREATE TABLE cart (
        id INTEGER PRIMARY KEY,
        item_id INTEGER,
        name TEXT,
        price REAL,
        quantity INTEGER,
        category TEXT,
        user_type TEXT,
        payment_status
    );
    '''
    mock_cursor.execute(create_table_query)
    mock_execute.assert_called_with(create_table_query)


# happy path - conn.commit - Test that the transaction is committed successfully.
def test_commit_transaction(mock_db_setup, mock_commit):
    mock_connect, _ = mock_db_setup
    conn = mock_connect()
    conn.commit()
    mock_commit.assert_called_once()


# happy path - conn.close - Test that the connection is closed successfully.
def test_close_connection(mock_db_setup, mock_close):
    mock_connect, _ = mock_db_setup
    conn = mock_connect()
    conn.close()
    mock_close.assert_called_once()


# edge case - cursor.execute - Test that an error is handled when trying to drop a non-existent table.
def test_drop_non_existent_table(mock_db_setup, mock_execute):
    _, mock_cursor = mock_db_setup
    drop_table_query = 'DROP TABLE IF EXISTS non_existent_table;'
    mock_cursor.execute(drop_table_query)
    mock_execute.assert_called_with(drop_table_query)


# edge case - cursor.execute - Test that an error is handled when trying to create a table with a syntax error in SQL.
def test_create_table_syntax_error(mock_db_setup, mock_execute):
    _, mock_cursor = mock_db_setup
    create_table_query = '''
    CREATE TABLE cart (
        id INTEGER PRIMARY KEY,
        item_id INTEGER,
        name TEXT,
        price REAL,
        quantity INTEGER,
        category TEXT,
        user_type TEXT payment_status
    );
    '''
    mock_cursor.execute.side_effect = sqlite3.Error("Syntax error")
    try:
        mock_cursor.execute(create_table_query)
    except sqlite3.Error as e:
        assert str(e) == "Syntax error"


# edge case - sqlite3.connect - Test that the connection fails gracefully when an invalid database name is provided.
def test_invalid_db_name():
    with mock.patch('sqlite3.connect', side_effect=sqlite3.Error("Invalid path")) as mock_connect:
        try:
            sqlite3.connect('invalid_path/shopping_cart.db')
        except sqlite3.Error as e:
            assert str(e) == "Invalid path"
        mock_connect.assert_called_once_with('invalid_path/shopping_cart.db')


# edge case - conn.commit - Test that an error is handled when trying to commit a transaction without any changes.
def test_commit_without_changes(mock_db_setup, mock_commit):
    mock_connect, _ = mock_db_setup
    conn = mock_connect()
    conn.commit.side_effect = sqlite3.Error("No changes to commit")
    try:
        conn.commit()
    except sqlite3.Error as e:
        assert str(e) == "No changes to commit"


# edge case - conn.close - Test that an error is handled when trying to close an already closed connection.
def test_close_already_closed_connection(mock_db_setup, mock_close):
    mock_connect, _ = mock_db_setup
    conn = mock_connect()
    conn.close()
    conn.close.side_effect = sqlite3.Error("Connection already closed")
    try:
        conn.close()
    except sqlite3.Error as e:
        assert str(e) == "Connection already closed"


