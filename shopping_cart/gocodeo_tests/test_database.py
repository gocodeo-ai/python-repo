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
        
        yield {
            'connection': mock_connection,
            'cursor': mock_cursor,
            'connect': mock_connect
        }

@pytest.fixture
def setup_database(mock_database_connection):
    db_connection = DatabaseConnection("mock_db_path")
    db_connection.connection = mock_database_connection['connection']
    
    return db_connection

# happy_path - add_item_to_cart_db - Add an item to cart successfully
def test_add_item_to_cart_db_success(setup_database, mock_database_connection):
    query = 'INSERT INTO cart (item_id, quantity) VALUES (?, ?)'
    params = (1, 2)
    add_item_to_cart_db(query, params)
    mock_database_connection['cursor'].execute.assert_called_once_with(query, params)
    mock_database_connection['connection'].commit.assert_called_once()
    mock_database_connection['connection'].close.assert_called_once()

# happy_path - fetchone - Fetch one item from the database
def test_fetch_one_item(setup_database, mock_database_connection):
    query = 'SELECT * FROM cart WHERE item_id = ?'
    params = (1,)
    mock_database_connection['cursor'].fetchone.return_value = (1, 2)
    result = setup_database.fetchone(query, params)
    assert result == (1, 2)
    mock_database_connection['cursor'].execute.assert_called_once_with(query, params) 
    mock_database_connection['cursor'].fetchone.assert_called_once()

# happy_path - fetchall - Fetch all items from the database
def test_fetch_all_items(setup_database, mock_database_connection):
    query = 'SELECT * FROM cart'
    mock_database_connection['cursor'].fetchall.return_value = [(1, 2), (2, 3)]
    results = setup_database.fetchall(query)
    assert results == [(1, 2), (2, 3)]
    mock_database_connection['cursor'].execute.assert_called_once_with(query, [])
    mock_database_connection['cursor'].fetchall.assert_called_once()

# happy_path - commit - Commit changes to the database
def test_commit_changes(setup_database, mock_database_connection):
    setup_database.commit()
    mock_database_connection['connection'].commit.assert_called_once()

# happy_path - close - Close the database connection
def test_close_connection(setup_database, mock_database_connection):
    setup_database.close()
    mock_database_connection['connection'].close.assert_called_once()

# edge_case - add_item_to_cart_db - Handle SQL error when adding an item to cart
def test_add_item_to_cart_db_sql_error(setup_database, mock_database_connection):
    query = 'INSERT INTO cart (item_id, quantity) VALUES (?, ?)'
    params = (1, 2)
    mock_database_connection['cursor'].execute.side_effect = sqlite3.Error('SQL error')
    with pytest.raises(sqlite3.Error):
        add_item_to_cart_db(query, params) 
    mock_database_connection['cursor'].execute.assert_called_once_with(query, params)
    mock_database_connection['connection'].commit.assert_not_called()

# edge_case - fetchone - Handle case when fetchone returns None
def test_fetch_one_item_none(setup_database, mock_database_connection):
    query = 'SELECT * FROM cart WHERE item_id = ?'
    params = (999,)
    mock_database_connection['cursor'].fetchone.return_value = None
    result = setup_database.fetchone(query, params)
    assert result is None
    mock_database_connection['cursor'].execute.assert_called_once_with(query, params)
    mock_database_connection['cursor'].fetchone.assert_called_once()

# edge_case - fetchall - Handle case when fetchall returns an empty list
def test_fetch_all_items_empty(setup_database, mock_database_connection):
    query = 'SELECT * FROM cart'
    mock_database_connection['cursor'].fetchall.return_value = []
    results = setup_database.fetchall(query)
    assert results == []
    mock_database_connection['cursor'].execute.assert_called_once_with(query, [])
    mock_database_connection['cursor'].fetchall.assert_called_once()

# edge_case - commit - Handle commit error
def test_commit_changes_error(setup_database, mock_database_connection):
    mock_database_connection['connection'].commit.side_effect = sqlite3.Error('Commit error')
    with pytest.raises(sqlite3.Error):
        setup_database.commit()
    mock_database_connection['connection'].commit.assert_called_once()

# edge_case - close - Close connection when it is already closed
def test_close_connection_when_already_closed(setup_database, mock_database_connection):
    setup_database.close()
    setup_database.close()  # Call close again
    mock_database_connection['connection'].close.assert_called_once()

