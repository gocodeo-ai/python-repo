import pytest
from unittest import mock
from shopping_cart.cart import Item, Cart
from shopping_cart.database import add_item_to_cart_db

@pytest.fixture
def cart():
    return Cart(user_type='Regular')

@pytest.fixture
def mock_add_item_to_cart_db():
    with mock.patch('shopping_cart.database.add_item_to_cart_db') as mock_db:
        yield mock_db

@pytest.fixture
def mock_item():
    return Item(item_id=1, price=100, name='Laptop', category='Electronics')

@pytest.fixture
def setup_cart_with_item(cart, mock_add_item_to_cart_db):
    cart.add_item(item_id=1, quantity=2, price=100, name='Laptop', category='Electronics', user_type='Regular')
    return cart

# happy path - add_item - Test that an item is added to the cart successfully
def test_add_item_success(cart, mock_add_item_to_cart_db, mock_item):
    cart.add_item(item_id=1, quantity=2, price=100, name='Laptop', category='Electronics', user_type='Regular')
    assert cart.items == [{'item_id': 1, 'quantity': 2, 'price': 100, 'name': 'Laptop', 'category': 'Electronics', 'user_type': 'Regular'}]
    mock_add_item_to_cart_db.assert_called_once_with("INSERT INTO cart (item_id, quantity, price, name, category, user_type) VALUES (1, 2, 100, 'Laptop', 'Electronics', 'Regular')")


# happy path - remove_item - Test that an item is removed from the cart
def test_remove_item_success(setup_cart_with_item, mock_add_item_to_cart_db):
    setup_cart_with_item.remove_item(item_id=1)
    assert setup_cart_with_item.items == []
    mock_add_item_to_cart_db.assert_called_with("DELETE FROM cart WHERE item_id = 1")


# happy path - update_item_quantity - Test that item quantity is updated successfully
def test_update_item_quantity_success(setup_cart_with_item, mock_add_item_to_cart_db):
    setup_cart_with_item.update_item_quantity(item_id=1, new_quantity=5)
    assert setup_cart_with_item.items[0]['quantity'] == 5
    mock_add_item_to_cart_db.assert_called_with("UPDATE cart SET quantity = 5 WHERE item_id = 1")


# happy path - calculate_total_price - Test that total price is calculated correctly
def test_calculate_total_price_success(setup_cart_with_item):
    total_price = setup_cart_with_item.calculate_total_price()
    assert total_price == 200  # 2 * 100


# happy path - list_items - Test that all items are listed correctly
def test_list_items_success(setup_cart_with_item, capsys):
    setup_cart_with_item.list_items()
    captured = capsys.readouterr()
    assert captured.out == "Item: Laptop, Quantity: 2, Price per unit: 100\n"


# happy path - empty_cart - Test that cart is emptied successfully
def test_empty_cart_success(setup_cart_with_item, mock_add_item_to_cart_db):
    setup_cart_with_item.empty_cart()
    assert setup_cart_with_item.items == []
    mock_add_item_to_cart_db.assert_called_with("DELETE FROM cart")


# edge case - add_item - Test adding an item with zero quantity
def test_add_item_zero_quantity(cart, mock_add_item_to_cart_db):
    cart.add_item(item_id=2, quantity=0, price=50, name='Mouse', category='Accessories', user_type='Regular')
    assert cart.items == [{'item_id': 2, 'quantity': 0, 'price': 50, 'name': 'Mouse', 'category': 'Accessories', 'user_type': 'Regular'}]
    mock_add_item_to_cart_db.assert_called_once_with("INSERT INTO cart (item_id, quantity, price, name, category, user_type) VALUES (2, 0, 50, 'Mouse', 'Accessories', 'Regular')")


# edge case - remove_item - Test removing an item not in the cart
def test_remove_item_not_in_cart(cart, mock_add_item_to_cart_db):
    cart.remove_item(item_id=99)
    assert cart.items == []
    mock_add_item_to_cart_db.assert_called_with("DELETE FROM cart WHERE item_id = 99")


# edge case - update_item_quantity - Test updating quantity of an item not in the cart
def test_update_item_quantity_not_in_cart(cart, mock_add_item_to_cart_db):
    cart.update_item_quantity(item_id=99, new_quantity=3)
    assert cart.items == []
    mock_add_item_to_cart_db.assert_called_with("UPDATE cart SET quantity = 3 WHERE item_id = 99")


# edge case - calculate_total_price - Test calculating total price of an empty cart
def test_calculate_total_price_empty_cart(cart):
    total_price = cart.calculate_total_price()
    assert total_price == 0


# edge case - list_items - Test listing items when cart is empty
def test_list_items_empty_cart(cart, capsys):
    cart.list_items()
    captured = capsys.readouterr()
    assert captured.out == ""


# edge case - empty_cart - Test emptying an already empty cart
def test_empty_cart_already_empty(cart, mock_add_item_to_cart_db):
    cart.empty_cart()
    assert cart.items == []
    mock_add_item_to_cart_db.assert_called_with("DELETE FROM cart")


