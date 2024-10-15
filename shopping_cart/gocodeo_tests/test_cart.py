import pytest
from unittest.mock import patch, MagicMock
from shopping_cart.cart import Item, Cart
from shopping_cart.database import add_item_to_cart_db

@pytest.fixture
def cart():
    with patch('shopping_cart.database.add_item_to_cart_db') as mock_db:
        yield Cart(user_type='regular'), mock_db

@pytest.fixture
def item():
    return Item(item_id=1, price=10.0, name='Apple', category='Fruit')

@pytest.fixture
def mock_db():
    with patch('shopping_cart.database.add_item_to_cart_db') as mock:
        yield mock

# happy path - add_item - Test that adding an item updates the cart and database correctly.
def test_add_item_updates_cart_and_db(cart, item):
    cart_instance, mock_db = cart
    cart_instance.add_item(item_id=item.item_id, quantity=2, price=item.price, name=item.name, category=item.category, user_type='regular')
    assert cart_instance.items == [{'item_id': 1, 'quantity': 2, 'price': 10.0, 'name': 'Apple', 'category': 'Fruit', 'user_type': 'regular'}]
    mock_db.assert_called_once_with("INSERT INTO cart (item_id, quantity, price, name, category, user_type) VALUES (1, 2, 10.0, 'Apple', 'Fruit', 'regular')")


# happy path - remove_item - Test that removing an item updates the cart and database correctly.
def test_remove_item_updates_cart_and_db(cart, item):
    cart_instance, mock_db = cart
    cart_instance.add_item(item_id=item.item_id, quantity=2, price=item.price, name=item.name, category=item.category, user_type='regular')
    cart_instance.remove_item(item_id=item.item_id)
    assert cart_instance.items == []
    mock_db.assert_called_with('DELETE FROM cart WHERE item_id = 1')


# happy path - update_item_quantity - Test that updating item quantity modifies the cart and database correctly.
def test_update_item_quantity_modifies_cart_and_db(cart, item):
    cart_instance, mock_db = cart
    cart_instance.add_item(item_id=item.item_id, quantity=2, price=item.price, name=item.name, category=item.category, user_type='regular')
    cart_instance.update_item_quantity(item_id=item.item_id, new_quantity=5)
    assert cart_instance.items == [{'item_id': 1, 'quantity': 5, 'price': 10.0, 'name': 'Apple', 'category': 'Fruit', 'user_type': 'regular'}]
    mock_db.assert_called_with('UPDATE cart SET quantity = 5 WHERE item_id = 1')


# happy path - calculate_total_price - Test that calculating total price returns correct sum.
def test_calculate_total_price_returns_correct_sum(cart, item):
    cart_instance, _ = cart
    cart_instance.add_item(item_id=item.item_id, quantity=5, price=item.price, name=item.name, category=item.category, user_type='regular')
    total_price = cart_instance.calculate_total_price()
    assert total_price == 50.0


# happy path - list_items - Test that listing items prints correct details.
def test_list_items_prints_correct_details(cart, item, capsys):
    cart_instance, _ = cart
    cart_instance.add_item(item_id=item.item_id, quantity=2, price=item.price, name=item.name, category=item.category, user_type='regular')
    cart_instance.list_items()
    captured = capsys.readouterr()
    assert captured.out == 'Item: Apple, Quantity: 2, Price per unit: 10.0\n'


# edge case - add_item - Test that adding an item with zero quantity doesn't affect the cart.
def test_add_item_with_zero_quantity(cart, item):
    cart_instance, mock_db = cart
    cart_instance.add_item(item_id=2, quantity=0, price=5.0, name='Banana', category='Fruit', user_type='guest')
    assert cart_instance.items == []
    mock_db.assert_called_once_with("INSERT INTO cart (item_id, quantity, price, name, category, user_type) VALUES (2, 0, 5.0, 'Banana', 'Fruit', 'guest')")


# edge case - remove_item - Test that removing an item not in the cart doesn't cause errors.
def test_remove_item_not_in_cart(cart, item):
    cart_instance, mock_db = cart
    cart_instance.add_item(item_id=item.item_id, quantity=2, price=item.price, name=item.name, category=item.category, user_type='regular')
    cart_instance.remove_item(item_id=3)
    assert cart_instance.items == [{'item_id': 1, 'quantity': 2, 'price': 10.0, 'name': 'Apple', 'category': 'Fruit', 'user_type': 'regular'}]
    mock_db.assert_called_with('DELETE FROM cart WHERE item_id = 3')


# edge case - update_item_quantity - Test that updating quantity to zero removes the item from the cart.
def test_update_quantity_to_zero_removes_item(cart, item):
    cart_instance, mock_db = cart
    cart_instance.add_item(item_id=item.item_id, quantity=2, price=item.price, name=item.name, category=item.category, user_type='regular')
    cart_instance.update_item_quantity(item_id=item.item_id, new_quantity=0)
    assert cart_instance.items == []
    mock_db.assert_called_with('UPDATE cart SET quantity = 0 WHERE item_id = 1')


# edge case - calculate_total_price - Test that calculating total price with no items returns zero.
def test_calculate_total_price_with_no_items(cart):
    cart_instance, _ = cart
    total_price = cart_instance.calculate_total_price()
    assert total_price == 0.0


# edge case - empty_cart - Test that emptying the cart clears all items and updates database.
def test_empty_cart_clears_items_and_db(cart, item):
    cart_instance, mock_db = cart
    cart_instance.add_item(item_id=item.item_id, quantity=2, price=item.price, name=item.name, category=item.category, user_type='regular')
    cart_instance.empty_cart()
    assert cart_instance.items == []
    mock_db.assert_called_once_with('DELETE FROM cart')


