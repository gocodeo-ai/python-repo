import pytest
from unittest.mock import patch, MagicMock
from shopping_cart.database import DatabaseConnection, add_item_to_cart_db

@pytest.fixture
def mock_database_connection():
    with patch('shopping_cart.database.sqlitedb.connect') as mock_connect:
        mock_conn = MagicMock()
        mock_connect.return_value = mock_conn

        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor

        mock_cursor.execute.return_value = None
        mock_cursor.fetchone.return_value = None
        mock_cursor.fetchall.return_value = []

        yield mock_conn

        mock_conn.close.assert_called_once()

@pytest.fixture
def mock_os_path():
    with patch('shopping_cart.database.os.path') as mock_path:
        mock_path.dirname.return_value = "/mocked/dir"
        mock_path.abspath.return_value = "/mocked/dir/shopping_cart.db"
        mock_path.join.return_value = "/mocked/dir/shopping_cart.db"
        yield mock_path

# happy_path - test_init_with_correct_path - Test that the database connection is initialized with the correct path
def test_init_with_correct_path(mock_os_path):
    db_conn = DatabaseConnection(db_path="shopping_cart_table.db")
    assert db_conn.db_path == "/mocked/dir/shopping_cart_table.db"
    assert db_conn.connection is None

# happy_path - test_connect_opens_connection - Test that the connection is opened successfully
def test_connect_opens_connection(mock_database_connection):
    db_conn = DatabaseConnection(db_path="shopping_cart.db")
    db_conn.connect()
    mock_database_connection.cursor.assert_called_once()

# happy_path - test_execute_without_params - Test that a query is executed without parameters
def test_execute_without_params(mock_database_connection):
    db_conn = DatabaseConnection(db_path="shopping_cart.db")
    db_conn.connect()
    db_conn.execute("CREATE TABLE IF NOT EXISTS test (id INTEGER)")
    mock_database_connection.cursor.return_value.execute.assert_called_once_with("CREATE TABLE IF NOT EXISTS test (id INTEGER)", [])

# happy_path - test_fetchall_returns_records - Test that fetchall returns multiple records
def test_fetchall_returns_records(mock_database_connection):
    mock_database_connection.cursor.return_value.fetchall.return_value = [(1,), (2,), (3,)]
    db_conn = DatabaseConnection(db_path="shopping_cart.db")
    db_conn.connect()
    results = db_conn.fetchall("SELECT * FROM test")
    assert results == [(1,), (2,), (3,)]

# happy_path - test_commit_finalizes_transaction - Test that commit finalizes the transaction
def test_commit_finalizes_transaction(mock_database_connection):
    db_conn = DatabaseConnection(db_path="shopping_cart.db")
    db_conn.connect()
    db_conn.commit()
    mock_database_connection.commit.assert_called_once()

# happy_path - test_close_connection - Test that the connection is closed
def test_close_connection(mock_database_connection):
    db_conn = DatabaseConnection(db_path="shopping_cart.db")
    db_conn.connect()
    db_conn.close()
    mock_database_connection.close.assert_called_once()
    assert db_conn.connection is None

# happy_path - test_add_item_to_cart_db - Test that an item is added to the cart database
def test_add_item_to_cart_db(mock_database_connection):
    add_item_to_cart_db("INSERT INTO cart (item) VALUES (?)", ['apple'])
    mock_database_connection.cursor.return_value.execute.assert_called_once_with("INSERT INTO cart (item) VALUES (?)", ['apple'])
    mock_database_connection.commit.assert_called_once()

# edge_case - test_connect_invalid_path_raises_error - Test that connecting with an invalid path raises an error
def test_connect_invalid_path_raises_error():
    with patch('shopping_cart.database.sqlite3.connect', side_effect=sqlite3.OperationalError):
        db_conn = DatabaseConnection(db_path="invalid_path.db")
        with pytest.raises(sqlite3.OperationalError):
            db_conn.connect()

# edge_case - test_execute_malformed_query_raises_error - Test that executing a malformed query raises an error
def test_execute_malformed_query_raises_error(mock_database_connection):
    db_conn = DatabaseConnection(db_path="shopping_cart.db")
    db_conn.connect()
    with pytest.raises(sqlite3.OperationalError):
        db_conn.execute("MALFORMED QUERY")

# edge_case - test_fetchone_no_result_returns_none - Test that fetchone with no result returns None
def test_fetchone_no_result_returns_none(mock_database_connection):
    db_conn = DatabaseConnection(db_path="shopping_cart.db")
    db_conn.connect()
    result = db_conn.fetchone("SELECT * FROM test WHERE id=999")
    assert result is None

# edge_case - test_fetchall_no_results_returns_empty_list - Test that fetchall with no results returns an empty list
def test_fetchall_no_results_returns_empty_list(mock_database_connection):
    db_conn = DatabaseConnection(db_path="shopping_cart.db")
    db_conn.connect()
    results = db_conn.fetchall("SELECT * FROM test WHERE id=999")
    assert results == []

# edge_case - test_close_already_closed_connection - Test that closing an already closed connection does not raise an error
def test_close_already_closed_connection(mock_database_connection):
    db_conn = DatabaseConnection(db_path="shopping_cart.db")
    db_conn.connect()
    db_conn.close()
    db_conn.close()
    mock_database_connection.close.assert_called_once()
    assert db_conn.connection is None

# edge_case - test_add_item_invalid_sql_raises_error - Test that adding an item with invalid SQL raises an error
def test_add_item_invalid_sql_raises_error(mock_database_connection):
    with pytest.raises(sqlite3.OperationalError):
        add_item_to_cart_db("INVALID SQL", ['apple'])

