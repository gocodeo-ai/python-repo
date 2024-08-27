import pytest
from unittest.mock import patch
from shopping_cart.database import add_item_to_cart_db
from your_module import Cart, Item

@pytest.fixture
def cart():
    with patch('your_module.add_item_to_cart_db') as mock_db:
        cart = Cart(user_type="regular")
        yield cart, mock_db

@pytest.fixture
def item():
    return Item(item_id=1, price=100, name="Test Item", category="Test Category")

# happy_path - test_add_item_happy_path - Test adding an item to the cart with valid details
def test_add_item_happy_path(cart, item):
    cart_instance, mock_db = cart
    cart_instance.add_item(item.item_id, 2, item.price, item.name, item.category, cart_instance.user_type)
    assert len(cart_instance.items) == 1
    assert cart_instance.items[0]['item_id'] == item.item_id
    mock_db.assert_called_once()

# happy_path - test_remove_item_happy_path - Test removing an item from the cart that exists
def test_remove_item_happy_path(cart, item):
    cart_instance, mock_db = cart
    cart_instance.add_item(item.item_id, 2, item.price, item.name, item.category, cart_instance.user_type)
    cart_instance.remove_item(item.item_id)
    assert len(cart_instance.items) == 0
    mock_db.assert_called_with(f"DELETE FROM cart WHERE item_id = {item.item_id}")

# happy_path - test_update_item_quantity_happy_path - Test updating the quantity of an existing item in the cart
def test_update_item_quantity_happy_path(cart, item):
    cart_instance, mock_db = cart
    cart_instance.add_item(item.item_id, 2, item.price, item.name, item.category, cart_instance.user_type)
    cart_instance.update_item_quantity(item.item_id, 5)
    assert cart_instance.items[0]['quantity'] == 5
    mock_db.assert_called_with(f"UPDATE cart SET quantity = 5 WHERE item_id = {item.item_id}")

# happy_path - test_calculate_total_price_happy_path - Test calculating the total price of items in the cart
def test_calculate_total_price_happy_path(cart, item):
    cart_instance, _ = cart
    cart_instance.add_item(item.item_id, 2, item.price, item.name, item.category, cart_instance.user_type)
    total_price = cart_instance.calculate_total_price()
    assert total_price == 200

# happy_path - test_list_items_happy_path - Test listing all items in the cart
def test_list_items_happy_path(cart, item, capsys):
    cart_instance, _ = cart
    cart_instance.add_item(item.item_id, 2, item.price, item.name, item.category, cart_instance.user_type)
    cart_instance.list_items()
    captured = capsys.readouterr()
    assert "Item: Test Item, Quantity: 2, Price per unit: 100" in captured.out

# edge_case - test_add_item_edge_case - Test adding an item with zero quantity
def test_add_item_edge_case(cart, item):
    cart_instance, mock_db = cart
    cart_instance.add_item(item.item_id, 0, item.price, item.name, item.category, cart_instance.user_type)
    assert len(cart_instance.items) == 1
    assert cart_instance.items[0]['quantity'] == 0
    mock_db.assert_called_once()

# edge_case - test_remove_nonexistent_item_edge_case - Test removing an item that does not exist in the cart
def test_remove_nonexistent_item_edge_case(cart):
    cart_instance, mock_db = cart
    cart_instance.remove_item(999)
    assert len(cart_instance.items) == 0
    mock_db.assert_called_with("DELETE FROM cart WHERE item_id = 999")

# edge_case - test_update_item_quantity_nonexistent_edge_case - Test updating the quantity of an item not in the cart
def test_update_item_quantity_nonexistent_edge_case(cart):
    cart_instance, mock_db = cart
    cart_instance.update_item_quantity(999, 5)
    assert len(cart_instance.items) == 0
    mock_db.assert_called_with("UPDATE cart SET quantity = 5 WHERE item_id = 999")

# edge_case - test_calculate_total_price_empty_cart_edge_case - Test calculating total price when cart is empty
def test_calculate_total_price_empty_cart_edge_case(cart):
    cart_instance, _ = cart
    total_price = cart_instance.calculate_total_price()
    assert total_price == 0

# edge_case - test_empty_cart_edge_case - Test emptying a cart that already has items
def test_empty_cart_edge_case(cart, item):
    cart_instance, mock_db = cart
    cart_instance.add_item(item.item_id, 2, item.price, item.name, item.category, cart_instance.user_type)
    cart_instance.empty_cart()
    assert len(cart_instance.items) == 0
    mock_db.assert_called_with("DELETE FROM cart")

