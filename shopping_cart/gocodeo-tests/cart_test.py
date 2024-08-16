# happy_path - add_item - Adding an item to the cart should add it to the items list and call the database function
def test_add_item(cart):
    cart_instance, mock_db = cart
    cart_instance.add_item(1, 2, 10.0, 'Apple', 'Fruit', 'regular')
    assert len(cart_instance.items) == 1
    assert cart_instance.items[0]['item_id'] == 1
    assert cart_instance.items[0]['quantity'] == 2
    assert cart_instance.items[0]['price'] == 10.0
    mock_db.assert_called_once()

# happy_path - remove_item - Removing an item should remove it from the items list and call the database function
def test_remove_item(cart):
    cart_instance, mock_db = cart
    cart_instance.add_item(1, 2, 10.0, 'Apple', 'Fruit', 'regular')
    cart_instance.remove_item(1)
    assert len(cart_instance.items) == 0
    mock_db.assert_called_once()

# happy_path - update_item_quantity - Updating item quantity should change the quantity of the item in the list and call the database function
def test_update_item_quantity(cart):
    cart_instance, mock_db = cart
    cart_instance.add_item(1, 2, 10.0, 'Apple', 'Fruit', 'regular')
    cart_instance.update_item_quantity(1, 5)
    assert cart_instance.items[0]['quantity'] == 5
    mock_db.assert_called_once()

# happy_path - calculate_total_price - Calculating total price should return the correct total based on item prices and quantities
def test_calculate_total_price(cart):
    cart_instance, mock_db = cart
    cart_instance.add_item(1, 2, 10.0, 'Apple', 'Fruit', 'regular')
    cart_instance.add_item(2, 1, 5.0, 'Banana', 'Fruit', 'regular')
    total = cart_instance.calculate_total_price()
    assert total == 25.0

# happy_path - list_items - Listing items should print the correct item details
def test_list_items(cart, capsys):
    cart_instance, mock_db = cart
    cart_instance.add_item(1, 2, 10.0, 'Apple', 'Fruit', 'regular')
    cart_instance.list_items()
    captured = capsys.readouterr()
    assert 'Item: Apple, Quantity: 2, Price per unit: 10.0' in captured.out

# happy_path - empty_cart - Emptying the cart should clear the items list and call the database function
def test_empty_cart(cart):
    cart_instance, mock_db = cart
    cart_instance.add_item(1, 2, 10.0, 'Apple', 'Fruit', 'regular')
    cart_instance.empty_cart()
    assert len(cart_instance.items) == 0
    mock_db.assert_called_once()

# edge_case - add_item_edge_case - Adding an item with zero quantity should not change the items list
def test_add_item_zero_quantity(cart):
    cart_instance, mock_db = cart
    cart_instance.add_item(1, 0, 10.0, 'Apple', 'Fruit', 'regular')
    assert len(cart_instance.items) == 0
    mock_db.assert_not_called()

# edge_case - remove_item_nonexistent - Removing an item that does not exist should not change the items list
def test_remove_nonexistent_item(cart):
    cart_instance, mock_db = cart
    cart_instance.add_item(1, 2, 10.0, 'Apple', 'Fruit', 'regular')
    cart_instance.remove_item(2)
    assert len(cart_instance.items) == 1
    mock_db.assert_called_once()

# edge_case - update_item_quantity_nonexistent - Updating quantity of an item that does not exist should not change the items list
def test_update_nonexistent_item_quantity(cart):
    cart_instance, mock_db = cart
    cart_instance.add_item(1, 2, 10.0, 'Apple', 'Fruit', 'regular')
    cart_instance.update_item_quantity(2, 5)
    assert cart_instance.items[0]['quantity'] == 2
    mock_db.assert_not_called()

# edge_case - calculate_total_price_empty_cart - Calculating total price on an empty cart should return 0
def test_calculate_total_price_empty(cart):
    cart_instance, mock_db = cart
    total = cart_instance.calculate_total_price()
    assert total == 0.0

# edge_case - empty_cart_when_already_empty - Emptying an already empty cart should not cause any errors
def test_empty_cart_when_already_empty(cart):
    cart_instance, mock_db = cart
    cart_instance.empty_cart()
    assert len(cart_instance.items) == 0
    mock_db.assert_called_once()

