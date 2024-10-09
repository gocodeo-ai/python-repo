import pytest
from unittest.mock import patch, MagicMock
from shopping_cart.cart import Item, Cart
from shopping_cart.database import add_item_to_cart_db

@pytest.fixture
def cart_setup():
    # Create a Cart instance for testing
    cart = Cart(user_type='regular')

    # Mock the add_item_to_cart_db function
    with patch('shopping_cart.database.add_item_to_cart_db') as mock_add_item_to_cart_db:
        mock_add_item_to_cart_db.return_value = None  # Mock return value if needed
        yield cart, mock_add_item_to_cart_db  # Provide the cart instance and the mock

@pytest.fixture
def item_setup():
    # Create an Item instance for testing
    item = Item(item_id=1, price=10.0, name='Apple', category='Fruit')
    yield item  # Provide the item instance

# happy path - remove_item - Test that removing an item from the cart updates the cart's items list and database.
def test_remove_item_from_cart(cart_setup, item_setup):
    cart, mock_add_item_to_cart_db = cart_setup
    item = item_setup
    
    # Add the item to the cart
    cart.add_item(item_id=item.item_id, quantity=2, price=item.price, name=item.name, category=item.category, user_type=cart.user_type)
    
    # Ensure item is added
    assert len(cart.items) == 1
    assert cart.items[0]['item_id'] == item.item_id
    
    # Remove the item from the cart
    cart.remove_item(item_id=item.item_id)
    
    # Validate the cart is empty
    assert cart.items == []
    
    # Check the database query for removing the item
    mock_add_item_to_cart_db.assert_called_once_with('DELETE FROM cart WHERE item_id = 1')


# happy path - update_item_quantity - Test that updating an item's quantity in the cart reflects the change in the items list and database.
def test_update_item_quantity(cart_setup):
    cart, mock_add_item_to_cart_db = cart_setup
    cart.add_item(item_id=1, quantity=2, price=10.0, name='Apple', category='Fruit', user_type='regular')
    cart.update_item_quantity(item_id=1, new_quantity=5)
    assert cart.items == [{'item_id': 1, 'quantity': 5, 'price': 10.0, 'name': 'Apple', 'category': 'Fruit', 'user_type': 'regular'}]
    mock_add_item_to_cart_db.assert_called_with('UPDATE cart SET quantity = 5 WHERE item_id = 1')


# happy path - calculate_total_price - Test that calculating the total price returns the correct total for the items in the cart.
def test_calculate_total_price(cart_setup):
    cart, _ = cart_setup
    cart.add_item(item_id=1, quantity=2, price=10.0, name='Apple', category='Fruit', user_type='regular')
    total_price = cart.calculate_total_price()
    assert total_price == 20.0


# happy path - list_items - Test that listing items prints the correct details of each item in the cart.
def test_list_items(cart_setup, capsys):
    cart, _ = cart_setup
    cart.add_item(item_id=1, quantity=2, price=10.0, name='Apple', category='Fruit', user_type='regular')
    cart.list_items()
    captured = capsys.readouterr()
    assert captured.out == 'Item: Apple, Quantity: 2, Price per unit: 10.0\n'


# edge case - add_item - Test adding an item with zero quantity to the cart and ensure it is handled correctly.
def test_add_zero_quantity_item(cart_setup):
    cart, mock_add_item_to_cart_db = cart_setup
    cart.add_item(item_id=2, quantity=0, price=15.0, name='Banana', category='Fruit', user_type='regular')
    assert cart.items == [{'item_id': 2, 'quantity': 0, 'price': 15.0, 'name': 'Banana', 'category': 'Fruit', 'user_type': 'regular'}]
    mock_add_item_to_cart_db.assert_called_once_with("INSERT INTO cart (item_id, quantity, price, name, category, user_type) VALUES (2, 0, 15.0, 'Banana', 'Fruit', 'regular')")


# edge case - remove_item - Test removing an item that does not exist in the cart and ensure no errors occur.
def test_remove_nonexistent_item(cart_setup):
    cart, mock_add_item_to_cart_db = cart_setup
    cart.remove_item(item_id=99)
    assert cart.items == []
    mock_add_item_to_cart_db.assert_called_with('DELETE FROM cart WHERE item_id = 99')


# edge case - update_item_quantity - Test updating the quantity of an item not present in the cart and ensure it is handled correctly.
def test_update_nonexistent_item_quantity(cart_setup):
    cart, mock_add_item_to_cart_db = cart_setup
    cart.update_item_quantity(item_id=99, new_quantity=3)
    assert cart.items == []
    mock_add_item_to_cart_db.assert_called_with('UPDATE cart SET quantity = 3 WHERE item_id = 99')


# edge case - calculate_total_price - Test calculating total price when the cart is empty and ensure it returns zero.
def test_calculate_total_price_empty_cart(cart_setup):
    cart, _ = cart_setup
    total_price = cart.calculate_total_price()
    assert total_price == 0.0


# edge case - empty_cart - Test emptying the cart when it is already empty and ensure no errors occur.
def test_empty_already_empty_cart(cart_setup):
    cart, mock_add_item_to_cart_db = cart_setup
    cart.empty_cart()
    assert cart.items == []
    mock_add_item_to_cart_db.assert_called_with('DELETE FROM cart')


# happy path - add_item - Test that adding an item to the cart updates the cart's items list and database correctly.



# happy path - add_item - generate test cases on adding an item to the cart and ensure it is added correctly to the items list and database.



# happy path - list_items - generate test cases on listing items in the cart and ensure all items are printed correctly with details.



# edge case - add_item - generate test cases on adding an item with negative quantity and ensure it is handled correctly.



# edge case - remove_item - generate test cases on removing an item from an empty cart and ensure no errors occur.



