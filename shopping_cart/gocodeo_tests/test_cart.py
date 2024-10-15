import pytest
from unittest import mock
from shopping_cart.cart import Item, Cart
from shopping_cart.database import add_item_to_cart_db

@pytest.fixture
def cart():
    return Cart(user_type='regular')

@pytest.fixture
def mock_add_item_to_cart_db(mocker):
    return mocker.patch('shopping_cart.database.add_item_to_cart_db')

@pytest.fixture
def mock_item():
    return Item(item_id=1, price=10.0, name='Apple', category='Fruit')

@pytest.fixture
def setup_cart_with_item(cart, mock_item, mock_add_item_to_cart_db):
    cart.add_item(mock_item.item_id, 2, mock_item.price, mock_item.name, mock_item.category, cart.user_type)
    return cart

# happy path - add_item - Test that adding an item updates the items list and database correctly
def test_add_item_updates_items_list_and_db(cart, mock_add_item_to_cart_db):
    cart.add_item(1, 2, 10.0, 'Apple', 'Fruit', 'regular')
    assert cart.items == [{'item_id': 1, 'quantity': 2, 'price': 10.0, 'name': 'Apple', 'category': 'Fruit', 'user_type': 'regular'}]
    mock_add_item_to_cart_db.assert_called_once_with("INSERT INTO cart (item_id, quantity, price, name, category, user_type) VALUES (1, 2, 10.0, 'Apple', 'Fruit', 'regular')")


# happy path - remove_item - Test that removing an item updates the items list and database correctly
def test_remove_item_updates_items_list_and_db(setup_cart_with_item, mock_add_item_to_cart_db):
    setup_cart_with_item.remove_item(1)
    assert setup_cart_with_item.items == []
    mock_add_item_to_cart_db.assert_called_with('DELETE FROM cart WHERE item_id = 1')


# happy path - update_item_quantity - Test that updating item quantity changes the quantity in items list and database
def test_update_item_quantity_changes_quantity_in_items_list_and_db(setup_cart_with_item, mock_add_item_to_cart_db):
    setup_cart_with_item.update_item_quantity(1, 5)
    assert setup_cart_with_item.items[0]['quantity'] == 5
    mock_add_item_to_cart_db.assert_called_with('UPDATE cart SET quantity = 5 WHERE item_id = 1')


# happy path - calculate_total_price - Test that calculating total price returns correct total
def test_calculate_total_price_returns_correct_total(setup_cart_with_item):
    total_price = setup_cart_with_item.calculate_total_price()
    assert total_price == 20.0


# happy path - list_items - Test that listing items outputs correct information
def test_list_items_outputs_correct_information(setup_cart_with_item, capsys):
    setup_cart_with_item.list_items()
    captured = capsys.readouterr()
    assert captured.out == 'Item: Apple, Quantity: 2, Price per unit: 10.0\n'


# happy path - empty_cart - Test that emptying the cart clears items and updates database
def test_empty_cart_clears_items_and_updates_db(setup_cart_with_item, mock_add_item_to_cart_db):
    setup_cart_with_item.empty_cart()
    assert setup_cart_with_item.items == []
    mock_add_item_to_cart_db.assert_called_with('DELETE FROM cart')


# edge case - add_item - Test that adding an item with zero quantity does not update the items list or database
def test_add_item_with_zero_quantity_does_not_update(cart, mock_add_item_to_cart_db):
    cart.add_item(2, 0, 5.0, 'Banana', 'Fruit', 'guest')
    assert cart.items == []
    mock_add_item_to_cart_db.assert_not_called()


# edge case - remove_item - Test that removing an item not in the cart does not change the items list or database
def test_remove_item_not_in_cart_does_not_change(cart, mock_add_item_to_cart_db):
    cart.remove_item(3)
    assert cart.items == []
    mock_add_item_to_cart_db.assert_not_called()


# edge case - update_item_quantity - Test that updating quantity for an item not in the cart does not change the items list or database
def test_update_quantity_for_item_not_in_cart_does_not_change(cart, mock_add_item_to_cart_db):
    cart.update_item_quantity(4, 3)
    assert cart.items == []
    mock_add_item_to_cart_db.assert_not_called()


# edge case - calculate_total_price - Test that calculating total price for empty cart returns zero
def test_calculate_total_price_for_empty_cart_returns_zero(cart):
    total_price = cart.calculate_total_price()
    assert total_price == 0.0


# edge case - list_items - Test that listing items for empty cart outputs nothing
def test_list_items_for_empty_cart_outputs_nothing(cart, capsys):
    cart.list_items()
    captured = capsys.readouterr()
    assert captured.out == ''


# edge case - empty_cart - Test that emptying an already empty cart does not affect database
def test_emptying_already_empty_cart_does_not_affect_db(cart, mock_add_item_to_cart_db):
    cart.empty_cart()
    assert cart.items == []
    mock_add_item_to_cart_db.assert_called_with('DELETE FROM cart')


