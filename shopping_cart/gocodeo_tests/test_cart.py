import pytest
from unittest.mock import patch, Magic
from shopping_cart.cart import Cart, Item

@pytest.fixture
def cart():
    with patch('shopping_cart.database.add_item_to_cart_db') as mock_add_item_to_cart_db:
        mock_add_item_to_cart_db.return_value = None
        cart = Cart(user_type='regular')
        cart.add_item_to_cart_db = mock_add_item_to_cart_db
        yield cart

# happy_path - test_remove_item_success - Test that an item is successfully removed from the cart when it exists.
def test_remove_item_success(cart):
    # Arrange
    cart.add_item(1, 2, 10.0, 'Apple', 'Fruit', 'regular')
    
    # Act
    cart.remove_item(1)
    
    # Assert
    assert cart.items == []
    cart.add_item_to_cart_db.assert_called_with('DELETE FROM cart WHERE item_id = 1')

# happy_path - test_update_item_quantity_success - Test that the item quantity is updated correctly in the cart.
def test_update_item_quantity_success(cart):
    # Arrange
    cart.add_item(1, 2, 10.0, 'Apple', 'Fruit', 'regular')
    
    # Act
    cart.update_item_quantity(1, 5)
    
    # Assert
    assert cart.items == [{'item_id': 1, 'quantity': 5, 'price': 10.0, 'name': 'Apple', 'category': 'Fruit', 'user_type': 'regular'}]
    cart.add_item_to_cart_db.assert_called_with('UPDATE cart SET quantity = 5 WHERE item_id = 1')

# happy_path - test_calculate_total_price_success - Test that the total price is calculated correctly for items in cart.
def test_calculate_total_price_success(cart):
    # Arrange
    cart.add_item(1, 2, 10.0, 'Apple', 'Fruit', 'regular')
    
    # Act
    total_price = cart.calculate_total_price()
    
    # Assert
    assert total_price == 20.0

# happy_path - test_list_items_success - Test that all items are listed correctly from the cart.
def test_list_items_success(cart, capsys):
    # Arrange
    cart.add_item(1, 2, 10.0, 'Apple', 'Fruit', 'regular')
    
    # Act
    cart.list_items()
    captured = capsys.readouterr()
    
    # Assert
    assert captured.out == 'Item: Apple, Quantity: 2, Price per unit: 10.0\n'

# happy_path - test_empty_cart_success - Test that the cart is emptied successfully.
def test_empty_cart_success(cart):
    # Arrange
    cart.add_item(1, 2, 10.0, 'Apple', 'Fruit', 'regular')
    
    # Act
    cart.empty_cart()
    
    # Assert
    assert cart.items == []
    cart.add_item_to_cart_db.assert_called_with('DELETE FROM cart')

# edge_case - test_add_item_zero_quantity - Test adding an item with zero quantity does not add the item to the cart.
def test_add_item_zero_quantity(cart):
    # Act
    cart.add_item(2, 0, 10.0, 'Banana', 'Fruit', 'guest')
    
    # Assert
    assert cart.items == []

# edge_case - test_remove_item_non_existent - Test removing an item that does not exist in the cart does not affect the cart items.
def test_remove_item_non_existent(cart):
    # Arrange
    cart.add_item(1, 2, 10.0, 'Apple', 'Fruit', 'regular')
    
    # Act
    cart.remove_item(999)
    
    # Assert
    assert cart.items == [{'item_id': 1, 'quantity': 2, 'price': 10.0, 'name': 'Apple', 'category': 'Fruit', 'user_type': 'regular'}]
    cart.add_item_to_cart_db.assert_called_with('DELETE FROM cart WHERE item_id = 999')

# edge_case - test_update_quantity_non_existent - Test updating the quantity of an item that does not exist in the cart does not affect the cart items.
def test_update_quantity_non_existent(cart):
    # Arrange
    cart.add_item(1, 2, 10.0, 'Apple', 'Fruit', 'regular')
    
    # Act
    cart.update_item_quantity(999, 3)
    
    # Assert
    assert cart.items == [{'item_id': 1, 'quantity': 2, 'price': 10.0, 'name': 'Apple', 'category': 'Fruit', 'user_type': 'regular'}]
    cart.add_item_to_cart_db.assert_called_with('UPDATE cart SET quantity = 3 WHERE item_id = 999')

# edge_case - test_calculate_total_price_empty_cart - Test calculating total price with no items in the cart returns zero.
def test_calculate_total_price_empty_cart(cart):
    # Act
    total_price = cart.calculate_total_price()
    
    # Assert
    assert total_price == 0.0

# edge_case - test_list_items_empty_cart - Test listing items when the cart is empty results in no output.
def test_list_items_empty_cart(cart, capsys):
    # Act
    cart.list_items()
    captured = capsys.readouterr()
    
    # Assert
    assert captured.out == ''

# edge_case - test_empty_already_empty_cart - Test emptying an already empty cart does not cause errors.
def test_empty_already_empty_cart(cart):
    # Act
    cart.empty_cart()
    
    # Assert
    assert cart.items == []
    cart.add_item_to_cart_db.assert_called_with('DELETE FROM cart')

