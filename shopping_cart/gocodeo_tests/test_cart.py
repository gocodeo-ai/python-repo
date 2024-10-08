import pytest
from unittest import mock
from shopping_cart.cart import Item, Cart
from shopping_cart.database import add_item_to_cart_db

@pytest.fixture
def cart_setup():
    # Create a Cart instance
    cart = Cart(user_type='regular')
    
    # Mock the add_item_to_cart_db function
    with mock.patch('shopping_cart.database.add_item_to_cart_db') as mock_db:
        yield cart, mock_db
        
        # Clean up if necessary

@pytest.fixture
def item_setup():
    # Create an Item instance
    item = Item(item_id=1, price=10.0, name='apple', category='fruit')
    return item

# happy path - add_item - Test that item is added correctly to cart and database
def test_add_item_to_cart(cart_setup):
    cart, mock_db = cart_setup
    cart.add_item(item_id=1, quantity=2, price=10.0, name='apple', category='fruit', user_type='regular')
    assert cart.items == [{'item_id': 1, 'quantity': 2, 'price': 10.0, 'name': 'apple', 'category': 'fruit', 'user_type': 'regular'}]
    mock_db.assert_called_once_with("INSERT INTO cart (item_id, quantity, price, name, category, user_type) VALUES (1, 2, 10.0, 'apple', 'fruit', 'regular')")


# happy path - remove_item - Test that item is removed correctly from cart and database
def test_remove_item_from_cart(cart_setup):
    cart, mock_db = cart_setup
    cart.add_item(item_id=1, quantity=2, price=10.0, name='apple', category='fruit', user_type='regular')
    cart.remove_item(item_id=1)
    assert cart.items == []
    mock_db.assert_called_with('DELETE FROM cart WHERE item_id = 1')


# happy path - update_item_quantity - Test that item quantity is updated correctly in cart and database
def test_update_item_quantity(cart_setup):
    cart, mock_db = cart_setup
    cart.add_item(item_id=1, quantity=2, price=10.0, name='apple', category='fruit', user_type='regular')
    cart.update_item_quantity(item_id=1, new_quantity=5)
    assert cart.items == [{'item_id': 1, 'quantity': 5, 'price': 10.0, 'name': 'apple', 'category': 'fruit', 'user_type': 'regular'}]
    mock_db.assert_called_with('UPDATE cart SET quantity = 5 WHERE item_id = 1')


# happy path - calculate_total_price - Test that total price is calculated correctly
def test_calculate_total_price(cart_setup):
    cart, mock_db = cart_setup
    cart.add_item(item_id=1, quantity=2, price=10.0, name='apple', category='fruit', user_type='regular')
    cart.add_item(item_id=2, quantity=1, price=20.0, name='banana', category='fruit', user_type='regular')
    total_price = cart.calculate_total_price()
    assert total_price == 40.0


# happy path - empty_cart - Test that cart is emptied correctly and database is cleared
def test_empty_cart(cart_setup):
    cart, mock_db = cart_setup
    cart.add_item(item_id=1, quantity=2, price=10.0, name='apple', category='fruit', user_type='regular')
    cart.empty_cart()
    assert cart.items == []
    mock_db.assert_called_with('DELETE FROM cart')


# edge case - add_item - Test adding item with zero quantity
def test_add_item_with_zero_quantity(cart_setup):
    cart, mock_db = cart_setup
    cart.add_item(item_id=2, quantity=0, price=15.0, name='banana', category='fruit', user_type='regular')
    assert cart.items == [{'item_id': 2, 'quantity': 0, 'price': 15.0, 'name': 'banana', 'category': 'fruit', 'user_type': 'regular'}]
    mock_db.assert_called_once_with("INSERT INTO cart (item_id, quantity, price, name, category, user_type) VALUES (2, 0, 15.0, 'banana', 'fruit', 'regular')")


# edge case - remove_item - Test removing item not in cart
def test_remove_item_not_in_cart(cart_setup):
    cart, mock_db = cart_setup
    cart.remove_item(item_id=99)
    assert cart.items == []
    mock_db.assert_called_with('DELETE FROM cart WHERE item_id = 99')


# edge case - update_item_quantity - Test updating quantity of item not in cart
def test_update_quantity_item_not_in_cart(cart_setup):
    cart, mock_db = cart_setup
    cart.update_item_quantity(item_id=99, new_quantity=3)
    assert cart.items == []
    mock_db.assert_called_with('UPDATE cart SET quantity = 3 WHERE item_id = 99')


# edge case - calculate_total_price - Test calculating total price with empty cart
def test_calculate_total_price_empty_cart(cart_setup):
    cart, mock_db = cart_setup
    total_price = cart.calculate_total_price()
    assert total_price == 0


# edge case - empty_cart - Test empty cart when already empty
def test_empty_cart_when_already_empty(cart_setup):
    cart, mock_db = cart_setup
    cart.empty_cart()
    assert cart.items == []
    mock_db.assert_called_with('DELETE FROM cart')


