# happy_path - add_item - Add an item to the cart successfully
def test_add_item(cart):
    cart.add_item(1, 2, 10.0, 'Apple', 'Fruit', 'regular')
    assert len(cart.items) == 1
    assert cart.items[0]['item_id'] == 1
    assert cart.items[0]['quantity'] == 2
    assert cart.items[0]['price'] == 10.0
    assert cart.items[0]['name'] == 'Apple'
    assert cart.items[0]['category'] == 'Fruit'
    assert cart.items[0]['user_type'] == 'regular'

# happy_path - remove_item - Remove an item from the cart successfully
def test_remove_item(cart):
    cart.add_item(1, 2, 10.0, 'Apple', 'Fruit', 'regular')
    cart.remove_item(1)
    assert len(cart.items) == 0

# happy_path - update_item_quantity - Update the quantity of an existing item
def test_update_item_quantity(cart):
    cart.add_item(1, 2, 10.0, 'Apple', 'Fruit', 'regular')
    cart.update_item_quantity(1, 5)
    assert cart.items[0]['quantity'] == 5

# happy_path - calculate_total_price - Calculate total price of items in the cart
def test_calculate_total_price(cart):
    cart.add_item(1, 2, 10.0, 'Apple', 'Fruit', 'regular')
    cart.add_item(2, 1, 20.0, 'Banana', 'Fruit', 'regular')
    total = cart.calculate_total_price()
    assert total == 50.0

# happy_path - list_items - List items in the cart
def test_list_items(cart, capsys):
    cart.add_item(1, 2, 10.0, 'Apple', 'Fruit', 'regular')
    cart.list_items()
    captured = capsys.readouterr()
    assert 'Item: Apple, Quantity: 2, Price per unit: 10.0' in captured.out

# happy_path - empty_cart - Empty the cart successfully
def test_empty_cart(cart):
    cart.add_item(1, 2, 10.0, 'Apple', 'Fruit', 'regular')
    cart.empty_cart()
    assert len(cart.items) == 0

# edge_case - add_item - Add an item with zero quantity
def test_add_item_zero_quantity(cart):
    cart.add_item(1, 0, 10.0, 'Apple', 'Fruit', 'regular')
    assert len(cart.items) == 1
    assert cart.items[0]['quantity'] == 0

# edge_case - remove_item - Remove an item that does not exist
def test_remove_non_existing_item(cart):
    cart.add_item(1, 2, 10.0, 'Apple', 'Fruit', 'regular')
    cart.remove_item(2)
    assert len(cart.items) == 1

# edge_case - update_item_quantity - Update quantity of an item that does not exist
def test_update_quantity_non_existing_item(cart):
    cart.add_item(1, 2, 10.0, 'Apple', 'Fruit', 'regular')
    cart.update_item_quantity(2, 5)
    assert cart.items[0]['quantity'] == 2

# edge_case - calculate_total_price - Calculate total price with no items
def test_calculate_total_price_empty(cart):
    total = cart.calculate_total_price()
    assert total == 0.0

# edge_case - list_items - List items in an empty cart
def test_list_items_empty(cart, capsys):
    cart.list_items()
    captured = capsys.readouterr()
    assert captured.out == ''

# edge_case - empty_cart - Empty an already empty cart
def test_empty_cart_already_empty(cart):
    cart.empty_cart()
    assert len(cart.items) == 0

