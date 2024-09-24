import pytest
from unittest.mock import patch, MagicMock
from shopping_cart.cart import Cart, Item
from shopping_cart.database import add_item_to_cart_db

@pytest.fixture
def cart_setup():
    with patch('shopping_cart.database.add_item_to_cart_db') as mock_add_item_to_cart_db:
        mock_add_item_to_cart_db.return_value = None  # Mocking the return value of the DB function
        
        cart = Cart(user_type='regular')
        yield cart, mock_add_item_to_cart_db  # Provide the cart instance and the mock for further assertions

@pytest.fixture
def item_setup():
    item = Item(item_id=1, price=10.0, name='Item A', category='Category 1')
    return item

# happy_path - test_add_item - Test that an item is added to the cart with correct details
def test_add_item(cart_setup):
    cart, mock_db = cart_setup
    cart.add_item(item_id=1, quantity=2, price=10.0, name='Item A', category='Category 1', user_type='regular')
    assert cart.items == [{'item_id': 1, 'quantity': 2, 'price': 10.0, 'name': 'Item A', 'category': 'Category 1', 'user_type': 'regular'}]
    mock_db.assert_called_once_with("INSERT INTO cart (item_id, quantity, price, name, category, user_type) VALUES (1, 2, 10.0, 'Item A', 'Category 1', 'regular')")

# happy_path - test_remove_item - Test that an item is removed from the cart successfully
def test_remove_item(cart_setup, item_setup):
    cart, mock_db = cart_setup
    item = item_setup
    cart.add_item(item_id=item.item_id, quantity=2, price=item.price, name=item.name, category=item.category, user_type='regular')
    cart.remove_item(item_id=item.item_id)
    assert cart.items == []
    mock_db.assert_called_with("DELETE FROM cart WHERE item_id = 1")

# happy_path - test_update_item_quantity - Test that the quantity of an item is updated correctly in the cart
def test_update_item_quantity(cart_setup, item_setup):
    cart, mock_db = cart_setup
    item = item_setup
    cart.add_item(item_id=item.item_id, quantity=2, price=item.price, name=item.name, category=item.category, user_type='regular')
    cart.update_item_quantity(item_id=item.item_id, new_quantity=5)
    assert cart.items[0]['quantity'] == 5
    mock_db.assert_called_with("UPDATE cart SET quantity = 5 WHERE item_id = 1")

# happy_path - test_calculate_total_price - Test that the total price is calculated correctly
def test_calculate_total_price(cart_setup, item_setup):
    cart, mock_db = cart_setup
    item = item_setup
    cart.add_item(item_id=item.item_id, quantity=2, price=item.price, name=item.name, category=item.category, user_type='regular')
    total_price = cart.calculate_total_price()
    assert total_price == 20.0

# happy_path - test_list_items - Test that all items are listed correctly with their details
def test_list_items(cart_setup, capsys):
    cart, mock_db = cart_setup
    cart.add_item(item_id=1, quantity=2, price=10.0, name='Item A', category='Category 1', user_type='regular')
    cart.list_items()
    captured = capsys.readouterr()
    assert captured.out.strip() == "Item: Item A, Quantity: 2, Price per unit: 10.0"

# happy_path - test_empty_cart - Test that the cart is emptied successfully
def test_empty_cart(cart_setup, item_setup):
    cart, mock_db = cart_setup
    item = item_setup
    cart.add_item(item_id=item.item_id, quantity=2, price=item.price, name=item.name, category=item.category, user_type='regular')
    cart.empty_cart()
    assert cart.items == []
    mock_db.assert_called_with("DELETE FROM cart")

# edge_case - test_add_item_zero_quantity - Test adding an item with zero quantity
def test_add_item_zero_quantity(cart_setup):
    cart, mock_db = cart_setup
    cart.add_item(item_id=2, quantity=0, price=10.0, name='Item B', category='Category 2', user_type='guest')
    assert cart.items == [{'item_id': 2, 'quantity': 0, 'price': 10.0, 'name': 'Item B', 'category': 'Category 2', 'user_type': 'guest'}]
    mock_db.assert_called_once_with("INSERT INTO cart (item_id, quantity, price, name, category, user_type) VALUES (2, 0, 10.0, 'Item B', 'Category 2', 'guest')")

# edge_case - test_remove_nonexistent_item - Test removing an item that does not exist in the cart
def test_remove_nonexistent_item(cart_setup):
    cart, mock_db = cart_setup
    cart.remove_item(item_id=99)
    assert cart.items == []
    mock_db.assert_called_with("DELETE FROM cart WHERE item_id = 99")

# edge_case - test_update_item_negative_quantity - Test updating the quantity of an item to a negative value
def test_update_item_negative_quantity(cart_setup, item_setup):
    cart, mock_db = cart_setup
    item = item_setup
    cart.add_item(item_id=item.item_id, quantity=2, price=item.price, name=item.name, category=item.category, user_type='regular')
    cart.update_item_quantity(item_id=item.item_id, new_quantity=-1)
    assert cart.items[0]['quantity'] == -1
    mock_db.assert_called_with("UPDATE cart SET quantity = -1 WHERE item_id = 1")

# edge_case - test_calculate_total_price_empty_cart - Test calculating total price with no items in the cart
def test_calculate_total_price_empty_cart(cart_setup):
    cart, mock_db = cart_setup
    total_price = cart.calculate_total_price()
    assert total_price == 0.0

# edge_case - test_list_items_empty_cart - Test listing items when the cart is empty
def test_list_items_empty_cart(cart_setup, capsys):
    cart, mock_db = cart_setup
    cart.list_items()
    captured = capsys.readouterr()
    assert captured.out.strip() == ""

# edge_case - test_empty_already_empty_cart - Test emptying an already empty cart
def test_empty_already_empty_cart(cart_setup):
    cart, mock_db = cart_setup
    cart.empty_cart()
    assert cart.items == []
    mock_db.assert_called_with("DELETE FROM cart")

