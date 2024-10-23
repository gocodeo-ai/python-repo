import pytest
from unittest.mock import patch, MagicMock
from shopping_cart.cart import Cart, Item
from shopping_cart.database import add_item_to_cart_db

@pytest.fixture
def cart_setup():
    with patch('shopping_cart.database.add_item_to_cart_db') as mock_add_item_to_cart_db:
        mock_add_item_to_cart_db.return_value = None
        
        cart = Cart(user_type='regular')
        yield cart, mock_add_item_to_cart_db

@pytest.fixture
def item_setup():
    return Item(item_id=1, price=10.0, name='Test Item', category='Test Category')

# happy path - add_item - Test adding a single item to the cart successfully
def test_add_single_item_successfully(cart_setup):
    cart, mock_add_item_to_cart_db = cart_setup
    cart.add_item(item_id=1, quantity=2, price=10.0, name='Test Item', category='Fashion', user_type='regular')
    assert cart.items == [{'item_id': 1, 'quantity': 2, 'price': 10.0, 'name': 'Test Item', 'category': 'Fashion', 'user_type': 'prime_member'}]
    mock_add_item_to_cart_db.assert_called_once()


# happy path - remove_item - Test removing an item from the cart successfully
def test_remove_item_successfully(cart_setup, item_setup):
    cart, mock_add_item_to_cart_db = cart_setup
    cart.add_item(item_id=1, quantity=2, price=10.0, name='Test Item', category='Test Category', user_type='regular')
    cart.remove_item(item_id=1)
    assert cart.items == []
    assert mock_add_item_to_cart_db.call_count == 2


# happy path - update_item_quantity - Test updating the quantity of an item in the cart successfully
def test_update_item_quantity_successfully(cart_setup, item_setup):
    cart, mock_add_item_to_cart_db = cart_setup
    cart.add_item(item_id=1, quantity=2, price=10.0, name='Test Item', category='Test Category', user_type='regular')
    cart.update_item_quantity(item_id=1, new_quantity=5)
    assert cart.items == [{'item_id': 1, 'quantity': 5, 'price': 10.0, 'name': 'Test Item', 'category': 'Test Category', 'user_type': 'regular'}]
    assert mock_add_item_to_cart_db.call_count == 2


# happy path - calculate_total_price - Test calculating total price of items in the cart
def test_calculate_total_price(cart_setup, item_setup):
    cart, mock_add_item_to_cart_db = cart_setup
    cart.add_item(item_id=1, quantity=2, price=10.0, name='Test Item', category='Test Category', user_type='regular')
    total_price = cart.calculate_total_price()
    assert total_price == 20.0
    mock_add_item_to_cart_db.assert_called_once()


# happy path - list_items - Test listing items in the cart
def test_list_items(cart_setup, item_setup, capsys):
    cart, mock_add_item_to_cart_db = cart_setup
    cart.add_item(item_id=1, quantity=2, price=10.0, name='Test Item', category='Test Category', user_type='regular')
    cart.list_items()
    captured = capsys.readouterr()
    assert captured.out.strip() == "Item: Test Item, Quantity: 2, Price per unit: 10.0"
    mock_add_item_to_cart_db.assert_called_once()


# happy path - empty_cart - Test emptying the cart successfully
def test_empty_cart_successfully(cart_setup, item_setup):
    cart, mock_add_item_to_cart_db = cart_setup
    cart.add_item(item_id=1, quantity=2, price=10.0, name='Test Item', category='Test Category', user_type='regular')
    cart.empty_cart()
    assert cart.items == []
    assert mock_add_item_to_cart_db.call_count == 2


# edge case - add_item - Test adding an item with zero quantity
def test_add_item_with_zero_quantity(cart_setup):
    cart, mock_add_item_to_cart_db = cart_setup
    cart.add_item(item_id=2, quantity=0, price=10.0, name='Zero Quantity Item', category='Test Category', user_type='regular')
    assert cart.items == [{'item_id': 2, 'quantity': 0, 'price': 10.0, 'name': 'Zero Quantity Item', 'category': 'Test Category', 'user_type': 'regular'}]
    mock_add_item_to_cart_db.assert_called_once()


# edge case - remove_item - Test removing an item not present in the cart
def test_remove_nonexistent_item(cart_setup, item_setup):
    cart, mock_add_item_to_cart_db = cart_setup
    cart.add_item(item_id=1, quantity=2, price=10.0, name='Test Item', category='Test Category', user_type='regular')
    cart.remove_item(item_id=99)
    assert cart.items == [{'item_id': 1, 'quantity': 2, 'price': 10.0, 'name': 'Test Item', 'category': 'Test Category', 'user_type': 'regular'}]
    assert mock_add_item_to_cart_db.call_count == 2


# edge case - update_item_quantity - Test updating quantity of an item not present in the cart
def test_update_quantity_nonexistent_item(cart_setup, item_setup):
    cart, mock_add_item_to_cart_db = cart_setup
    cart.add_item(item_id=1, quantity=2, price=10.0, name='Test Item', category='Test Category', user_type='regular')
    cart.update_item_quantity(item_id=99, new_quantity=3)
    assert cart.items == [{'item_id': 1, 'quantity': 2, 'price': 10.0, 'name': 'Test Item', 'category': 'Test Category', 'user_type': 'regular'}]
    assert mock_add_item_to_cart_db.call_count == 2


# edge case - calculate_total_price - Test calculating total price with no items in the cart
def test_calculate_total_price_empty_cart(cart_setup):
    cart, mock_add_item_to_cart_db = cart_setup
    total_price = cart.calculate_total_price()
    assert total_price == 0.0
    mock_add_item_to_cart_db.assert_not_called()


# edge case - list_items - Test listing items when cart is empty
def test_list_items_empty_cart(cart_setup, capsys):
    cart, mock_add_item_to_cart_db = cart_setup
    cart.list_items()
    captured = capsys.readouterr()
    assert captured.out.strip() == ""
    mock_add_item_to_cart_db.assert_not_called()


# edge case - empty_cart - Test emptying an already empty cart
def test_empty_already_empty_cart(cart_setup):
    cart, mock_add_item_to_cart_db = cart_setup
    cart.empty_cart()
    assert cart.items == []
    mock_add_item_to_cart_db.assert_called_once()


