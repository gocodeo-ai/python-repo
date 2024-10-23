import pytest
from unittest.mock import patch, MagicMock
from shopping_cart.cart import Cart, Item
from shopping_cart.database import add_item_to_cart_db

@pytest.fixture
def mock_cart():
    with patch('shopping_cart.database.add_item_to_cart_db') as mock_db:
        mock_db.return_value = None
        cart = Cart(user_type='regular')
        yield cart

@pytest.fixture
def mock_item():
    with patch('shopping_cart.cart.Item') as mock_item_class:
        mock_item_instance = MagicMock()
        mock_item_class.return_value = mock_item_instance
        yield mock_item_instance

# happy path - add_item - Test that an item is added to the cart with correct details
def test_add_item(mock_cart):
    mock_cart.add_item(1, 2, 10.0, 'Apple', 'Fruit', 'regular')
    assert mock_cart.items == [{'item_id': 1, 'quantity': 2, 'price': 10.0, 'name': 'Apple', 'category': 'Fruit', 'user_type': 'regular'}]


# happy path - remove_item - Test that an item is removed from the cart successfully
def test_remove_item(mock_cart):
    mock_cart.add_item(1, 2, 10.0, 'Apple', 'Fruit', 'regular')
    mock_cart.remove_item(1)
    assert mock_cart.items == []


# happy path - update_item_quantity - Test that item quantity is updated correctly in the cart
def test_update_item_quantity(mock_cart):
    mock_cart.add_item(1, 2, 10.0, 'Apple', 'Fruit', 'regular')
    mock_cart.update_item_quantity(1, 5)
    assert mock_cart.items == [{'item_id': 1, 'quantity': 5, 'price': 10.0, 'name': 'Apple', 'category': 'Fruit', 'user_type': 'regular'}]


# happy path - calculate_total_price - Test that total price is calculated correctly
def test_calculate_total_price(mock_cart):
    mock_cart.add_item(1, 2, 10.0, 'Apple', 'Fruit', 'regular')
    total_price = mock_cart.calculate_total_price()
    assert total_price == 20.0


# happy path - list_items - Test that listing items shows correct details
def test_list_items(mock_cart, capsys):
    mock_cart.add_item(1, 2, 10.0, 'Apple', 'Fruit', 'regular')
    mock_cart.list_items()
    captured = capsys.readouterr()
    assert captured.out == 'Item: Apple, Quantity: 2, Price per unit: 10.0\n'


# happy path - empty_cart - Test that cart is emptied successfully
def test_empty_cart(mock_cart):
    mock_cart.add_item(1, 2, 10.0, 'Apple', 'Fruit', 'regular')
    mock_cart.empty_cart()
    assert mock_cart.items == []


# edge case - add_item - Test adding an item with zero quantity
def test_add_item_zero_quantity(mock_cart):
    mock_cart.add_item(2, 0, 5.0, 'Banana', 'Fruit', 'guest')
    assert mock_cart.items == [{'item_id': 2, 'quantity': 0, 'price': 5.0, 'name': 'Banana', 'category': 'Fruit', 'user_type': 'guest'}]


# edge case - remove_item - Test removing an item that does not exist in the cart
def test_remove_nonexistent_item(mock_cart):
    mock_cart.remove_item(99)
    assert mock_cart.items == []


# edge case - update_item_quantity - Test updating quantity of an item that does not exist
def test_update_nonexistent_item_quantity(mock_cart):
    mock_cart.update_item_quantity(99, 3)
    assert mock_cart.items == []


# edge case - calculate_total_price - Test calculating total price of an empty cart
def test_calculate_total_price_empty_cart(mock_cart):
    total_price = mock_cart.calculate_total_price()
    assert total_price == 0.0


# edge case - list_items - Test listing items in an empty cart
def test_list_items_empty_cart(mock_cart, capsys):
    mock_cart.list_items()
    captured = capsys.readouterr()
    assert captured.out == ''


# edge case - empty_cart - Test emptying an already empty cart
def test_empty_already_empty_cart(mock_cart):
    mock_cart.empty_cart()
    assert mock_cart.items == []


