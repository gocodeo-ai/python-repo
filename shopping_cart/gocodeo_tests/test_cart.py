import pytest
from unittest.mock import patch, MagicMock
from shopping_cart.cart import Item, Cart
from shopping_cart.database import add_item_to_cart_db

@pytest.fixture
def cart_fixture():
    with patch('shopping_cart.database.add_item_to_cart_db') as mock_add_item_to_cart_db:
        mock_add_item_to_cart_db.return_value = None
        cart = Cart(user_type='regular')
        yield cart, mock_add_item_to_cart_db

@pytest.fixture
def item_fixture():
    item = Item(item_id=1, price=10.0, name='Apple', category='Fruit')
    return item

# happy path - add_item - Test that add_item adds an item with correct details to the cart and database.
def test_add_item_happy_path(cart_fixture):
    cart, mock_add_item_to_cart_db = cart_fixture
    cart.add_item(item_id=1, quantity=2, price=10.0, name='Apple', category='Fruit', user_type='regular')
    assert cart.items == [{'item_id': 1, 'quantity': 2, 'price': 10.0, 'name': 'Apple', 'category': 'Fruit', 'user_type': 'regular'}]
    mock_add_item_to_cart_db.assert_called_once_with("INSERT INTO cart (item_id, quantity, price, name, category, user_type) VALUES (1, 2, 10.0, 'Apple', 'Fruit', 'regular')")


# happy path - remove_item - Test that remove_item removes the correct item from the cart and database.
def test_remove_item_happy_path(cart_fixture):
    cart, mock_add_item_to_cart_db = cart_fixture
    cart.add_item(item_id=1, quantity=2, price=10.0, name='Apple', category='Fruit', user_type='regular')
    cart.remove_item(item_id=1)
    assert cart.items == []
    mock_add_item_to_cart_db.assert_called_with("DELETE FROM cart WHERE item_id = 1")


# happy path - update_item_quantity - Test that update_item_quantity updates the quantity of an item in the cart and database.
def test_update_item_quantity_happy_path(cart_fixture):
    cart, mock_add_item_to_cart_db = cart_fixture
    cart.add_item(item_id=1, quantity=2, price=10.0, name='Apple', category='Fruit', user_type='regular')
    cart.update_item_quantity(item_id=1, new_quantity=5)
    assert cart.items == [{'item_id': 1, 'quantity': 5, 'price': 10.0, 'name': 'Apple', 'category': 'Fruit', 'user_type': 'regular'}]
    mock_add_item_to_cart_db.assert_called_with("UPDATE cart SET quantity = 5 WHERE item_id = 1")


# happy path - calculate_total_price - Test that calculate_total_price calculates the total price correctly for multiple items.
def test_calculate_total_price_happy_path(cart_fixture):
    cart, _ = cart_fixture
    cart.add_item(item_id=1, quantity=2, price=10.0, name='Apple', category='Fruit', user_type='regular')
    cart.add_item(item_id=2, quantity=3, price=5.0, name='Banana', category='Fruit', user_type='regular')
    total_price = cart.calculate_total_price()
    assert total_price == 35.0


# happy path - list_items - Test that list_items prints all items in the cart with correct details.
def test_list_items_happy_path(cart_fixture, capsys):
    cart, _ = cart_fixture
    cart.add_item(item_id=1, quantity=2, price=10.0, name='Apple', category='Fruit', user_type='regular')
    cart.list_items()
    captured = capsys.readouterr()
    assert captured.out.strip() == "Item: Apple, Quantity: 2, Price per unit: 10.0"


# happy path - empty_cart - Test that empty_cart removes all items from the cart and database.
def test_empty_cart_happy_path(cart_fixture):
    cart, mock_add_item_to_cart_db = cart_fixture
    cart.add_item(item_id=1, quantity=2, price=10.0, name='Apple', category='Fruit', user_type='regular')
    cart.empty_cart()
    assert cart.items == []
    mock_add_item_to_cart_db.assert_called_with("DELETE FROM cart")


# edge case - add_item - Test that add_item handles adding an item with zero quantity gracefully.
def test_add_item_zero_quantity(cart_fixture):
    cart, mock_add_item_to_cart_db = cart_fixture
    cart.add_item(item_id=2, quantity=0, price=15.0, name='Banana', category='Fruit', user_type='regular')
    assert cart.items == [{'item_id': 2, 'quantity': 0, 'price': 15.0, 'name': 'Banana', 'category': 'Fruit', 'user_type': 'regular'}]
    mock_add_item_to_cart_db.assert_called_once_with("INSERT INTO cart (item_id, quantity, price, name, category, user_type) VALUES (2, 0, 15.0, 'Banana', 'Fruit', 'regular')")


# edge case - remove_item - Test that remove_item does not fail when removing an item not in the cart.
def test_remove_item_not_in_cart(cart_fixture):
    cart, mock_add_item_to_cart_db = cart_fixture
    cart.add_item(item_id=1, quantity=2, price=10.0, name='Apple', category='Fruit', user_type='regular')
    cart.remove_item(item_id=99)
    assert cart.items == [{'item_id': 1, 'quantity': 2, 'price': 10.0, 'name': 'Apple', 'category': 'Fruit', 'user_type': 'regular'}]
    mock_add_item_to_cart_db.assert_called_with("DELETE FROM cart WHERE item_id = 99")


# edge case - update_item_quantity - Test that update_item_quantity handles updating quantity to zero correctly.
def test_update_item_quantity_to_zero(cart_fixture):
    cart, mock_add_item_to_cart_db = cart_fixture
    cart.add_item(item_id=1, quantity=2, price=10.0, name='Apple', category='Fruit', user_type='regular')
    cart.update_item_quantity(item_id=1, new_quantity=0)
    assert cart.items == [{'item_id': 1, 'quantity': 0, 'price': 10.0, 'name': 'Apple', 'category': 'Fruit', 'user_type': 'regular'}]
    mock_add_item_to_cart_db.assert_called_with("UPDATE cart SET quantity = 0 WHERE item_id = 1")


# edge case - calculate_total_price - Test that calculate_total_price returns zero for an empty cart.
def test_calculate_total_price_empty_cart(cart_fixture):
    cart, _ = cart_fixture
    total_price = cart.calculate_total_price()
    assert total_price == 0.0


# edge case - list_items - Test that list_items handles an empty cart without errors.
def test_list_items_empty_cart(cart_fixture, capsys):
    cart, _ = cart_fixture
    cart.list_items()
    captured = capsys.readouterr()
    assert captured.out.strip() == ""


# edge case - empty_cart - Test that empty_cart does not fail when the cart is already empty.
def test_empty_cart_already_empty(cart_fixture):
    cart, mock_add_item_to_cart_db = cart_fixture
    cart.empty_cart()
    assert cart.items == []
    mock_add_item_to_cart_db.assert_called_with("DELETE FROM cart")


