import pytest
from unittest.mock import patch, MagicMock
from shopping_cart.cart import Item, Cart
from shopping_cart.database import add_item_to_cart_db

@pytest.fixture
def cart():
    return Cart(user_type='regular')

@pytest.fixture
def mock_add_item_to_cart_db():
    with patch('shopping_cart.database.add_item_to_cart_db') as mock:
        yield mock

@pytest.fixture
def mock_item():
    return Item(item_id=1, price=10.0, name='Apple', category='Fruit')

@pytest.fixture
def mock_cart_with_item(cart, mock_item):
    cart.add_item(mock_item.item_id, 2, mock_item.price, mock_item.name, mock_item.category, cart.user_type)
    return cart

# happy path - add_item - Test that item is added to the cart successfully
def test_add_item_success(cart, mock_add_item_to_cart_db, mock_item):
    cart.add_item(mock_item.item_id, 2, mock_item.price, mock_item.name, mock_item.category, cart.user_type)
    assert cart.items == [{'item_id': 1, 'quantity': 2, 'price': 10.0, 'name': 'Apple', 'category': 'Fruit', 'user_type': 'regular'}]
    mock_add_item_to_cart_db.assert_called_once()


# happy path - remove_item - Test that item is removed from the cart successfully
def test_remove_item_success(mock_cart_with_item, mock_add_item_to_cart_db):
    mock_cart_with_item.remove_item(1)
    assert mock_cart_with_item.items == []
    mock_add_item_to_cart_db.assert_called_once()


# happy path - update_item_quantity - Test that item quantity is updated successfully
def test_update_item_quantity_success(mock_cart_with_item, mock_add_item_to_cart_db):
    mock_cart_with_item.update_item_quantity(1, 5)
    assert mock_cart_with_item.items == [{'item_id': 1, 'quantity': 5, 'price': 10.0, 'name': 'Apple', 'category': 'Fruit', 'user_type': 'regular'}]
    mock_add_item_to_cart_db.assert_called_once()


# happy path - calculate_total_price - Test that total price is calculated correctly
def test_calculate_total_price_success(mock_cart_with_item):
    total_price = mock_cart_with_item.calculate_total_price()
    assert total_price == 20.0


# happy path - list_items - Test that items are listed correctly
def test_list_items_success(mock_cart_with_item, capsys):
    mock_cart_with_item.list_items()
    captured = capsys.readouterr()
    assert 'Item: Apple, Quantity: 2, Price per unit: 10.0' in captured.out


# happy path - empty_cart - Test that cart is emptied successfully
def test_empty_cart_success(mock_cart_with_item, mock_add_item_to_cart_db):
    mock_cart_with_item.empty_cart()
    assert mock_cart_with_item.items == []
    mock_add_item_to_cart_db.assert_called_once()


# edge case - add_item - Test adding item with zero quantity
def test_add_item_zero_quantity(cart, mock_add_item_to_cart_db):
    cart.add_item(2, 0, 15.0, 'Banana', 'Fruit', 'guest')
    assert cart.items == [{'item_id': 2, 'quantity': 0, 'price': 15.0, 'name': 'Banana', 'category': 'Fruit', 'user_type': 'guest'}]
    mock_add_item_to_cart_db.assert_called_once()


# edge case - remove_item - Test removing item not in cart
def test_remove_item_not_in_cart(cart, mock_add_item_to_cart_db):
    cart.remove_item(99)
    assert cart.items == []
    mock_add_item_to_cart_db.assert_called_once()


# edge case - update_item_quantity - Test updating quantity of item not in cart
def test_update_item_quantity_not_in_cart(cart, mock_add_item_to_cart_db):
    cart.update_item_quantity(99, 3)
    assert cart.items == []
    mock_add_item_to_cart_db.assert_called_once()


# edge case - calculate_total_price - Test calculating total price with no items
def test_calculate_total_price_no_items(cart):
    total_price = cart.calculate_total_price()
    assert total_price == 0.0


# edge case - list_items - Test listing items when cart is empty
def test_list_items_empty_cart(cart, capsys):
    cart.list_items()
    captured = capsys.readouterr()
    assert captured.out == ''


# edge case - empty_cart - Test emptying an already empty cart
def test_empty_cart_already_empty(cart, mock_add_item_to_cart_db):
    cart.empty_cart()
    assert cart.items == []
    mock_add_item_to_cart_db.assert_called_once()


