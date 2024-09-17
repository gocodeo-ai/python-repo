import pytest
from unittest.mock import patch, MagicMock
from shopping_cart.cart import Cart, Item
from shopping_cart.database import add_item_to_cart_db

@pytest.fixture
def cart_setup():
    # Create a Cart instance
    cart = Cart(user_type='regular')
    
    # Mock the add_item_to_cart_db function
    with patch('shopping_cart.database.add_item_to_cart_db') as mock_add_item_to_cart_db:
        mock_add_item_to_cart_db.return_value = None  # You can set a specific return value if needed
        
        yield cart, mock_add_item_to_cart_db  # Provide the cart instance and the mock

@pytest.fixture
def item_setup():
    # Create an Item instance
    item = Item(item_id=1, price=10.0, name='Apple', category='Fruit')
    
    yield item  # Provide the item instance

# happy_path - test_add_item_updates_cart - Test that adding an item updates the cart with the correct details
def test_add_item_updates_cart(cart_setup, item_setup):
    cart, mock_add_item_to_cart_db = cart_setup
    item = item_setup
    cart.add_item(item.item_id, 2, item.price, item.name, item.category, cart.user_type)
    assert cart.items == [{'item_id': 1, 'quantity': 2, 'price': 10.0, 'name': 'Apple', 'category': 'Fruit', 'user_type': 'regular'}]
    mock_add_item_to_cart_db.assert_called_once()

# happy_path - test_remove_item_deletes_from_cart - Test that removing an item deletes it from the cart
def test_remove_item_deletes_from_cart(cart_setup, item_setup):
    cart, mock_add_item_to_cart_db = cart_setup
    item = item_setup
    cart.add_item(item.item_id, 2, item.price, item.name, item.category, cart.user_type)
    cart.remove_item(item.item_id)
    assert cart.items == []
    mock_add_item_to_cart_db.assert_called_with('DELETE FROM cart WHERE item_id = 1')

# happy_path - test_update_item_quantity_changes_quantity - Test that updating item quantity changes the quantity in the cart
def test_update_item_quantity_changes_quantity(cart_setup, item_setup):
    cart, mock_add_item_to_cart_db = cart_setup
    item = item_setup
    cart.add_item(item.item_id, 2, item.price, item.name, item.category, cart.user_type)
    cart.update_item_quantity(item.item_id, 5)
    assert cart.items == [{'item_id': 1, 'quantity': 5, 'price': 10.0, 'name': 'Apple', 'category': 'Fruit', 'user_type': 'regular'}]
    mock_add_item_to_cart_db.assert_called_with('UPDATE cart SET quantity = 5 WHERE item_id = 1')

# happy_path - test_calculate_total_price_returns_correct_total - Test that calculating total price returns correct total
def test_calculate_total_price_returns_correct_total(cart_setup, item_setup):
    cart, _ = cart_setup
    item = item_setup
    cart.add_item(item.item_id, 2, item.price, item.name, item.category, cart.user_type)
    total_price = cart.calculate_total_price()
    assert total_price == 20.0

# happy_path - test_list_items_prints_all_items - Test that listing items prints all items in the cart
def test_list_items_prints_all_items(cart_setup, item_setup, capsys):
    cart, _ = cart_setup
    item = item_setup
    cart.add_item(item.item_id, 2, item.price, item.name, item.category, cart.user_type)
    cart.list_items()
    captured = capsys.readouterr()
    assert captured.out == 'Item: Apple, Quantity: 2, Price per unit: 10.0\n'

# happy_path - test_empty_cart_removes_all_items - Test that emptying the cart removes all items
def test_empty_cart_removes_all_items(cart_setup, item_setup):
    cart, mock_add_item_to_cart_db = cart_setup
    item = item_setup
    cart.add_item(item.item_id, 2, item.price, item.name, item.category, cart.user_type)
    cart.empty_cart()
    assert cart.items == []
    mock_add_item_to_cart_db.assert_called_with('DELETE FROM cart')

# edge_case - test_add_item_with_zero_quantity - Test adding an item with zero quantity
def test_add_item_with_zero_quantity(cart_setup):
    cart, mock_add_item_to_cart_db = cart_setup
    cart.add_item(2, 0, 5.0, 'Banana', 'Fruit', 'regular')
    assert cart.items == [{'item_id': 2, 'quantity': 0, 'price': 5.0, 'name': 'Banana', 'category': 'Fruit', 'user_type': 'regular'}]
    mock_add_item_to_cart_db.assert_called_once()

# edge_case - test_remove_item_not_in_cart - Test removing an item not in the cart
def test_remove_item_not_in_cart(cart_setup, item_setup):
    cart, mock_add_item_to_cart_db = cart_setup
    item = item_setup
    cart.add_item(item.item_id, 2, item.price, item.name, item.category, cart.user_type)
    cart.remove_item(99)
    assert cart.items == [{'item_id': 1, 'quantity': 2, 'price': 10.0, 'name': 'Apple', 'category': 'Fruit', 'user_type': 'regular'}]
    mock_add_item_to_cart_db.assert_not_called()

# edge_case - test_update_quantity_for_item_not_in_cart - Test updating quantity for an item not in the cart
def test_update_quantity_for_item_not_in_cart(cart_setup, item_setup):
    cart, mock_add_item_to_cart_db = cart_setup
    item = item_setup
    cart.add_item(item.item_id, 2, item.price, item.name, item.category, cart.user_type)
    cart.update_item_quantity(99, 3)
    assert cart.items == [{'item_id': 1, 'quantity': 2, 'price': 10.0, 'name': 'Apple', 'category': 'Fruit', 'user_type': 'regular'}]
    mock_add_item_to_cart_db.assert_not_called()

# edge_case - test_calculate_total_price_no_items - Test calculating total price with no items in the cart
def test_calculate_total_price_no_items(cart_setup):
    cart, _ = cart_setup
    total_price = cart.calculate_total_price()
    assert total_price == 0.0

# edge_case - test_list_items_empty_cart - Test listing items when the cart is empty
def test_list_items_empty_cart(cart_setup, capsys):
    cart, _ = cart_setup
    cart.list_items()
    captured = capsys.readouterr()
    assert captured.out == ''

# edge_case - test_empty_cart_already_empty - Test emptying an already empty cart
def test_empty_cart_already_empty(cart_setup):
    cart, mock_add_item_to_cart_db = cart_setup
    cart.empty_cart()
    assert cart.items == []
    mock_add_item_to_cart_db.assert_called_with('DELETE FROM cart')

