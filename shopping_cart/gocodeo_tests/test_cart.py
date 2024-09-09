import pytest
from unittest.mock import patch, MagicMock
from shopping_cart.cart import Cart, Item

@pytest.fixture
def cart_setup():
    with patch('shopping_cart.cart.add_item_to_cart_db') as mock_add_item_to_cart_db:
        # Mock the database interaction function
        mock_add_item_to_cart_db.return_value = None

        # Create a Cart instance
        cart = Cart(user_type='regular')
        
        # Return the cart and the mocked dependencies
        yield cart, mock_add_item_to_cart_db
```

# happy_path - test_add_item_success - Test that an item is added to the cart successfully
def test_add_item_success(cart_setup):
    cart, mock_add_item_to_cart_db = cart_setup
    cart.add_item(item_id=1, quantity=2, price=100, name='Laptop', category='Electronics', user_type='regular')
    assert cart.items == [{'item_id': 1, 'quantity': 2, 'price': 100, 'name': 'Laptop', 'category': 'Electronics', 'user_type': 'regular'}]
    mock_add_item_to_cart_db.assert_called_once()

# happy_path - test_remove_item_success - Test that an item is removed from the cart successfully
def test_remove_item_success(cart_setup):
    cart, mock_add_item_to_cart_db = cart_setup
    cart.add_item(item_id=1, quantity=2, price=100, name='Laptop', category='Electronics', user_type='regular')
    cart.remove_item(item_id=1)
    assert cart.items == []
    mock_add_item_to_cart_db.assert_called()

# happy_path - test_update_item_quantity_success - Test that item quantity is updated successfully
def test_update_item_quantity_success(cart_setup):
    cart, mock_add_item_to_cart_db = cart_setup
    cart.add_item(item_id=1, quantity=2, price=100, name='Laptop', category='Electronics', user_type='regular')
    cart.update_item_quantity(item_id=1, new_quantity=5)
    assert cart.items == [{'item_id': 1, 'quantity': 5, 'price': 100, 'name': 'Laptop', 'category': 'Electronics', 'user_type': 'regular'}]
    mock_add_item_to_cart_db.assert_called()

# happy_path - test_calculate_total_price_success - Test that total price is calculated correctly
def test_calculate_total_price_success(cart_setup):
    cart, mock_add_item_to_cart_db = cart_setup
    cart.add_item(item_id=1, quantity=2, price=100, name='Laptop', category='Electronics', user_type='regular')
    total_price = cart.calculate_total_price()
    assert total_price == 200

# happy_path - test_list_items_success - Test that items are listed correctly
def test_list_items_success(cart_setup, capsys):
    cart, mock_add_item_to_cart_db = cart_setup
    cart.add_item(item_id=1, quantity=2, price=100, name='Laptop', category='Electronics', user_type='regular')
    cart.list_items()
    captured = capsys.readouterr()
    assert captured.out.strip() == 'Item: Laptop, Quantity: 2, Price per unit: 100'

# edge_case - test_add_item_zero_quantity - Test add item with zero quantity
def test_add_item_zero_quantity(cart_setup):
    cart, mock_add_item_to_cart_db = cart_setup
    cart.add_item(item_id=2, quantity=0, price=50, name='Mouse', category='Electronics', user_type='regular')
    assert cart.items == [{'item_id': 2, 'quantity': 0, 'price': 50, 'name': 'Mouse', 'category': 'Electronics', 'user_type': 'regular'}]
    mock_add_item_to_cart_db.assert_called_once()

# edge_case - test_add_item_negative_price - Test add item with negative price
def test_add_item_negative_price(cart_setup):
    cart, mock_add_item_to_cart_db = cart_setup
    with pytest.raises(ValueError, match='Negative price'):
        cart.add_item(item_id=3, quantity=1, price=-10, name='Keyboard', category='Electronics', user_type='regular')
    mock_add_item_to_cart_db.assert_not_called()

# edge_case - test_remove_non_existent_item - Test remove non-existent item
def test_remove_non_existent_item(cart_setup):
    cart, mock_add_item_to_cart_db = cart_setup
    cart.add_item(item_id=1, quantity=2, price=100, name='Laptop', category='Electronics', user_type='regular')
    cart.remove_item(item_id=99)
    assert cart.items == [{'item_id': 1, 'quantity': 2, 'price': 100, 'name': 'Laptop', 'category': 'Electronics', 'user_type': 'regular'}]
    mock_add_item_to_cart_db.assert_called()

# edge_case - test_update_quantity_non_existent_item - Test update quantity for non-existent item
def test_update_quantity_non_existent_item(cart_setup):
    cart, mock_add_item_to_cart_db = cart_setup
    cart.add_item(item_id=1, quantity=2, price=100, name='Laptop', category='Electronics', user_type='regular')
    cart.update_item_quantity(item_id=99, new_quantity=3)
    assert cart.items == [{'item_id': 1, 'quantity': 2, 'price': 100, 'name': 'Laptop', 'category': 'Electronics', 'user_type': 'regular'}]
    mock_add_item_to_cart_db.assert_called()

# edge_case - test_calculate_total_price_no_items - Test calculate total price with no items
def test_calculate_total_price_no_items(cart_setup):
    cart, mock_add_item_to_cart_db = cart_setup
    total_price = cart.calculate_total_price()
    assert total_price == 0

# edge_case - test_list_items_no_items - Test list items with no items in cart
def test_list_items_no_items(cart_setup, capsys):
    cart, mock_add_item_to_cart_db = cart_setup
    cart.list_items()
    captured = capsys.readouterr()
    assert captured.out.strip() == ''

