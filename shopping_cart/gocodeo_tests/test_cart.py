import pytest
from unittest.mock import patch, MagicMock
from shopping_cart.cart import Item, Cart
from shopping_cart.database import add_item_to_cart_db

@pytest.fixture
def cart_setup():
    with patch('shopping_cart.database.add_item_to_cart_db') as mock_add_item_to_cart_db:
        mock_add_item_to_cart_db.return_value = None
        
        cart = Cart(user_type='regular')
        item = Item(item_id=1, price=10.0, name='Apple', category='Fruit')
        
        yield {
            'cart': cart,
            'item': item,
            'mock_add_item_to_cart_db': mock_add_item_to_cart_db
        }

# happy_path - test_add_item - Test that adding an item updates the items list and calls the database function with correct query.
def test_add_item(cart_setup):
    cart = cart_setup['cart']
    mock_add_item_to_cart_db = cart_setup['mock_add_item_to_cart_db']
    cart.add_item(item_id=1, quantity=2, price=10.0, name='Apple', category='Fruit', user_type='regular')
    assert cart.items == [{'item_id': 1, 'quantity': 2, 'price': 10.0, 'name': 'Apple', 'category': 'Fruit', 'user_type': 'regular'}]
    mock_add_item_to_cart_db.assert_called_once_with("INSERT INTO cart (item_id, quantity, price, name, category, user_type) VALUES (1, 2, 10.0, 'Apple', 'Fruit', 'regular')")

# happy_path - test_remove_item - Test that removing an item updates the items list and calls the database function with correct query.
def test_remove_item(cart_setup):
    cart = cart_setup['cart']
    mock_add_item_to_cart_db = cart_setup['mock_add_item_to_cart_db']
    cart.add_item(item_id=1, quantity=2, price=10.0, name='Apple', category='Fruit', user_type='regular')
    cart.remove_item(item_id=1)
    assert cart.items == []
    mock_add_item_to_cart_db.assert_any_call('DELETE FROM cart WHERE item_id = 1')

# happy_path - test_update_item_quantity - Test that updating item quantity changes the quantity in items list and calls the database function with correct query.
def test_update_item_quantity(cart_setup):
    cart = cart_setup['cart']
    mock_add_item_to_cart_db = cart_setup['mock_add_item_to_cart_db']
    cart.add_item(item_id=1, quantity=2, price=10.0, name='Apple', category='Fruit', user_type='regular')
    cart.update_item_quantity(item_id=1, new_quantity=5)
    assert cart.items == [{'item_id': 1, 'quantity': 5, 'price': 10.0, 'name': 'Apple', 'category': 'Fruit', 'user_type': 'regular'}]
    mock_add_item_to_cart_db.assert_any_call('UPDATE cart SET quantity = 5 WHERE item_id = 1')

# happy_path - test_calculate_total_price - Test that calculating total price returns the correct total for items in the cart.
def test_calculate_total_price(cart_setup):
    cart = cart_setup['cart']
    cart.add_item(item_id=1, quantity=2, price=10.0, name='Apple', category='Fruit', user_type='regular')
    total_price = cart.calculate_total_price()
    assert total_price == 20.0

# happy_path - test_list_items - Test that listing items prints the correct details of each item in the cart.
def test_list_items(cart_setup, capsys):
    cart = cart_setup['cart']
    cart.add_item(item_id=1, quantity=2, price=10.0, name='Apple', category='Fruit', user_type='regular')
    cart.list_items()
    captured = capsys.readouterr()
    assert captured.out == 'Item: Apple, Quantity: 2, Price per unit: 10.0\n'

# happy_path - test_empty_cart - Test that emptying the cart clears the items list and calls the database function with correct query.
def test_empty_cart(cart_setup):
    cart = cart_setup['cart']
    mock_add_item_to_cart_db = cart_setup['mock_add_item_to_cart_db']
    cart.add_item(item_id=1, quantity=2, price=10.0, name='Apple', category='Fruit', user_type='regular')
    cart.empty_cart()
    assert cart.items == []
    mock_add_item_to_cart_db.assert_any_call('DELETE FROM cart')

# edge_case - test_add_item_zero_quantity - Test that adding an item with zero quantity does not add it to the cart.
def test_add_item_zero_quantity(cart_setup):
    cart = cart_setup['cart']
    mock_add_item_to_cart_db = cart_setup['mock_add_item_to_cart_db']
    cart.add_item(item_id=2, quantity=0, price=15.0, name='Banana', category='Fruit', user_type='regular')
    assert cart.items == []
    mock_add_item_to_cart_db.assert_called_once_with("INSERT INTO cart (item_id, quantity, price, name, category, user_type) VALUES (2, 0, 15.0, 'Banana', 'Fruit', 'regular')")

# edge_case - test_remove_non_existing_item - Test that removing an item not in the cart does not affect the items list.
def test_remove_non_existing_item(cart_setup):
    cart = cart_setup['cart']
    mock_add_item_to_cart_db = cart_setup['mock_add_item_to_cart_db']
    cart.add_item(item_id=1, quantity=2, price=10.0, name='Apple', category='Fruit', user_type='regular')
    cart.remove_item(item_id=3)
    assert cart.items == [{'item_id': 1, 'quantity': 2, 'price': 10.0, 'name': 'Apple', 'category': 'Fruit', 'user_type': 'regular'}]
    mock_add_item_to_cart_db.assert_any_call('DELETE FROM cart WHERE item_id = 3')

# edge_case - test_update_quantity_non_existing_item - Test that updating quantity for an item not in the cart does not affect the items list.
def test_update_quantity_non_existing_item(cart_setup):
    cart = cart_setup['cart']
    mock_add_item_to_cart_db = cart_setup['mock_add_item_to_cart_db']
    cart.add_item(item_id=1, quantity=2, price=10.0, name='Apple', category='Fruit', user_type='regular')
    cart.update_item_quantity(item_id=3, new_quantity=3)
    assert cart.items == [{'item_id': 1, 'quantity': 2, 'price': 10.0, 'name': 'Apple', 'category': 'Fruit', 'user_type': 'regular'}]
    mock_add_item_to_cart_db.assert_any_call('UPDATE cart SET quantity = 3 WHERE item_id = 3')

# edge_case - test_calculate_total_price_empty_cart - Test that calculating total price with an empty cart returns zero.
def test_calculate_total_price_empty_cart(cart_setup):
    cart = cart_setup['cart']
    total_price = cart.calculate_total_price()
    assert total_price == 0.0

# edge_case - test_list_items_empty_cart - Test that listing items with an empty cart prints nothing.
def test_list_items_empty_cart(cart_setup, capsys):
    cart = cart_setup['cart']
    cart.list_items()
    captured = capsys.readouterr()
    assert captured.out == ''

# edge_case - test_empty_already_empty_cart - Test that emptying an already empty cart does not cause errors.
def test_empty_already_empty_cart(cart_setup):
    cart = cart_setup['cart']
    mock_add_item_to_cart_db = cart_setup['mock_add_item_to_cart_db']
    cart.empty_cart()
    assert cart.items == []
    mock_add_item_to_cart_db.assert_called_once_with('DELETE FROM cart')

