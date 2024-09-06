import pytest
from unittest.mock import Mock, patch
from shopping_cart.cart import Item, Cart
from shopping_cart.database import add_item_to_cart_db

@pytest.fixture
def mock_add_item_to_cart_db():
    with patch('shopping_cart.cart.add_item_to_cart_db') as mock:
        yield mock

@pytest.fixture
def cart():
    return Cart("Regular")

@pytest.fixture
def item():
    return Item(1, 10.99, "Test Item", "Gadgets")

@pytest.fixture
def mock_print():
    with patch('builtins.print') as mock_print:
        yield mock_print

@pytest.fixture
def mock_cart():
    with patch('shopping_cart.cart.Cart') as mock_cart:
        cart_instance = mock_cart.return_value
        cart_instance.items = []
        cart_instance.user_type = "Regular"
        cart_instance.payment_status = ""
        cart_instance.total_price = 0
        cart_instance.add_item = Mock()
        cart_instance.remove_item = Mock()
        cart_instance.update_item_quantity = Mock()
        cart_instance.calculate_total_price = Mock(return_value=0)
        cart_instance.list_items = Mock()
        cart_instance.empty_cart = Mock()
        yield cart_instance

@pytest.fixture
def mock_item():
    with patch('shopping_cart.cart.Item') as mock_item:
        item_instance = mock_item.return_value
        item_instance.item_id = 1
        item_instance.price = 10.99
        item_instance.name = "Test Item"
        item_instance.category = "Electronics"
        yield item_instance

# happy path - remove_item - Generate test cases on removing an item from the cart successfully
def test_remove_item_success(cart, mock_add_item_to_cart_db):
    cart.items = [{'item_id': 1, 'quantity': 2, 'price': 10.99, 'name': 'Test Item', 'category': 'Electronics', 'user_type': 'Regular'}]
    cart.remove_item(1)
    assert len(cart.items) == 0
    mock_add_item_to_cart_db.assert_called_once_with('DELETE FROM cart WHERE item_id = 1')

# happy path - update_item_quantity - Generate test cases on updating item quantity in the cart successfully
def test_update_item_quantity_success(cart, mock_add_item_to_cart_db):
    cart.items = [{'item_id': 1, 'quantity': 2, 'price': 10.99, 'name': 'Test Item', 'category': 'Electronics', 'user_type': 'Regular'}]
    cart.update_item_quantity(1, 5)
    assert cart.items[0]['quantity'] == 5
    mock_add_item_to_cart_db.assert_called_once_with('UPDATE cart SET quantity = 5 WHERE item_id = 1')

# happy path - calculate_total_price - Generate test cases on calculating total price correctly
def test_calculate_total_price(cart):
    cart.items = [
        {'item_id': 1, 'quantity': 2, 'price': 10.99, 'name': 'Test Item 1', 'category': 'Electronics', 'user_type': 'Regular'},
        {'item_id': 2, 'quantity': 1, 'price': 5.99, 'name': 'Test Item 2', 'category': 'Books', 'user_type': 'Regular'}
    ]
    total_price = cart.calculate_total_price()
    assert total_price == pytest.approx(27.97, 0.01)
    assert cart.total_price == pytest.approx(27.97, 0.01)

# happy path - list_items - Generate test cases on listing items in the cart successfully
def test_list_items(cart, mock_print):
    cart.items = [
        {'item_id': 1, 'quantity': 2, 'price': 10.99, 'name': 'Test Item 1', 'category': 'Electronics', 'user_type': 'Regular'},
        {'item_id': 2, 'quantity': 1, 'price': 5.99, 'name': 'Test Item 2', 'category': 'Books', 'user_type': 'Regular'}
    ]
    cart.list_items()
    mock_print.assert_any_call('Item: Test Item 1, Quantity: 2, Price per unit: 10.99')
    mock_print.assert_any_call('Item: Test Item 2, Quantity: 1, Price per unit: 5.99')

# happy path - empty_cart - Generate test cases on emptying the cart successfully
def test_empty_cart(cart, mock_add_item_to_cart_db):
    cart.items = [
        {'item_id': 1, 'quantity': 2, 'price': 10.99, 'name': 'Test Item 1', 'category': 'Electronics', 'user_type': 'Regular'},
        {'item_id': 2, 'quantity': 1, 'price': 5.99, 'name': 'Test Item 2', 'category': 'Books', 'user_type': 'Regular'}
    ]
    cart.empty_cart()
    assert len(cart.items) == 0
    mock_add_item_to_cart_db.assert_called_once_with('DELETE FROM cart')

# edge case - add_item - Generate test cases on adding an item with zero quantity
def test_add_item_zero_quantity(cart, mock_add_item_to_cart_db):
    cart.add_item(1, 0, 10.99, 'Test Item', 'Electronics', 'Regular')
    assert len(cart.items) == 0
    mock_add_item_to_cart_db.assert_not_called()

# edge case - remove_item - Generate test cases on removing a non-existent item from the cart
def test_remove_nonexistent_item(cart, mock_add_item_to_cart_db):
    cart.items = [{'item_id': 1, 'quantity': 2, 'price': 10.99, 'name': 'Test Item', 'category': 'Electronics', 'user_type': 'Regular'}]
    cart.remove_item(999)
    assert len(cart.items) == 1
    mock_add_item_to_cart_db.assert_called_once_with('DELETE FROM cart WHERE item_id = 999')

# edge case - update_item_quantity - Generate test cases on updating quantity for a non-existent item
def test_update_nonexistent_item_quantity(cart, mock_add_item_to_cart_db):
    cart.items = [{'item_id': 1, 'quantity': 2, 'price': 10.99, 'name': 'Test Item', 'category': 'Electronics', 'user_type': 'Regular'}]
    cart.update_item_quantity(999, 5)
    assert len(cart.items) == 1
    assert cart.items[0]['quantity'] == 2
    mock_add_item_to_cart_db.assert_called_once_with('UPDATE cart SET quantity = 5 WHERE item_id = 999')

# edge case - calculate_total_price - Generate test cases on calculating total price for an empty cart
def test_calculate_total_price_empty_cart(cart):
    assert cart.calculate_total_price() == 0
    assert cart.total_price == 0

# edge case - list_items - Generate test cases on listing items for an empty cart
def test_list_items_empty_cart(cart, mock_print):
    cart.list_items()
    mock_print.assert_not_called()

# edge case - empty_cart - Generate test cases on emptying an already empty cart
def test_empty_already_empty_cart(cart, mock_add_item_to_cart_db):
    cart.empty_cart()
    assert len(cart.items) == 0
    mock_add_item_to_cart_db.assert_called_once_with('DELETE FROM cart')

