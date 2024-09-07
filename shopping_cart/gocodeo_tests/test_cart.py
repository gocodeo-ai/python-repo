import pytest
from unittest.mock import patch, MagicMock
from shopping_cart.cart import Cart, Item
from shopping_cart.database import add_item_to_cart_db

@pytest.fixture
def setup_cart():
    with patch('shopping_cart.cart.add_item_to_cart_db') as mock_add_item_to_cart_db:
        cart = Cart(user_type='regular')
        yield cart, mock_add_item_to_cart_db

# happy_path - test_add_item - Test that item is added to the cart correctly
def test_add_item(setup_cart):
    cart, mock_add_item_to_cart_db = setup_cart
    cart.add_item(item_id=1, quantity=2, price=100, name='Laptop', category='Electronics', user_type='regular')
    assert cart.items == [{'item_id': 1, 'quantity': 2, 'price': 100, 'name': 'Laptop', 'category': 'Electronics', 'user_type': 'regular'}]
    mock_add_item_to_cart_db.assert_called_once_with("INSERT INTO cart (item_id, quantity, price, name, category, user_type) VALUES (1, 2, 100, 'Laptop', 'Electronics', 'regular')")

# happy_path - test_remove_item - Test that item is removed from the cart correctly
def test_remove_item(setup_cart):
    cart, mock_add_item_to_cart_db = setup_cart
    cart.add_item(item_id=1, quantity=2, price=100, name='Laptop', category='Electronics', user_type='regular')
    cart.remove_item(item_id=1)
    assert cart.items == []
    mock_add_item_to_cart_db.assert_called_with("DELETE FROM cart WHERE item_id = 1")

# happy_path - test_update_item_quantity - Test that item quantity is updated correctly
def test_update_item_quantity(setup_cart):
    cart, mock_add_item_to_cart_db = setup_cart
    cart.add_item(item_id=1, quantity=2, price=100, name='Laptop', category='Electronics', user_type='regular')
    cart.update_item_quantity(item_id=1, new_quantity=5)
    assert cart.items[0]['quantity'] == 5
    mock_add_item_to_cart_db.assert_called_with("UPDATE cart SET quantity = 5 WHERE item_id = 1")

# happy_path - test_calculate_total_price - Test that total price is calculated correctly
def test_calculate_total_price(setup_cart):
    cart, _ = setup_cart
    cart.add_item(item_id=1, quantity=2, price=100, name='Laptop', category='Electronics', user_type='regular')
    total_price = cart.calculate_total_price()
    assert total_price == 200

# happy_path - test_list_items - Test that items are listed correctly
def test_list_items(setup_cart, capsys):
    cart, _ = setup_cart
    cart.add_item(item_id=1, quantity=2, price=100, name='Laptop', category='Electronics', user_type='regular')
    cart.list_items()
    captured = capsys.readouterr()
    assert captured.out == "Item: Laptop, Quantity: 2, Price per unit: 100\n"

# happy_path - test_empty_cart - Test that cart is emptied correctly
def test_empty_cart(setup_cart):
    cart, mock_add_item_to_cart_db = setup_cart
    cart.add_item(item_id=1, quantity=2, price=100, name='Laptop', category='Electronics', user_type='regular')
    cart.empty_cart()
    assert cart.items == []
    mock_add_item_to_cart_db.assert_called_with("DELETE FROM cart")

# edge_case - test_add_item_zero_quantity - Test adding an item with zero quantity
def test_add_item_zero_quantity(setup_cart):
    cart, mock_add_item_to_cart_db = setup_cart
    cart.add_item(item_id=2, quantity=0, price=50, name='Mouse', category='Electronics', user_type='guest')
    assert cart.items == [{'item_id': 2, 'quantity': 0, 'price': 50, 'name': 'Mouse', 'category': 'Electronics', 'user_type': 'guest'}]
    mock_add_item_to_cart_db.assert_called_once_with("INSERT INTO cart (item_id, quantity, price, name, category, user_type) VALUES (2, 0, 50, 'Mouse', 'Electronics', 'guest')")

# edge_case - test_remove_nonexistent_item - Test removing an item not in the cart
def test_remove_nonexistent_item(setup_cart):
    cart, mock_add_item_to_cart_db = setup_cart
    cart.remove_item(item_id=99)
    assert cart.items == []
    mock_add_item_to_cart_db.assert_called_with("DELETE FROM cart WHERE item_id = 99")

# edge_case - test_update_quantity_nonexistent_item - Test updating quantity of an item not in the cart
def test_update_quantity_nonexistent_item(setup_cart):
    cart, mock_add_item_to_cart_db = setup_cart
    cart.update_item_quantity(item_id=99, new_quantity=3)
    assert cart.items == []
    mock_add_item_to_cart_db.assert_called_with("UPDATE cart SET quantity = 3 WHERE item_id = 99")

# edge_case - test_calculate_total_price_empty_cart - Test calculating total price with no items
def test_calculate_total_price_empty_cart(setup_cart):
    cart, _ = setup_cart
    total_price = cart.calculate_total_price()
    assert total_price == 0

# edge_case - test_list_items_empty_cart - Test listing items when cart is empty
def test_list_items_empty_cart(setup_cart, capsys):
    cart, _ = setup_cart
    cart.list_items()
    captured = capsys.readouterr()
    assert captured.out == ""

# edge_case - test_empty_already_empty_cart - Test emptying an already empty cart
def test_empty_already_empty_cart(setup_cart):
    cart, mock_add_item_to_cart_db = setup_cart
    cart.empty_cart()
    assert cart.items == []
    mock_add_item_to_cart_db.assert_called_with("DELETE FROM cart")

