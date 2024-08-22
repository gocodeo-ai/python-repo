import pytest
from unittest.mock import patch, MagicMock
from shopping_cart.database import add_item_to_cart_db
from shopping_cart.cart import Cart, Item

@pytest.fixture
def cart():
    with patch('shopping_cart.database.add_item_to_cart_db') as mock_add_item_to_cart_db:
        mock_add_item_to_cart_db.return_value = None
        cart = Cart(user_type="regular")
        yield cart
```

# happy_path - test_add_item_success - Test that adding an item with valid details to the cart is successful.
def test_add_item_success(cart):
    cart.add_item(item_id=1, quantity=2, price=100, name='Laptop', category='Electronics', user_type='regular')
    assert cart.items == [{'item_id': 1, 'quantity': 2, 'price': 100, 'name': 'Laptop', 'category': 'Electronics', 'user_type': 'regular'}]

# happy_path - test_remove_item_success - Test that removing an existing item from the cart is successful.
def test_remove_item_success(cart):
    cart.add_item(item_id=1, quantity=2, price=100, name='Laptop', category='Electronics', user_type='regular')
    cart.remove_item(item_id=1)
    assert cart.items == []

# happy_path - test_update_item_quantity_success - Test that updating the quantity of an existing item in the cart is successful.
def test_update_item_quantity_success(cart):
    cart.add_item(item_id=1, quantity=2, price=100, name='Laptop', category='Electronics', user_type='regular')
    cart.update_item_quantity(item_id=1, new_quantity=5)
    assert cart.items == [{'item_id': 1, 'quantity': 5, 'price': 100, 'name': 'Laptop', 'category': 'Electronics', 'user_type': 'regular'}]

# happy_path - test_calculate_total_price_success - Test that calculating the total price of items in the cart returns the correct sum.
def test_calculate_total_price_success(cart):
    cart.add_item(item_id=1, quantity=2, price=100, name='Laptop', category='Electronics', user_type='regular')
    total_price = cart.calculate_total_price()
    assert total_price == 200

# happy_path - test_list_items_success - Test that listing items in the cart displays all items with correct details.
def test_list_items_success(cart, capsys):
    cart.add_item(item_id=1, quantity=2, price=100, name='Laptop', category='Electronics', user_type='regular')
    cart.list_items()
    captured = capsys.readouterr()
    assert 'Item: Laptop, Quantity: 2, Price per unit: 100' in captured.out

# happy_path - test_empty_cart_success - Test that emptying the cart removes all items successfully.
def test_empty_cart_success(cart):
    cart.add_item(item_id=1, quantity=2, price=100, name='Laptop', category='Electronics', user_type='regular')
    cart.empty_cart()
    assert cart.items == []

# edge_case - test_add_item_zero_quantity - Test that adding an item with zero quantity does not add the item to the cart.
def test_add_item_zero_quantity(cart):
    cart.add_item(item_id=2, quantity=0, price=50, name='Mouse', category='Electronics', user_type='guest')
    assert cart.items == []

# edge_case - test_remove_item_not_in_cart - Test that removing an item not present in the cart does not affect the cart contents.
def test_remove_item_not_in_cart(cart):
    cart.add_item(item_id=1, quantity=2, price=100, name='Laptop', category='Electronics', user_type='regular')
    cart.remove_item(item_id=99)
    assert cart.items == [{'item_id': 1, 'quantity': 2, 'price': 100, 'name': 'Laptop', 'category': 'Electronics', 'user_type': 'regular'}]

# edge_case - test_update_item_quantity_not_in_cart - Test that updating the quantity of an item not in the cart does not alter the cart.
def test_update_item_quantity_not_in_cart(cart):
    cart.add_item(item_id=1, quantity=2, price=100, name='Laptop', category='Electronics', user_type='regular')
    cart.update_item_quantity(item_id=99, new_quantity=3)
    assert cart.items == [{'item_id': 1, 'quantity': 2, 'price': 100, 'name': 'Laptop', 'category': 'Electronics', 'user_type': 'regular'}]

# edge_case - test_calculate_total_price_empty_cart - Test that calculating total price in an empty cart returns zero.
def test_calculate_total_price_empty_cart(cart):
    total_price = cart.calculate_total_price()
    assert total_price == 0

# edge_case - test_list_items_empty_cart - Test that listing items in an empty cart displays no items.
def test_list_items_empty_cart(cart, capsys):
    cart.list_items()
    captured = capsys.readouterr()
    assert captured.out == ''

# edge_case - test_empty_cart_already_empty - Test that emptying an already empty cart does not cause errors.
def test_empty_cart_already_empty(cart):
    cart.empty_cart()
    assert cart.items == []

