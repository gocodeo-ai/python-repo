import pytest
from unittest import mock
from shopping_cart.cart import Item, Cart
from shopping_cart.database import add_item_to_cart_db

@pytest.fixture
def cart():
    with mock.patch('shopping_cart.database.add_item_to_cart_db') as mock_add_item_to_cart_db:
        yield Cart(user_type='regular')

@pytest.fixture
def item():
    return Item(item_id=1, price=10.0, name='Apple', category='Fruit')

@pytest.fixture
def mock_db():
    with mock.patch('shopping_cart.database.add_item_to_cart_db') as mock_add_item_to_cart_db:
        yield mock_add_item_to_cart_db

# happy path - add_item - Test that item is added to the cart with correct details
def test_add_item_to_cart(cart, mock_db, item):
    cart.add_item(item_id=item.item_id, quantity=2, price=item.price, name=item.name, category=item.category, user_type=cart.user_type)
    assert cart.items == [{'item_id': 1, 'quantity': 2, 'price': 10.0, 'name': 'Apple', 'category': 'Fruit', 'user_type': 'regular'}]
    mock_db.assert_called_once_with("INSERT INTO cart (item_id, quantity, price, name, category, user_type) VALUES (1, 2, 10.0, 'Apple', 'Fruit', 'regular')")


# happy path - remove_item - Test that item is removed from the cart
def test_remove_item_from_cart(cart, mock_db, item):
    cart.add_item(item_id=item.item_id, quantity=2, price=item.price, name=item.name, category=item.category, user_type=cart.user_type)
    cart.remove_item(item_id=item.item_id)
    assert cart.items == []
    mock_db.assert_called_with("DELETE FROM cart WHERE item_id = 1")


# happy path - update_item_quantity - Test that item quantity is updated in the cart
def test_update_item_quantity(cart, mock_db, item):
    cart.add_item(item_id=item.item_id, quantity=2, price=item.price, name=item.name, category=item.category, user_type=cart.user_type)
    cart.update_item_quantity(item_id=item.item_id, new_quantity=5)
    assert cart.items == [{'item_id': 1, 'quantity': 5, 'price': 10.0, 'name': 'Apple', 'category': 'Fruit', 'user_type': 'regular'}]
    mock_db.assert_called_with("UPDATE cart SET quantity = 5 WHERE item_id = 1")


# happy path - calculate_total_price - Test that total price is calculated correctly
def test_calculate_total_price(cart, item):
    cart.add_item(item_id=item.item_id, quantity=2, price=item.price, name=item.name, category=item.category, user_type=cart.user_type)
    total_price = cart.calculate_total_price()
    assert total_price == 20.0


# happy path - list_items - Test that items are listed correctly
def test_list_items(cart, capsys, item):
    cart.add_item(item_id=item.item_id, quantity=2, price=item.price, name=item.name, category=item.category, user_type=cart.user_type)
    cart.list_items()
    captured = capsys.readouterr()
    assert captured.out == 'Item: Apple, Quantity: 2, Price per unit: 10.0\n'


# happy path - empty_cart - Test that cart is emptied successfully
def test_empty_cart(cart, mock_db, item):
    cart.add_item(item_id=item.item_id, quantity=2, price=item.price, name=item.name, category=item.category, user_type=cart.user_type)
    cart.empty_cart()
    assert cart.items == []
    mock_db.assert_called_with("DELETE FROM cart")


# edge case - add_item - Test adding item with zero quantity
def test_add_item_zero_quantity(cart, mock_db):
    cart.add_item(item_id=2, quantity=0, price=15.0, name='Banana', category='Fruit', user_type='guest')
    assert cart.items == [{'item_id': 2, 'quantity': 0, 'price': 15.0, 'name': 'Banana', 'category': 'Fruit', 'user_type': 'guest'}]
    mock_db.assert_called_once_with("INSERT INTO cart (item_id, quantity, price, name, category, user_type) VALUES (2, 0, 15.0, 'Banana', 'Fruit', 'guest')")


# edge case - remove_item - Test removing item not in the cart
def test_remove_item_not_in_cart(cart, mock_db, item):
    cart.add_item(item_id=item.item_id, quantity=2, price=item.price, name=item.name, category=item.category, user_type=cart.user_type)
    cart.remove_item(item_id=3)
    assert cart.items == [{'item_id': 1, 'quantity': 2, 'price': 10.0, 'name': 'Apple', 'category': 'Fruit', 'user_type': 'regular'}]
    mock_db.assert_called_with("DELETE FROM cart WHERE item_id = 3")


# edge case - update_item_quantity - Test updating quantity of item not in the cart
def test_update_quantity_item_not_in_cart(cart, mock_db, item):
    cart.add_item(item_id=item.item_id, quantity=2, price=item.price, name=item.name, category=item.category, user_type=cart.user_type)
    cart.update_item_quantity(item_id=4, new_quantity=3)
    assert cart.items == [{'item_id': 1, 'quantity': 2, 'price': 10.0, 'name': 'Apple', 'category': 'Fruit', 'user_type': 'regular'}]
    mock_db.assert_called_with("UPDATE cart SET quantity = 3 WHERE item_id = 4")


# edge case - calculate_total_price - Test calculating total price with no items in the cart
def test_calculate_total_price_empty_cart(cart):
    total_price = cart.calculate_total_price()
    assert total_price == 0.0


# edge case - list_items - Test listing items when cart is empty
def test_list_items_empty_cart(cart, capsys):
    cart.list_items()
    captured = capsys.readouterr()
    assert captured.out == ''


# edge case - empty_cart - Test emptying an already empty cart
def test_empty_cart_already_empty(cart, mock_db):
    cart.empty_cart()
    assert cart.items == []
    mock_db.assert_called_with("DELETE FROM cart")


