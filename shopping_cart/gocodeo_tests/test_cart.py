import pytest
from unittest.mock import patch, MagicMock
from shopping_cart.cart import Cart, Item
from shopping_cart.database import add_item_to_cart_db

@pytest.fixture
def setup_cart():
    with patch('shopping_cart.cart.add_item_to_cart_db') as mock_add_item_to_cart_db:
        mock_add_item_to_cart_db.return_value = MagicMock()
        cart = Cart(user_type="regular")
        yield cart, mock_add_item_to_cart_db# happy_path - add_item - Add an item to the cart and verify it is added correctly
def test_add_item(setup_cart):
    cart, mock_add_item_to_cart_db = setup_cart
    cart.add_item(item_id=1, quantity=2, price=10.0, name='Apple', category='Fruit', user_type='regular')
    assert len(cart.items) == 1
    assert cart.items[0]['item_id'] == 1
    assert cart.items[0]['quantity'] == 2
    assert cart.items[0]['price'] == 10.0
    mock_add_item_to_cart_db.assert_called_once()

# happy_path - remove_item - Remove an item from the cart and verify it is removed
def test_remove_item(setup_cart):
    cart, mock_add_item_to_cart_db = setup_cart
    cart.add_item(item_id=1, quantity=2, price=10.0, name='Apple', category='Fruit', user_type='regular')
    cart.remove_item(item_id=1)
    assert len(cart.items) == 0
    mock_add_item_to_cart_db.assert_called_once()

# happy_path - update_item_quantity - Update the quantity of an item in the cart and verify the change
def test_update_item_quantity(setup_cart):
    cart, mock_add_item_to_cart_db = setup_cart
    cart.add_item(item_id=1, quantity=2, price=10.0, name='Apple', category='Fruit', user_type='regular')
    cart.update_item_quantity(item_id=1, new_quantity=5)
    assert cart.items[0]['quantity'] == 5
    mock_add_item_to_cart_db.assert_called_once()

# happy_path - calculate_total_price - Calculate the total price of items in the cart and verify the total
def test_calculate_total_price(setup_cart):
    cart, mock_add_item_to_cart_db = setup_cart
    cart.add_item(item_id=1, quantity=2, price=10.0, name='Apple', category='Fruit', user_type='regular')
    cart.add_item(item_id=2, quantity=1, price=5.0, name='Banana', category='Fruit', user_type='regular')
    total = cart.calculate_total_price()
    assert total == 25.0

# happy_path - list_items - List items in the cart and verify correct output
def test_list_items(capfd, setup_cart):
    cart, mock_add_item_to_cart_db = setup_cart
    cart.add_item(item_id=1, quantity=2, price=10.0, name='Apple', category='Fruit', user_type='regular')
    cart.list_items()
    captured = capfd.readouterr()
    assert 'Item: Apple, Quantity: 2, Price per unit: 10.0' in captured.out

# happy_path - empty_cart - Empty the cart and verify it is empty
def test_empty_cart(setup_cart):
    cart, mock_add_item_to_cart_db = setup_cart
    cart.add_item(item_id=1, quantity=2, price=10.0, name='Apple', category='Fruit', user_type='regular')
    cart.empty_cart()
    assert len(cart.items) == 0
    mock_add_item_to_cart_db.assert_called_once()

# edge_case - add_item_with_negative_quantity - Attempt to add an item with negative quantity and verify no items are added
def test_add_item_with_negative_quantity(setup_cart):
    cart, mock_add_item_to_cart_db = setup_cart
    cart.add_item(item_id=1, quantity=-2, price=10.0, name='Apple', category='Fruit', user_type='regular')
    assert len(cart.items) == 0
    mock_add_item_to_cart_db.assert_not_called()

# edge_case - remove_nonexistent_item - Attempt to remove an item that does not exist in the cart
def test_remove_nonexistent_item(setup_cart):
    cart, mock_add_item_to_cart_db = setup_cart
    cart.remove_item(item_id=999)
    assert len(cart.items) == 0
    mock_add_item_to_cart_db.assert_called_once()

# edge_case - update_nonexistent_item_quantity - Attempt to update quantity of an item that does not exist
def test_update_nonexistent_item_quantity(setup_cart):
    cart, mock_add_item_to_cart_db = setup_cart
    cart.update_item_quantity(item_id=999, new_quantity=5)
    assert len(cart.items) == 0
    mock_add_item_to_cart_db.assert_called_once()

# edge_case - calculate_total_price_empty_cart - Calculate total price of an empty cart and verify it returns 0
def test_calculate_total_price_empty_cart(setup_cart):
    cart, mock_add_item_to_cart_db = setup_cart
    total = cart.calculate_total_price()
    assert total == 0

# edge_case - empty_already_empty_cart - Attempt to empty an already empty cart and verify no errors occur
def test_empty_already_empty_cart(setup_cart):
    cart, mock_add_item_to_cart_db = setup_cart
    cart.empty_cart()
    assert len(cart.items) == 0
    mock_add_item_to_cart_db.assert_called_once()

