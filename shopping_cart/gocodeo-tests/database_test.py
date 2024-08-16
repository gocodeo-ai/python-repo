# happy_path - add_item_to_cart_db - Add an item to the cart database successfully
def test_add_item_to_cart_db(mock_database_connection, mock_os_path):
    query = 'INSERT INTO cart (item) VALUES (?)'
    params = ('apple',)
    add_item_to_cart_db(query, params)
    mock_database_connection.execute.assert_called_once_with(query, params)
    mock_database_connection.commit.assert_called_once()

# edge_case - add_item_to_cart_db - Attempt to add an item with a None parameter
def test_add_item_to_cart_db_with_none_params(mock_database_connection, mock_os_path):
    query = 'INSERT INTO cart (item) VALUES (?)'
    add_item_to_cart_db(query)
    mock_database_connection.execute.assert_called_once_with(query, [])
    mock_database_connection.commit.assert_called_once()

