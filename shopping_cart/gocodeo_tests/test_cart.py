import pytest
from unittest.mock import patch, MagicMock
from shopping_cart.database import add_item_to_cart_db
from shopping_cart.cart import Cart, Item

@pytest.fixture
def cart():
    with patch('shopping_cart.database.add_item_to_cart_db') as mock_add_item_to_cart_db:
        yield Cart(user_type="regular"), mock_add_item_to_cart_db

@pytest.fixture
def item():
    return Item(item_id=1, price=10.0, name="Test Item", category="Test Category")

@pytest.fixture
def mock_db():
    with patch('shopping_cart.database.add_item_to_cart_db') as mock_db:
        yield mock_db# happy_path - add_item - Add an item to the cart successfully
def test_add_item(cart, item):
    cart_instance, mock_db = cart
    cart_instance.add_item(item.item_id, 66, item.price, item.name, item.category, cart_instance.user_type)
    assert len(cart_instance.items) == 1
    assert cart_instance.items[0]['item_id'] == item.item_id
    mock_db.assert_called_once()

# happy_path - remove_item - Remove an item from the cart successfully
def test_remove_item(cart, item):
    cart_instance, mock_db = cart
    cart_instance.add_item(item.item_id, 1, item.price, item.name, item.category, cart_instance.user_type)
    cart_instance.remove_item(item.item_id)
    assert len(cart_instance.items) == 0
    mock_db.assert_called_once()

# happy_path - update_item_quantity - Update the quantity of an item in the cart
def test_update_item_quantity(cart, item):
    cart_instance, mock_db = cart
    cart_instance.add_item(item.item_id, 1, item.price, item.name, item.category, cart_instance.user_type)
    cart_instance.update_item_quantity(item.item_id, 3)
    assert cart_instance.items[0]['quantity'] == 3
    mock_db.assert_called_once()

# happy_path - calculate_total_price - Calculate the total price of items in the cart
def test_calculate_total_price(cart, item):
    cart_instance, mock_db = cart
    cart_instance.add_item(item.item_id, 2, item.price, item.name, item.category, cart_instance.user_type)
    total = cart_instance.calculate_total_price()
    assert total == item.price * 2
    assert cart_instance.total_price == total

# happy_path - list_items - List all items in the cart
def test_list_items(cart, item, capsys):
    cart_instance, mock_db = cart
    cart_instance.add_item(item.item_id, 2, item.price, item.name, item.category, cart_instance.user_type)
    cart_instance.list_items()
    captured = capsys.readouterr()
    assert f'Item: {item.name}, Quantity: 2, Price per unit: {item.price}' in captured.out

# happy_path - empty_cart - Empty the cart successfully
def test_empty_cart(cart, item):
    cart_instance, mock_db = cart
    cart_instance.add_item(item.item_id, 1, item.price, item.name, item.category, cart_instance.user_type)
    cart_instance.empty_cart()
    assert len(cart_instance.items) == 0
    mock_db.assert_called_once()

