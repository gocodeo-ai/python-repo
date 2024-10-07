import pytest
from unittest import mock
from shopping_cart.cart import Item, Cart
from shopping_cart.database import add_item_to_cart_db

@pytest.fixture
def cart():
    # Create a Cart instance for testing
    return Cart(user_type='regular')

@pytest.fixture
def mock_add_item_to_cart_db():
    with mock.patch('shopping_cart.database.add_item_to_cart_db') as mock_db:
        yield mock_db

@pytest.fixture
def mock_item():
    with mock.patch('shopping_cart.cart.Item') as mock_item_class:
        yield mock_item_class

@pytest.fixture
def setup_cart_with_item(cart, mock_add_item_to_cart_db):
    # Add an item to the cart
    item_id = 1
    quantity = 2
    price = 10.0
    name = 'Apple'
    category = 'Fruit'
    user_type = 'regular'
    
    cart.add_item(item_id, quantity, price, name, category, user_type)
    
    return cart

# happy_path - add_item - Test that adding an item to the cart updates the cart items list and database correctly.
def test_add_item_happy_path(cart, mock_add_item_to_cart_db):
    item_id = 1
    quantity = 2
    price = 10.0
    name = 'Apple'
    category = 'Fruit'
    user_type = 'regular'
    
    cart.add_item(item_id, quantity, price, name, category, user_type)
    
    assert cart.items == [{'item_id': 1, 'quantity': 2, 'price': 10.0, 'name': 'Apple', 'category': 'Fruit', 'user_type': 'regular'}]
    mock_add_item_to_cart_db.assert_called_once_with("INSERT INTO cart (item_id, quantity, price, name, category, user_type) VALUES (1, 2, 10.0, 'Apple', 'Fruit', 'regular')")

# happy_path - remove_item - Test that removing an item from the cart updates the cart items list and database correctly.
def test_remove_item_happy_path(setup_cart_with_item, mock_add_item_to_cart_db):
    cart = setup_cart_with_item
    item_id = 1
    
    cart.remove_item(item_id)
    
    assert cart.items == []
    mock_add_item_to_cart_db.assert_called_with('DELETE FROM cart WHERE item_id = 1')

# happy_path - update_item_quantity - Test that updating an item's quantity in the cart updates the cart items list and database correctly.
def test_update_item_quantity_happy_path(setup_cart_with_item, mock_add_item_to_cart_db):
    cart = setup_cart_with_item
    item_id = 1
    new_quantity = 5
    
    cart.update_item_quantity(item_id, new_quantity)
    
    assert cart.items == [{'item_id': 1, 'quantity': 5, 'price': 10.0, 'name': 'Apple', 'category': 'Fruit', 'user_type': 'regular'}]
    mock_add_item_to_cart_db.assert_called_with('UPDATE cart SET quantity = 5 WHERE item_id = 1')

# happy_path - calculate_total_price - Test that calculating total price returns the correct total for all items in the cart.
def test_calculate_total_price_happy_path(setup_cart_with_item):
    cart = setup_cart_with_item
    
    total_price = cart.calculate_total_price()
    
    assert total_price == 20.0

# happy_path - list_items - Test that listing items in the cart outputs the correct details for each item.
def test_list_items_happy_path(setup_cart_with_item, capsys):
    cart = setup_cart_with_item
    
    cart.list_items()
    captured = capsys.readouterr()
    assert captured.out == 'Item: Apple, Quantity: 2, Price per unit: 10.0\n'

# happy_path - empty_cart - Test that emptying the cart clears the items list and database correctly.
def test_empty_cart_happy_path(setup_cart_with_item, mock_add_item_to_cart_db):
    cart = setup_cart_with_item
    
    cart.empty_cart()
    
    assert cart.items == []
    mock_add_item_to_cart_db.assert_called_with('DELETE FROM cart')

# edge_case - add_item - Test that adding an item with zero quantity does not update the cart items list or database.
def test_add_item_zero_quantity_edge_case(cart, mock_add_item_to_cart_db):
    item_id = 2
    quantity = 0
    price = 15.0
    name = 'Banana'
    category = 'Fruit'
    user_type = 'guest'
    
    cart.add_item(item_id, quantity, price, name, category, user_type)
    
    assert cart.items == []
    mock_add_item_to_cart_db.assert_not_called()

# edge_case - remove_item - Test that removing an item not in the cart does not affect the cart items list or database.
def test_remove_item_not_in_cart_edge_case(cart, mock_add_item_to_cart_db):
    item_id = 3
    
    cart.remove_item(item_id)
    
    assert cart.items == []
    mock_add_item_to_cart_db.assert_not_called()

# edge_case - update_item_quantity - Test that updating an item's quantity to zero removes it from the cart and updates the database correctly.
def test_update_item_quantity_to_zero_edge_case(setup_cart_with_item, mock_add_item_to_cart_db):
    cart = setup_cart_with_item
    item_id = 1
    new_quantity = 0
    
    cart.update_item_quantity(item_id, new_quantity)
    
    assert cart.items == []
    mock_add_item_to_cart_db.assert_called_with('UPDATE cart SET quantity = 0 WHERE item_id = 1')

# edge_case - calculate_total_price - Test that calculating total price for an empty cart returns zero.
def test_calculate_total_price_empty_cart_edge_case(cart):
    total_price = cart.calculate_total_price()
    
    assert total_price == 0.0

# edge_case - list_items - Test that listing items in an empty cart outputs no item details.
def test_list_items_empty_cart_edge_case(cart, capsys):
    cart.list_items()
    captured = capsys.readouterr()
    assert captured.out == ''

# edge_case - empty_cart - Test that emptying an already empty cart does not affect the cart items list or database.
def test_empty_cart_already_empty_edge_case(cart, mock_add_item_to_cart_db):
    cart.empty_cart()
    
    assert cart.items == []
    mock_add_item_to_cart_db.assert_called_with('DELETE FROM cart')

