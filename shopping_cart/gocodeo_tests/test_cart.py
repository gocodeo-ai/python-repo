import pytest
from unittest.mock import patch, MagicMock
from shopping_cart.database import add_item_to_cart_db
from shopping_cart.cart import Cart, Item

@pytest.fixture
def mock_database():
    with patch('shopping_cart.database.add_item_to_cart_db') as mock_db:
        yield mock_db

@pytest.fixture
def cart():
    return Cart(user_type='regular')

@pytest.fixture
def item():
    return Item(item_id=1, price=10.0, name='Apple', category='Fruit')

@pytest.fixture
def mock_add_item_to_cart_db():
    with patch('shopping_cart.database.add_item_to_cart_db') as mock_db:
        yield mock_db

@pytest.fixture
def setup_cart_with_items(cart, item):
    cart.add_item(item_id=item.item_id, quantity=2, price=item.price, name=item.name, category=item.category, user_type=cart.user_type)
    return cart

@pytest.fixture
def mock_print():
    with patch('builtins.print') as mock_print:
        yield mock_print

# happy_path - test_add_item_successfully - Test that an item is successfully added to the cart.
def test_add_item_successfully(cart, item, mock_add_item_to_cart_db):
    cart.add_item(item_id=item.item_id, quantity=2, price=item.price, name=item.name, category=item.category, user_type=cart.user_type)
    assert cart.items == [{'item_id': 1, 'quantity': 2, 'price': 10.0, 'name': 'Apple', 'category': 'Fruit', 'user_type': 'regular'}]
    mock_add_item_to_cart_db.assert_called_once()

# happy_path - test_remove_item_successfully - Test that an item is successfully removed from the cart.
def test_remove_item_successfully(setup_cart_with_items, mock_add_item_to_cart_db):
    setup_cart_with_items.remove_item(item_id=1)
    assert setup_cart_with_items.items == []
    mock_add_item_to_cart_db.assert_called_once()

# happy_path - test_update_item_quantity_successfully - Test that the item quantity is successfully updated in the cart.
def test_update_item_quantity_successfully(setup_cart_with_items, mock_add_item_to_cart_db):
    setup_cart_with_items.update_item_quantity(item_id=1, new_quantity=5)
    assert setup_cart_with_items.items == [{'item_id': 1, 'quantity': 5, 'price': 10.0, 'name': 'Apple', 'category': 'Fruit', 'user_type': 'regular'}]
    mock_add_item_to_cart_db.assert_called_once()

# happy_path - test_calculate_total_price_successfully - Test that the total price is calculated correctly for items in the cart.
def test_calculate_total_price_successfully(setup_cart_with_items):
    total_price = setup_cart_with_items.calculate_total_price()
    assert total_price == 20.0

# happy_path - test_list_items_successfully - Test that all items are listed correctly from the cart.
def test_list_items_successfully(setup_cart_with_items, mock_print):
    setup_cart_with_items.list_items()
    mock_print.assert_called_once_with('Item: Apple, Quantity: 2, Price per unit: 10.0')

# happy_path - test_empty_cart_successfully - Test that the cart is successfully emptied.
def test_empty_cart_successfully(setup_cart_with_items, mock_add_item_to_cart_db):
    setup_cart_with_items.empty_cart()
    assert setup_cart_with_items.items == []
    mock_add_item_to_cart_db.assert_called_once()

# happy_path - test_add_item_valid - Test that adding a valid item updates the items list and database correctly.
def test_add_item_valid(cart, item, mock_add_item_to_cart_db):
    cart.add_item(item_id=item.item_id, quantity=2, price=item.price, name=item.name, category=item.category, user_type=cart.user_type)
    assert cart.items == [{'item_id': 1, 'quantity': 2, 'price': 10.0, 'name': 'Apple', 'category': 'Fruit', 'user_type': 'regular'}]
    mock_add_item_to_cart_db.assert_called_once()

# happy_path - test_remove_item_existing - Test that removing an existing item updates the items list and database correctly.
def test_remove_item_existing(setup_cart_with_items, mock_add_item_to_cart_db):
    setup_cart_with_items.remove_item(item_id=1)
    assert setup_cart_with_items.items == []
    mock_add_item_to_cart_db.assert_called_once()

# happy_path - test_update_item_quantity_existing - Test that updating the quantity of an existing item reflects correctly in the items list and database.
def test_update_item_quantity_existing(setup_cart_with_items, mock_add_item_to_cart_db):
    setup_cart_with_items.update_item_quantity(item_id=1, new_quantity=5)
    assert setup_cart_with_items.items == [{'item_id': 1, 'quantity': 5, 'price': 10.0, 'name': 'Apple', 'category': 'Fruit', 'user_type': 'regular'}]
    mock_add_item_to_cart_db.assert_called_once()

# happy_path - test_calculate_total_price_multiple_items - Test that calculating total price returns the correct sum for multiple items.
def test_calculate_total_price_multiple_items(cart):
    cart.items = [{'item_id': 1, 'quantity': 2, 'price': 10.0}, {'item_id': 2, 'quantity': 3, 'price': 5.0}]
    total_price = cart.calculate_total_price()
    assert total_price == 35.0

# happy_path - test_list_items_correct_details - Test that listing items displays all items with correct details.
def test_list_items_correct_details(cart, mock_print):
    cart.items = [{'item_id': 1, 'quantity': 2, 'price': 10.0, 'name': 'Apple'}]
    cart.list_items()
    mock_print.assert_called_once_with('Item: Apple, Quantity: 2, Price per unit: 10.0')

# happy_path - test_empty_cart_clears_items - Test that emptying the cart clears all items and updates the database.
def test_empty_cart_clears_items(setup_cart_with_items, mock_add_item_to_cart_db):
    setup_cart_with_items.empty_cart()
    assert setup_cart_with_items.items == []
    mock_add_item_to_cart_db.assert_called_once()

# happy_path - test_add_item_success - Test that an item is added to the cart successfully with correct details.
def test_add_item_success(cart, item, mock_add_item_to_cart_db):
    cart.add_item(item_id=item.item_id, quantity=2, price=item.price, name=item.name, category=item.category, user_type=cart.user_type)
    assert cart.items == [{'item_id': 1, 'quantity': 2, 'price': 10.0, 'name': 'Apple', 'category': 'Fruit', 'user_type': 'regular'}]
    mock_add_item_to_cart_db.assert_called_once()

# happy_path - test_remove_item_success - Test that an item is removed from the cart successfully.
def test_remove_item_success(setup_cart_with_items, mock_add_item_to_cart_db):
    setup_cart_with_items.remove_item(item_id=1)
    assert setup_cart_with_items.items == []
    mock_add_item_to_cart_db.assert_called_once()

# happy_path - test_update_item_quantity_success - Test that item quantity is updated correctly in the cart.
def test_update_item_quantity_success(setup_cart_with_items, mock_add_item_to_cart_db):
    setup_cart_with_items.update_item_quantity(item_id=1, new_quantity=5)
    assert setup_cart_with_items.items == [{'item_id': 1, 'quantity': 5, 'price': 10.0, 'name': 'Apple', 'category': 'Fruit', 'user_type': 'regular'}]
    mock_add_item_to_cart_db.assert_called_once()

# happy_path - test_calculate_total_price_success - Test that total price is calculated correctly for items in the cart.
def test_calculate_total_price_success(setup_cart_with_items):
    total_price = setup_cart_with_items.calculate_total_price()
    assert total_price == 50.0

# happy_path - test_list_items_success - Test that all items in the cart are listed correctly.
def test_list_items_success(setup_cart_with_items, mock_print):
    setup_cart_with_items.list_items()
    mock_print.assert_called_once_with('Item: Apple, Quantity: 2, Price per unit: 10.0')

# happy_path - test_empty_cart_success - Test that the cart is emptied successfully.
def test_empty_cart_success(setup_cart_with_items, mock_add_item_to_cart_db):
    setup_cart_with_items.empty_cart()
    assert setup_cart_with_items.items == []
    mock_add_item_to_cart_db.assert_called_once()

# happy_path - test_add_item_success - Test that an item is added to the cart with valid details
def test_add_item_success(cart, item, mock_add_item_to_cart_db):
    cart.add_item(item_id=item.item_id, quantity=2, price=100.0, name='Book', category='Education', user_type='Regular')
    assert cart.items == [{'item_id': 1, 'quantity': 2, 'price': 100.0, 'name': 'Book', 'category': 'Education', 'user_type': 'Regular'}]
    mock_add_item_to_cart_db.assert_called_once()

# happy_path - test_remove_item_success - Test that an item is removed from the cart successfully
def test_remove_item_success(setup_cart_with_items, mock_add_item_to_cart_db):
    setup_cart_with_items.remove_item(item_id=1)
    assert setup_cart_with_items.items == []
    mock_add_item_to_cart_db.assert_called_once()

# happy_path - test_update_item_quantity_success - Test that the quantity of an item is updated successfully
def test_update_item_quantity_success(setup_cart_with_items, mock_add_item_to_cart_db):
    setup_cart_with_items.update_item_quantity(item_id=1, new_quantity=5)
    assert setup_cart_with_items.items == [{'item_id': 1, 'quantity': 5, 'price': 10.0, 'name': 'Apple', 'category': 'Fruit', 'user_type': 'regular'}]
    mock_add_item_to_cart_db.assert_called_once()

# happy_path - test_calculate_total_price_success - Test that the total price is calculated correctly
def test_calculate_total_price_success(setup_cart_with_items):
    total_price = setup_cart_with_items.calculate_total_price()
    assert total_price == 500.0

# happy_path - test_list_items_success - Test that all items in the cart are listed
def test_list_items_success(setup_cart_with_items, mock_print):
    setup_cart_with_items.list_items()
    mock_print.assert_called_once_with('Item: Apple, Quantity: 2, Price per unit: 10.0')

# happy_path - test_empty_cart_success - Test that the cart is emptied successfully
def test_empty_cart_success(setup_cart_with_items, mock_add_item_to_cart_db):
    setup_cart_with_items.empty_cart()
    assert setup_cart_with_items.items == []
    mock_add_item_to_cart_db.assert_called_once()

# happy_path - test_add_item_happy_path - Test that add_item correctly adds a new item to the cart with given details.
def test_add_item_happy_path(cart, item, mock_add_item_to_cart_db):
    cart.add_item(item_id=item.item_id, quantity=2, price=100.0, name='Laptop', category='Electronics', user_type='regular')
    assert cart.items == [{'item_id': 1, 'quantity': 2, 'price': 100.0, 'name': 'Laptop', 'category': 'Electronics', 'user_type': 'regular'}]
    mock_add_item_to_cart_db.assert_called_once()

# happy_path - test_remove_item_happy_path - Test that remove_item successfully removes an item from the cart by item_id.
def test_remove_item_happy_path(setup_cart_with_items, mock_add_item_to_cart_db):
    setup_cart_with_items.remove_item(item_id=1)
    assert setup_cart_with_items.items == []
    mock_add_item_to_cart_db.assert_called_once()

# happy_path - test_update_item_quantity_happy_path - Test that update_item_quantity updates the quantity of an existing item in the cart.
def test_update_item_quantity_happy_path(setup_cart_with_items, mock_add_item_to_cart_db):
    setup_cart_with_items.update_item_quantity(item_id=1, new_quantity=5)
    assert setup_cart_with_items.items == [{'item_id': 1, 'quantity': 5, 'price': 10.0, 'name': 'Apple', 'category': 'Fruit', 'user_type': 'regular'}]
    mock_add_item_to_cart_db.assert_called_once()

# happy_path - test_calculate_total_price_happy_path - Test that calculate_total_price returns the correct total price of all items in the cart.
def test_calculate_total_price_happy_path(setup_cart_with_items):
    total_price = setup_cart_with_items.calculate_total_price()
    assert total_price == 500.0

# happy_path - test_list_items_happy_path - Test that list_items prints the correct list of items in the cart.
def test_list_items_happy_path(setup_cart_with_items, mock_print):
    setup_cart_with_items.list_items()
    mock_print.assert_called_once_with('Item: Apple, Quantity: 2, Price per unit: 10.0')

# happy_path - test_empty_cart_happy_path - Test that empty_cart removes all items from the cart.
def test_empty_cart_happy_path(setup_cart_with_items, mock_add_item_to_cart_db):
    setup_cart_with_items.empty_cart()
    assert setup_cart_with_items.items == []
    mock_add_item_to_cart_db.assert_called_once()

# happy_path - test_add_item_success - Test that an item is added successfully to the cart with valid details.
def test_add_item_success(cart, item, mock_add_item_to_cart_db):
    cart.add_item(item_id=item.item_id, quantity=2, price=100, name='Laptop', category='Electronics', user_type='regular')
    assert cart.items == [{'item_id': 1, 'quantity': 2, 'price': 100, 'name': 'Laptop', 'category': 'Electronics', 'user_type': 'regular'}]
    mock_add_item_to_cart_db.assert_called_once()

# happy_path - test_remove_item_success - Test that an item is removed successfully from the cart when it exists.
def test_remove_item_success(setup_cart_with_items, mock_add_item_to_cart_db):
    setup_cart_with_items.remove_item(item_id=1)
    assert setup_cart_with_items.items == []
    mock_add_item_to_cart_db.assert_called_once()

# happy_path - test_update_item_quantity_success - Test that the quantity of an item is updated successfully.
def test_update_item_quantity_success(setup_cart_with_items, mock_add_item_to_cart_db):
    setup_cart_with_items.update_item_quantity(item_id=1, new_quantity=5)
    assert setup_cart_with_items.items == [{'item_id': 1, 'quantity': 5, 'price': 10.0, 'name': 'Apple', 'category': 'Fruit', 'user_type': 'regular'}]
    mock_add_item_to_cart_db.assert_called_once()

# happy_path - test_calculate_total_price - Test that the total price is calculated correctly for items in the cart.
def test_calculate_total_price(setup_cart_with_items):
    total_price = setup_cart_with_items.calculate_total_price()
    assert total_price == 200

# happy_path - test_list_items - Test that listing items displays the correct information for each item in the cart.
def test_list_items(setup_cart_with_items, mock_print):
    setup_cart_with_items.list_items()
    mock_print.assert_called_once_with('Item: Apple, Quantity: 2, Price per unit: 10.0')

# happy_path - test_empty_cart - Test that the cart is emptied successfully.
def test_empty_cart(setup_cart_with_items, mock_add_item_to_cart_db):
    setup_cart_with_items.empty_cart()
    assert setup_cart_with_items.items == []
    mock_add_item_to_cart_db.assert_called_once()

# happy_path - test_add_item_happy_path - Test that add_item adds an item to the cart with correct details.
def test_add_item_happy_path(cart, item, mock_add_item_to_cart_db):
    cart.add_item(item_id=item.item_id, quantity=2, price=10.0, name=item.name, category=item.category, user_type=cart.user_type)
    assert cart.items == [{'item_id': 1, 'quantity': 2, 'price': 10.0, 'name': 'Apple', 'category': 'Fruit', 'user_type': 'regular'}]
    mock_add_item_to_cart_db.assert_called_once()

# happy_path - test_remove_item_happy_path - Test that remove_item removes an existing item from the cart.
def test_remove_item_happy_path(setup_cart_with_items, mock_add_item_to_cart_db):
    setup_cart_with_items.remove_item(item_id=1)
    assert setup_cart_with_items.items == []
    mock_add_item_to_cart_db.assert_called_once()

# happy_path - test_update_item_quantity_happy_path - Test that update_item_quantity updates the quantity of an existing item correctly.
def test_update_item_quantity_happy_path(setup_cart_with_items, mock_add_item_to_cart_db):
    setup_cart_with_items.update_item_quantity(item_id=1, new_quantity=5)
    assert setup_cart_with_items.items == [{'item_id': 1, 'quantity': 5, 'price': 10.0, 'name': 'Apple', 'category': 'Fruit', 'user_type': 'regular'}]
    mock_add_item_to_cart_db.assert_called_once()

# happy_path - test_calculate_total_price_happy_path - Test that calculate_total_price returns the correct total price for items in the cart.
def test_calculate_total_price_happy_path(setup_cart_with_items):
    total_price = setup_cart_with_items.calculate_total_price()
    assert total_price == 20.0

# happy_path - test_list_items_happy_path - Test that list_items prints all items in the cart.
def test_list_items_happy_path(setup_cart_with_items, mock_print):
    setup_cart_with_items.list_items()
    mock_print.assert_called_once_with('Item: Apple, Quantity: 2, Price per unit: 10.0')

# happy_path - test_empty_cart_happy_path - Test that empty_cart clears all items from the cart.
def test_empty_cart_happy_path(setup_cart_with_items, mock_add_item_to_cart_db):
    setup_cart_with_items.empty_cart()
    assert setup_cart_with_items.items == []
    mock_add_item_to_cart_db.assert_called_once()

# happy_path - test_add_item_valid - Test that an item can be added to the cart with valid details.
def test_add_item_valid(cart, item, mock_add_item_to_cart_db):
    cart.add_item(item_id=item.item_id, quantity=2, price=item.price, name=item.name, category=item.category, user_type=cart.user_type)
    assert cart.items == [{'item_id': 1, 'quantity': 2, 'price': 10.0, 'name': 'Apple', 'category': 'Fruit', 'user_type': 'regular'}]
    mock_add_item_to_cart_db.assert_called_once()

# happy_path - test_remove_item_exists - Test that an item can be removed from the cart when it exists.
def test_remove_item_exists(setup_cart_with_items, mock_add_item_to_cart_db):
    setup_cart_with_items.remove_item(item_id=1)
    assert setup_cart_with_items.items == []
    mock_add_item_to_cart_db.assert_called_once()

# happy_path - test_update_item_quantity_exists - Test that the quantity of an existing item can be updated.
def test_update_item_quantity_exists(setup_cart_with_items, mock_add_item_to_cart_db):
    setup_cart_with_items.update_item_quantity(item_id=1, new_quantity=5)
    assert setup_cart_with_items.items == [{'item_id': 1, 'quantity': 5, 'price': 10.0, 'name': 'Apple', 'category': 'Fruit', 'user_type': 'regular'}]
    mock_add_item_to_cart_db.assert_called_once()

# happy_path - test_calculate_total_price_multiple - Test that the total price is calculated correctly for multiple items.
def test_calculate_total_price_multiple(cart):
    cart.items = [{'item_id': 1, 'quantity': 2, 'price': 10.0}, {'item_id': 2, 'quantity': 3, 'price': 10.0}]
    total_price = cart.calculate_total_price()
    assert total_price == 50.0

# happy_path - test_list_items - Test that all items in the cart are listed correctly.
def test_list_items(cart, mock_print):
    cart.items = [{'item_id': 1, 'quantity': 2, 'price': 10.0, 'name': 'Apple', 'category': 'Fruit'}]
    cart.list_items()
    mock_print.assert_called_once_with('Item: Apple, Quantity: 2, Price per unit: 10.0')

# happy_path - test_empty_cart - Test that the cart is emptied successfully.
def test_empty_cart(setup_cart_with_items, mock_add_item_to_cart_db):
    setup_cart_with_items.empty_cart()
    assert setup_cart_with_items.items == []
    mock_add_item_to_cart_db.assert_called_once()

# happy_path - test_add_item_valid - Test that adding a valid item to the cart updates the cart's item list and database.
def test_add_item_valid(cart, item, mock_add_item_to_cart_db):
    cart.add_item(item_id=item.item_id, quantity=2, price=item.price, name=item.name, category=item.category, user_type=cart.user_type)
    assert cart.items == [{'item_id': 1, 'quantity': 2, 'price': 10.0, 'name': 'Apple', 'category': 'Fruit', 'user_type': 'regular'}]
    mock_add_item_to_cart_db.assert_called_once()

# happy_path - test_remove_existing_item - Test that removing an existing item decreases the cart's item list size and updates the database.
def test_remove_existing_item(setup_cart_with_items, mock_add_item_to_cart_db):
    setup_cart_with_items.remove_item(item_id=1)
    assert setup_cart_with_items.items == []
    mock_add_item_to_cart_db.assert_called_once()

# happy_path - test_update_item_quantity - Test that updating the quantity of an existing item reflects the change in the cart and database.
def test_update_item_quantity(setup_cart_with_items, mock_add_item_to_cart_db):
    setup_cart_with_items.update_item_quantity(item_id=1, new_quantity=5)
    assert setup_cart_with_items.items == [{'item_id': 1, 'quantity': 5, 'price': 10.0, 'name': 'Apple', 'category': 'Fruit', 'user_type': 'regular'}]
    mock_add_item_to_cart_db.assert_called_once()

# happy_path - test_calculate_total_price - Test that calculating total price returns the correct sum based on items in the cart.
def test_calculate_total_price(setup_cart_with_items):
    total_price = setup_cart_with_items.calculate_total_price()
    assert total_price == 50.0

# happy_path - test_list_items - Test that listing items prints the correct details for each item in the cart.
def test_list_items(setup_cart_with_items, mock_print):
    setup_cart_with_items.list_items()
    mock_print.assert_called_once_with('Item: Apple, Quantity: 2, Price per unit: 10.0')

# happy_path - test_empty_cart - Test that emptying the cart clears all items and updates the database.
def test_empty_cart(setup_cart_with_items, mock_add_item_to_cart_db):
    setup_cart_with_items.empty_cart()
    assert setup_cart_with_items.items == []
    mock_add_item_to_cart_db.assert_called_once()

# happy_path - test_remove_item_success - Test that an item is successfully removed from the cart when it exists.
def test_remove_item_success(setup_cart_with_items, mock_add_item_to_cart_db):
    setup_cart_with_items.remove_item(item_id=1)
    assert setup_cart_with_items.items == []
    mock_add_item_to_cart_db.assert_called_once()

# happy_path - test_update_item_quantity_success - Test that the quantity of an existing item is successfully updated in the cart.
def test_update_item_quantity_success(setup_cart_with_items, mock_add_item_to_cart_db):
    setup_cart_with_items.update_item_quantity(item_id=1, new_quantity=5)
    assert setup_cart_with_items.items == [{'item_id': 1, 'quantity': 5, 'price': 10.0, 'name': 'Apple', 'category': 'Fruit', 'user_type': 'regular'}]
    mock_add_item_to_cart_db.assert_called_once()

# happy_path - test_calculate_total_price_success - Test that the total price is correctly calculated for all items in the cart.
def test_calculate_total_price_success(setup_cart_with_items):
    total_price = setup_cart_with_items.calculate_total_price()
    assert total_price == 50.0

# happy_path - test_list_items_success - Test that all items in the cart are listed with correct details.
def test_list_items_success(setup_cart_with_items, mock_print):
    setup_cart_with_items.list_items()
    mock_print.assert_called_once_with('Item: Apple, Quantity: 2, Price per unit: 10.0')

# happy_path - test_empty_cart_success - Test that the cart is emptied successfully.
def test_empty_cart_success(setup_cart_with_items, mock_add_item_to_cart_db):
    setup_cart_with_items.empty_cart()
    assert setup_cart_with_items.items == []
    mock_add_item_to_cart_db.assert_called_once()

# happy_path - test_add_item_successfully - Test that an item is successfully added to the cart.
def test_add_item_successfully(cart, item, mock_add_item_to_cart_db):
    cart.add_item(item_id=item.item_id, quantity=2, price=item.price, name=item.name, category=item.category, user_type=cart.user_type)
    assert cart.items == [{'item_id': 1, 'quantity': 2, 'price': 10.0, 'name': 'Apple', 'category': 'Fruit', 'user_type': 'regular'}]
    mock_add_item_to_cart_db.assert_called_once()

# happy_path - test_remove_item_successfully - Test that an item is successfully removed from the cart.
def test_remove_item_successfully(setup_cart_with_items, mock_add_item_to_cart_db):
    setup_cart_with_items.remove_item(item_id=1)
    assert setup_cart_with_items.items == []
    mock_add_item_to_cart_db.assert_called_once()

# happy_path - test_update_item_quantity_successfully - Test that the item quantity is successfully updated in the cart.
def test_update_item_quantity_successfully(setup_cart_with_items, mock_add_item_to_cart_db):
    setup_cart_with_items.update_item_quantity(item_id=1, new_quantity=5)
    assert setup_cart_with_items.items == [{'item_id': 1, 'quantity': 5, 'price': 10.0, 'name': 'Apple', 'category': 'Fruit', 'user_type': 'regular'}]
    mock_add_item_to_cart_db.assert_called_once()

# happy_path - test_calculate_total_price_successfully - Test that the total price is calculated correctly for items in the cart.
def test_calculate_total_price_successfully(setup_cart_with_items):
    total_price = setup_cart_with_items.calculate_total_price()
    assert total_price == 20.0

# happy_path - test_list_items_successfully - Test that all items are listed correctly from the cart.
def test_list_items_successfully(setup_cart_with_items, mock_print):
    setup_cart_with_items.list_items()
    mock_print.assert_called_once_with('Item: Apple, Quantity: 2, Price per unit: 10.0')

# happy_path - test_empty_cart_successfully - Test that the cart is successfully emptied.
def test_empty_cart_successfully(setup_cart_with_items, mock_add_item_to_cart_db):
    setup_cart_with_items.empty_cart()
    assert setup_cart_with_items.items == []
    mock_add_item_to_cart_db.assert_called_once()

# happy_path - test_add_item_valid - Test that adding a valid item updates the items list and database correctly.
def test_add_item_valid(cart, item, mock_add_item_to_cart_db):
    cart.add_item(item_id=item.item_id, quantity=2, price=item.price, name=item.name, category=item.category, user_type=cart.user_type)
    assert cart.items == [{'item_id': 1, 'quantity': 2, 'price': 10.0, 'name': 'Apple', 'category': 'Fruit', 'user_type': 'regular'}]
    mock_add_item_to_cart_db.assert_called_once()

# happy_path - test_remove_item_existing - Test that removing an existing item updates the items list and database correctly.
def test_remove_item_existing(setup_cart_with_items, mock_add_item_to_cart_db):
    setup_cart_with_items.remove_item(item_id=1)
    assert setup_cart_with_items.items == []
    mock_add_item_to_cart_db.assert_called_once()

# happy_path - test_update_item_quantity_existing - Test that updating the quantity of an existing item reflects correctly in the items list and database.
def test_update_item_quantity_existing(setup_cart_with_items, mock_add_item_to_cart_db):
    setup_cart_with_items.update_item_quantity(item_id=1, new_quantity=5)
    assert setup_cart_with_items.items == [{'item_id': 1, 'quantity': 5, 'price': 10.0, 'name': 'Apple', 'category': 'Fruit', 'user_type': 'regular'}]
    mock_add_item_to_cart_db.assert_called_once()

# happy_path - test_calculate_total_price_multiple_items - Test that calculating total price returns the correct sum for multiple items.
def test_calculate_total_price_multiple_items(cart):
    cart.items = [{'item_id': 1, 'quantity': 2, 'price': 10.0}, {'item_id': 2, 'quantity': 3, 'price': 5.0}]
    total_price = cart.calculate_total_price()
    assert total_price == 35.0

# happy_path - test_list_items_correct_details - Test that listing items displays all items with correct details.
def test_list_items_correct_details(cart, mock_print):
    cart.items = [{'item_id': 1, 'quantity': 2, 'price': 10.0, 'name': 'Apple'}]
    cart.list_items()
    mock_print.assert_called_once_with('Item: Apple, Quantity: 2, Price per unit: 10.0')

# happy_path - test_empty_cart_clears_items - Test that emptying the cart clears all items and updates the database.
def test_empty_cart_clears_items(setup_cart_with_items, mock_add_item_to_cart_db):
    setup_cart_with_items.empty_cart()
    assert setup_cart_with_items.items == []
    mock_add_item_to_cart_db.assert_called_once()

# happy_path - test_add_item_success - Test that an item is added to the cart successfully with correct details.
def test_add_item_success(cart, item, mock_add_item_to_cart_db):
    cart.add_item(item_id=item.item_id, quantity=2, price=item.price, name=item.name, category=item.category, user_type=cart.user_type)
    assert cart.items == [{'item_id': 1, 'quantity': 2, 'price': 10.0, 'name': 'Apple', 'category': 'Fruit', 'user_type': 'regular'}]
    mock_add_item_to_cart_db.assert_called_once()

# happy_path - test_remove_item_success - Test that an item is removed from the cart successfully.
def test_remove_item_success(setup_cart_with_items, mock_add_item_to_cart_db):
    setup_cart_with_items.remove_item(item_id=1)
    assert setup_cart_with_items.items == []
    mock_add_item_to_cart_db.assert_called_once()

# happy_path - test_update_item_quantity_success - Test that item quantity is updated correctly in the cart.
def test_update_item_quantity_success(setup_cart_with_items, mock_add_item_to_cart_db):
    setup_cart_with_items.update_item_quantity(item_id=1, new_quantity=5)
    assert setup_cart_with_items.items == [{'item_id': 1, 'quantity': 5, 'price': 10.0, 'name': 'Apple', 'category': 'Fruit', 'user_type': 'regular'}]
    mock_add_item_to_cart_db.assert_called_once()

# happy_path - test_calculate_total_price_success - Test that total price is calculated correctly for items in the cart.
def test_calculate_total_price_success(setup_cart_with_items):
    total_price = setup_cart_with_items.calculate_total_price()
    assert total_price == 50.0

# happy_path - test_list_items_success - Test that all items in the cart are listed correctly.
def test_list_items_success(setup_cart_with_items, mock_print):
    setup_cart_with_items.list_items()
    mock_print.assert_called_once_with('Item: Apple, Quantity: 2, Price per unit: 10.0')

# happy_path - test_empty_cart_success - Test that the cart is emptied successfully.
def test_empty_cart_success(setup_cart_with_items, mock_add_item_to_cart_db):
    setup_cart_with_items.empty_cart()
    assert setup_cart_with_items.items == []
    mock_add_item_to_cart_db.assert_called_once()

# happy_path - test_add_item_success - Test that an item is added to the cart with valid details
def test_add_item_success(cart, item, mock_add_item_to_cart_db):
    cart.add_item(item_id=item.item_id, quantity=2, price=100.0, name='Book', category='Education', user_type='Regular')
    assert cart.items == [{'item_id': 1, 'quantity': 2, 'price': 100.0, 'name': 'Book', 'category': 'Education', 'user_type': 'Regular'}]
    mock_add_item_to_cart_db.assert_called_once()

# happy_path - test_remove_item_success - Test that an item is removed from the cart successfully
def test_remove_item_success(setup_cart_with_items, mock_add_item_to_cart_db):
    setup_cart_with_items.remove_item(item_id=1)
    assert setup_cart_with_items.items == []
    mock_add_item_to_cart_db.assert_called_once()

# happy_path - test_update_item_quantity_success - Test that the quantity of an item is updated successfully
def test_update_item_quantity_success(setup_cart_with_items, mock_add_item_to_cart_db):
    setup_cart_with_items.update_item_quantity(item_id=1, new_quantity=5)
    assert setup_cart_with_items.items == [{'item_id': 1, 'quantity': 5, 'price': 10.0, 'name': 'Apple', 'category': 'Fruit', 'user_type': 'regular'}]
    mock_add_item_to_cart_db.assert_called_once()

# happy_path - test_calculate_total_price_success - Test that the total price is calculated correctly
def test_calculate_total_price_success(setup_cart_with_items):
    total_price = setup_cart_with_items.calculate_total_price()
    assert total_price == 500.0

# happy_path - test_list_items_success - Test that all items in the cart are listed
def test_list_items_success(setup_cart_with_items, mock_print):
    setup_cart_with_items.list_items()
    mock_print.assert_called_once_with('Item: Apple, Quantity: 2, Price per unit: 10.0')

# happy_path - test_empty_cart_success - Test that the cart is emptied successfully
def test_empty_cart_success(setup_cart_with_items, mock_add_item_to_cart_db):
    setup_cart_with_items.empty_cart()
    assert setup_cart_with_items.items == []
    mock_add_item_to_cart_db.assert_called_once()

# happy_path - test_add_item_happy_path - Test that add_item correctly adds a new item to the cart with given details.
def test_add_item_happy_path(cart, item, mock_add_item_to_cart_db):
    cart.add_item(item_id=item.item_id, quantity=2, price=100.0, name='Laptop', category='Electronics', user_type='regular')
    assert cart.items == [{'item_id': 1, 'quantity': 2, 'price': 100.0, 'name': 'Laptop', 'category': 'Electronics', 'user_type': 'regular'}]
    mock_add_item_to_cart_db.assert_called_once()

# happy_path - test_remove_item_happy_path - Test that remove_item successfully removes an item from the cart by item_id.
def test_remove_item_happy_path(setup_cart_with_items, mock_add_item_to_cart_db):
    setup_cart_with_items.remove_item(item_id=1)
    assert setup_cart_with_items.items == []
    mock_add_item_to_cart_db.assert_called_once()

# happy_path - test_update_item_quantity_happy_path - Test that update_item_quantity updates the quantity of an existing item in the cart.
def test_update_item_quantity_happy_path(setup_cart_with_items, mock_add_item_to_cart_db):
    setup_cart_with_items.update_item_quantity(item_id=1, new_quantity=5)
    assert setup_cart_with_items.items == [{'item_id': 1, 'quantity': 5, 'price': 10.0, 'name': 'Apple', 'category': 'Fruit', 'user_type': 'regular'}]
    mock_add_item_to_cart_db.assert_called_once()

# happy_path - test_calculate_total_price_happy_path - Test that calculate_total_price returns the correct total price of all items in the cart.
def test_calculate_total_price_happy_path(setup_cart_with_items):
    total_price = setup_cart_with_items.calculate_total_price()
    assert total_price == 500.0

# happy_path - test_list_items_happy_path - Test that list_items prints the correct list of items in the cart.
def test_list_items_happy_path(setup_cart_with_items, mock_print):
    setup_cart_with_items.list_items()
    mock_print.assert_called_once_with('Item: Apple, Quantity: 2, Price per unit: 10.0')

# happy_path - test_empty_cart_happy_path - Test that empty_cart removes all items from the cart.
def test_empty_cart_happy_path(setup_cart_with_items, mock_add_item_to_cart_db):
    setup_cart_with_items.empty_cart()
    assert setup_cart_with_items.items == []
    mock_add_item_to_cart_db.assert_called_once()

# happy_path - test_add_item_success - Test that an item is added successfully to the cart with valid details.
def test_add_item_success(cart, item, mock_add_item_to_cart_db):
    cart.add_item(item_id=item.item_id, quantity=2, price=100, name='Laptop', category='Electronics', user_type='regular')
    assert cart.items == [{'item_id': 1, 'quantity': 2, 'price': 100, 'name': 'Laptop', 'category': 'Electronics', 'user_type': 'regular'}]
    mock_add_item_to_cart_db.assert_called_once()

# happy_path - test_remove_item_success - Test that an item is removed successfully from the cart when it exists.
def test_remove_item_success(setup_cart_with_items, mock_add_item_to_cart_db):
    setup_cart_with_items.remove_item(item_id=1)
    assert setup_cart_with_items.items == []
    mock_add_item_to_cart_db.assert_called_once()

# happy_path - test_update_item_quantity_success - Test that the quantity of an item is updated successfully.
def test_update_item_quantity_success(setup_cart_with_items, mock_add_item_to_cart_db):
    setup_cart_with_items.update_item_quantity(item_id=1, new_quantity=5)
    assert setup_cart_with_items.items == [{'item_id': 1, 'quantity': 5, 'price': 10.0, 'name': 'Apple', 'category': 'Fruit', 'user_type': 'regular'}]
    mock_add_item_to_cart_db.assert_called_once()

# happy_path - test_calculate_total_price - Test that the total price is calculated correctly for items in the cart.
def test_calculate_total_price(setup_cart_with_items):
    total_price = setup_cart_with_items.calculate_total_price()
    assert total_price == 200

# happy_path - test_list_items - Test that listing items displays the correct information for each item in the cart.
def test_list_items(setup_cart_with_items, mock_print):
    setup_cart_with_items.list_items()
    mock_print.assert_called_once_with('Item: Apple, Quantity: 2, Price per unit: 10.0')

# happy_path - test_empty_cart - Test that the cart is emptied successfully.
def test_empty_cart(setup_cart_with_items, mock_add_item_to_cart_db):
    setup_cart_with_items.empty_cart()
    assert setup_cart_with_items.items == []
    mock_add_item_to_cart_db.assert_called_once()

# happy_path - test_add_item_happy_path - Test that add_item adds an item to the cart with correct details.
def test_add_item_happy_path(cart, item, mock_add_item_to_cart_db):
    cart.add_item(item_id=item.item_id, quantity=2, price=10.0, name=item.name, category=item.category, user_type=cart.user_type)
    assert cart.items == [{'item_id': 1, 'quantity': 2, 'price': 10.0, 'name': 'Apple', 'category': 'Fruit', 'user_type': 'regular'}]
    mock_add_item_to_cart_db.assert_called_once()

# happy_path - test_remove_item_happy_path - Test that remove_item removes an existing item from the cart.
def test_remove_item_happy_path(setup_cart_with_items, mock_add_item_to_cart_db):
    setup_cart_with_items.remove_item(item_id=1)
    assert setup_cart_with_items.items == []
    mock_add_item_to_cart_db.assert_called_once()

# happy_path - test_update_item_quantity_happy_path - Test that update_item_quantity updates the quantity of an existing item correctly.
def test_update_item_quantity_happy_path(setup_cart_with_items, mock_add_item_to_cart_db):
    setup_cart_with_items.update_item_quantity(item_id=1, new_quantity=5)
    assert setup_cart_with_items.items == [{'item_id': 1, 'quantity': 5, 'price': 10.0, 'name': 'Apple', 'category': 'Fruit', 'user_type': 'regular'}]
    mock_add_item_to_cart_db.assert_called_once()

# happy_path - test_calculate_total_price_happy_path - Test that calculate_total_price returns the correct total price for items in the cart.
def test_calculate_total_price_happy_path(setup_cart_with_items):
    total_price = setup_cart_with_items.calculate_total_price()
    assert total_price == 20.0

# happy_path - test_list_items_happy_path - Test that list_items prints all items in the cart.
def test_list_items_happy_path(setup_cart_with_items, mock_print):
    setup_cart_with_items.list_items()
    mock_print.assert_called_once_with('Item: Apple, Quantity: 2, Price per unit: 10.0')

# happy_path - test_empty_cart_happy_path - Test that empty_cart clears all items from the cart.
def test_empty_cart_happy_path(setup_cart_with_items, mock_add_item_to_cart_db):
    setup_cart_with_items.empty_cart()
    assert setup_cart_with_items.items == []
    mock_add_item_to_cart_db.assert_called_once()

# happy_path - test_add_item_valid - Test that an item can be added to the cart with valid details.
def test_add_item_valid(cart, item, mock_add_item_to_cart_db):
    cart.add_item(item_id=item.item_id, quantity=2, price=item.price, name=item.name, category=item.category, user_type=cart.user_type)
    assert cart.items == [{'item_id': 1, 'quantity': 2, 'price': 10.0, 'name': 'Apple', 'category': 'Fruit', 'user_type': 'regular'}]
    mock_add_item_to_cart_db.assert_called_once()

# happy_path - test_remove_item_exists - Test that an item can be removed from the cart when it exists.
def test_remove_item_exists(setup_cart_with_items, mock_add_item_to_cart_db):
    setup_cart_with_items.remove_item(item_id=1)
    assert setup_cart_with_items.items == []
    mock_add_item_to_cart_db.assert_called_once()

# happy_path - test_update_item_quantity_exists - Test that the quantity of an existing item can be updated.
def test_update_item_quantity_exists(setup_cart_with_items, mock_add_item_to_cart_db):
    setup_cart_with_items.update_item_quantity(item_id=1, new_quantity=5)
    assert setup_cart_with_items.items == [{'item_id': 1, 'quantity': 5, 'price': 10.0, 'name': 'Apple', 'category': 'Fruit', 'user_type': 'regular'}]
    mock_add_item_to_cart_db.assert_called_once()

# happy_path - test_calculate_total_price_multiple - Test that the total price is calculated correctly for multiple items.
def test_calculate_total_price_multiple(cart):
    cart.items = [{'item_id': 1, 'quantity': 2, 'price': 10.0}, {'item_id': 2, 'quantity': 3, 'price': 10.0}]
    total_price = cart.calculate_total_price()
    assert total_price == 50.0

# happy_path - test_list_items - Test that all items in the cart are listed correctly.
def test_list_items(cart, mock_print):
    cart.items = [{'item_id': 1, 'quantity': 2, 'price': 10.0, 'name': 'Apple', 'category': 'Fruit'}]
    cart.list_items()
    mock_print.assert_called_once_with('Item: Apple, Quantity: 2, Price per unit: 10.0')

# happy_path - test_empty_cart - Test that the cart is emptied successfully.
def test_empty_cart(setup_cart_with_items, mock_add_item_to_cart_db):
    setup_cart_with_items.empty_cart()
    assert setup_cart_with_items.items == []
    mock_add_item_to_cart_db.assert_called_once()

# happy_path - test_add_item_valid - Test that adding a valid item to the cart updates the cart's item list and database.
def test_add_item_valid(cart, item, mock_add_item_to_cart_db):
    cart.add_item(item_id=item.item_id, quantity=2, price=item.price, name=item.name, category=item.category, user_type=cart.user_type)
    assert cart.items == [{'item_id': 1, 'quantity': 2, 'price': 10.0, 'name': 'Apple', 'category': 'Fruit', 'user_type': 'regular'}]
    mock_add_item_to_cart_db.assert_called_once()

# happy_path - test_remove_existing_item - Test that removing an existing item decreases the cart's item list size and updates the database.
def test_remove_existing_item(setup_cart_with_items, mock_add_item_to_cart_db):
    setup_cart_with_items.remove_item(item_id=1)
    assert setup_cart_with_items.items == []
    mock_add_item_to_cart_db.assert_called_once()

# happy_path - test_update_item_quantity - Test that updating the quantity of an existing item reflects the change in the cart and database.
def test_update_item_quantity(setup_cart_with_items, mock_add_item_to_cart_db):
    setup_cart_with_items.update_item_quantity(item_id=1, new_quantity=5)
    assert setup_cart_with_items.items == [{'item_id': 1, 'quantity': 5, 'price': 10.0, 'name': 'Apple', 'category': 'Fruit', 'user_type': 'regular'}]
    mock_add_item_to_cart_db.assert_called_once()

# happy_path - test_calculate_total_price - Test that calculating total price returns the correct sum based on items in the cart.
def test_calculate_total_price(setup_cart_with_items):
    total_price = setup_cart_with_items.calculate_total_price()
    assert total_price == 50.0

# happy_path - test_list_items - Test that listing items prints the correct details for each item in the cart.
def test_list_items(setup_cart_with_items, mock_print):
    setup_cart_with_items.list_items()
    mock_print.assert_called_once_with('Item: Apple, Quantity: 2, Price per unit: 10.0')

# happy_path - test_empty_cart - Test that emptying the cart clears all items and updates the database.
def test_empty_cart(setup_cart_with_items, mock_add_item_to_cart_db):
    setup_cart_with_items.empty_cart()
    assert setup_cart_with_items.items == []
    mock_add_item_to_cart_db.assert_called_once()

# edge_case - test_calculate_total_price_empty_cart - Test total price calculation when cart is empty returns zero.
def test_calculate_total_price_empty_cart(cart):
    total_price = cart.calculate_total_price()
    assert total_price == 0.0

# edge_case - test_list_items_empty_cart - Test listing items when cart is empty outputs no items.
def test_list_items_empty_cart(cart, mock_print):
    cart.list_items()
    mock_print.assert_not_called()

# edge_case - test_empty_already_empty_cart - Test emptying an already empty cart does not cause errors.
def test_empty_already_empty_cart(cart, mock_add_item_to_cart_db):
    cart.empty_cart()
    assert cart.items == []
    mock_add_item_to_cart_db.assert_called_once()

# edge_case - test_add_item_zero_quantity - Test that adding an item with zero quantity does not affect the cart.
def test_add_item_zero_quantity(cart, mock_add_item_to_cart_db):
    cart.add_item(item_id=2, quantity=0, price=15.0, name='Banana', category='Fruit', user_type='regular')
    assert cart.items == []
    mock_add_item_to_cart_db.assert_not_called()

# edge_case - test_remove_item_not_in_cart - Test that removing an item not in the cart does not cause errors.
def test_remove_item_not_in_cart(cart, mock_add_item_to_cart_db):
    cart.remove_item(item_id=999)
    assert cart.items == []
    mock_add_item_to_cart_db.assert_called_once()

# edge_case - test_update_item_quantity_not_in_cart - Test that updating the quantity of an item not in the cart does not cause errors.
def test_update_item_quantity_not_in_cart(cart, mock_add_item_to_cart_db):
    cart.update_item_quantity(item_id=999, new_quantity=3)
    assert cart.items == []
    mock_add_item_to_cart_db.assert_called_once()

# edge_case - test_calculate_total_price_empty_cart - Test that calculating total price in an empty cart returns zero.
def test_calculate_total_price_empty_cart(cart):
    total_price = cart.calculate_total_price()
    assert total_price == 0.0

# edge_case - test_list_items_empty_cart - Test that listing items in an empty cart returns no output.
def test_list_items_empty_cart(cart, mock_print):
    cart.list_items()
    mock_print.assert_not_called()

# edge_case - test_empty_cart_already_empty - Test that emptying an already empty cart does not cause errors.
def test_empty_cart_already_empty(cart, mock_add_item_to_cart_db):
    cart.empty_cart()
    assert cart.items == []
    mock_add_item_to_cart_db.assert_called_once()

# edge_case - test_add_item_negative_quantity - Test that adding an item with negative quantity raises an error or is handled gracefully.
def test_add_item_negative_quantity(cart, mock_add_item_to_cart_db):
    try:
        cart.add_item(item_id=2, quantity=-1, price=10.0, name='Orange', category='Fruit', user_type='guest')
    except ValueError as e:
        assert str(e) == 'Invalid quantity'
    else:
        assert False, 'Exception not raised'
    mock_add_item_to_cart_db.assert_not_called()

# edge_case - test_remove_item_non_existing - Test that removing a non-existing item does not crash the system.
def test_remove_item_non_existing(cart, mock_add_item_to_cart_db):
    cart.remove_item(item_id=999)
    assert cart.items == []
    mock_add_item_to_cart_db.assert_called_once()

# edge_case - test_update_item_quantity_non_existing - Test that updating the quantity of a non-existing item does not affect the items list.
def test_update_item_quantity_non_existing(cart, mock_add_item_to_cart_db):
    cart.update_item_quantity(item_id=999, new_quantity=5)
    assert cart.items == []
    mock_add_item_to_cart_db.assert_called_once()

# edge_case - test_calculate_total_price_empty_cart - Test that calculating total price for an empty cart returns zero.
def test_calculate_total_price_empty_cart(cart):
    total_price = cart.calculate_total_price()
    assert total_price == 0.0

# edge_case - test_list_items_empty_cart - Test that listing items in an empty cart shows no output or a specific message.
def test_list_items_empty_cart(cart, mock_print):
    cart.list_items()
    mock_print.assert_not_called()

# edge_case - test_empty_cart_already_empty - Test that emptying an already empty cart does not crash the system.
def test_empty_cart_already_empty(cart, mock_add_item_to_cart_db):
    cart.empty_cart()
    assert cart.items == []
    mock_add_item_to_cart_db.assert_called_once()

# edge_case - test_add_item_zero_quantity - Test adding an item with zero quantity should not add to the cart.
def test_add_item_zero_quantity(cart, mock_add_item_to_cart_db):
    cart.add_item(item_id=2, quantity=0, price=15.0, name='Banana', category='Fruit', user_type='regular')
    assert cart.items == []
    mock_add_item_to_cart_db.assert_not_called()

# edge_case - test_remove_item_non_existent - Test removing an item that does not exist in the cart should not alter the cart.
def test_remove_item_non_existent(setup_cart_with_items, mock_add_item_to_cart_db):
    setup_cart_with_items.remove_item(item_id=999)
    assert setup_cart_with_items.items == [{'item_id': 1, 'quantity': 2, 'price': 10.0, 'name': 'Apple', 'category': 'Fruit', 'user_type': 'regular'}]
    mock_add_item_to_cart_db.assert_called_once()

# edge_case - test_update_item_quantity_to_zero - Test updating item quantity to zero should remove the item from the cart.
def test_update_item_quantity_to_zero(setup_cart_with_items, mock_add_item_to_cart_db):
    setup_cart_with_items.update_item_quantity(item_id=1, new_quantity=0)
    assert setup_cart_with_items.items == []
    mock_add_item_to_cart_db.assert_called_once()

# edge_case - test_calculate_total_price_empty_cart - Test calculating total price for an empty cart should return zero.
def test_calculate_total_price_empty_cart(cart):
    total_price = cart.calculate_total_price()
    assert total_price == 0.0

# edge_case - test_list_items_empty_cart - Test listing items in an empty cart should produce no output.
def test_list_items_empty_cart(cart, mock_print):
    cart.list_items()
    mock_print.assert_not_called()

# edge_case - test_empty_cart_already_empty - Test emptying an already empty cart should not cause errors.
def test_empty_cart_already_empty(cart, mock_add_item_to_cart_db):
    cart.empty_cart()
    assert cart.items == []
    mock_add_item_to_cart_db.assert_called_once()

# edge_case - test_add_item_zero_quantity - Test adding an item with zero quantity
def test_add_item_zero_quantity(cart, mock_add_item_to_cart_db):
    cart.add_item(item_id=2, quantity=0, price=50.0, name='Pen', category='Stationery', user_type='Regular')
    assert cart.items == []
    mock_add_item_to_cart_db.assert_not_called()

# edge_case - test_remove_item_not_in_cart - Test removing an item not in the cart
def test_remove_item_not_in_cart(cart, mock_add_item_to_cart_db):
    cart.remove_item(item_id=3)
    assert cart.items == []
    mock_add_item_to_cart_db.assert_called_once()

# edge_case - test_update_item_quantity_not_in_cart - Test updating quantity of an item not in the cart
def test_update_item_quantity_not_in_cart(cart, mock_add_item_to_cart_db):
    cart.update_item_quantity(item_id=4, new_quantity=3)
    assert cart.items == []
    mock_add_item_to_cart_db.assert_called_once()

# edge_case - test_calculate_total_price_empty_cart - Test calculating total price with no items in cart
def test_calculate_total_price_empty_cart(cart):
    total_price = cart.calculate_total_price()
    assert total_price == 0

# edge_case - test_list_items_empty_cart - Test listing items when cart is empty
def test_list_items_empty_cart(cart, mock_print):
    cart.list_items()
    mock_print.assert_not_called()

# edge_case - test_empty_cart_already_empty - Test emptying an already empty cart
def test_empty_cart_already_empty(cart, mock_add_item_to_cart_db):
    cart.empty_cart()
    assert cart.items == []
    mock_add_item_to_cart_db.assert_called_once()

# edge_case - test_add_item_zero_quantity - Test that add_item handles adding an item with zero quantity gracefully.
def test_add_item_zero_quantity(cart, mock_add_item_to_cart_db):
    cart.add_item(item_id=2, quantity=0, price=50.0, name='Mouse', category='Electronics', user_type='regular')
    assert cart.items == []
    mock_add_item_to_cart_db.assert_not_called()

# edge_case - test_remove_item_nonexistent_id - Test that remove_item does nothing if the item_id does not exist in the cart.
def test_remove_item_nonexistent_id(setup_cart_with_items, mock_add_item_to_cart_db):
    setup_cart_with_items.remove_item(item_id=999)
    assert setup_cart_with_items.items == [{'item_id': 1, 'quantity': 2, 'price': 100.0, 'name': 'Laptop', 'category': 'Electronics', 'user_type': 'regular'}]
    mock_add_item_to_cart_db.assert_called_once()

# edge_case - test_update_item_quantity_to_zero - Test that update_item_quantity handles updating quantity to zero correctly.
def test_update_item_quantity_to_zero(setup_cart_with_items, mock_add_item_to_cart_db):
    setup_cart_with_items.update_item_quantity(item_id=1, new_quantity=0)
    assert setup_cart_with_items.items == []
    mock_add_item_to_cart_db.assert_called_once()

# edge_case - test_calculate_total_price_empty_cart - Test that calculate_total_price returns zero when the cart is empty.
def test_calculate_total_price_empty_cart(cart):
    total_price = cart.calculate_total_price()
    assert total_price == 0.0

# edge_case - test_list_items_empty_cart - Test that list_items handles an empty cart without errors.
def test_list_items_empty_cart(cart, mock_print):
    cart.list_items()
    mock_print.assert_not_called()

# edge_case - test_empty_cart_already_empty - Test that empty_cart on an already empty cart does not cause errors.
def test_empty_cart_already_empty(cart, mock_add_item_to_cart_db):
    cart.empty_cart()
    assert cart.items == []
    mock_add_item_to_cart_db.assert_called_once()

# edge_case - test_add_item_zero_quantity - Test that adding an item with zero quantity does not add the item to the cart.
def test_add_item_zero_quantity(cart, mock_add_item_to_cart_db):
    cart.add_item(item_id=2, quantity=0, price=50, name='Mouse', category='Electronics', user_type='regular')
    assert cart.items == []
    mock_add_item_to_cart_db.assert_not_called()

# edge_case - test_remove_non_existent_item - Test that trying to remove an item not in the cart does not affect the cart.
def test_remove_non_existent_item(setup_cart_with_items, mock_add_item_to_cart_db):
    setup_cart_with_items.remove_item(item_id=99)
    assert setup_cart_with_items.items == [{'item_id': 1, 'quantity': 2, 'price': 100, 'name': 'Laptop', 'category': 'Electronics', 'user_type': 'regular'}]
    mock_add_item_to_cart_db.assert_called_once()

# edge_case - test_update_quantity_to_zero - Test that updating the quantity of an item to zero removes it from the cart.
def test_update_quantity_to_zero(setup_cart_with_items, mock_add_item_to_cart_db):
    setup_cart_with_items.update_item_quantity(item_id=1, new_quantity=0)
    assert setup_cart_with_items.items == []
    mock_add_item_to_cart_db.assert_called_once()

# edge_case - test_calculate_total_price_empty_cart - Test that calculating total price on an empty cart returns zero.
def test_calculate_total_price_empty_cart(cart):
    total_price = cart.calculate_total_price()
    assert total_price == 0

# edge_case - test_list_items_empty_cart - Test that listing items in an empty cart shows no output.
def test_list_items_empty_cart(cart, mock_print):
    cart.list_items()
    mock_print.assert_not_called()

# edge_case - test_empty_already_empty_cart - Test that emptying an already empty cart does not cause errors.
def test_empty_already_empty_cart(cart, mock_add_item_to_cart_db):
    cart.empty_cart()
    assert cart.items == []
    mock_add_item_to_cart_db.assert_called_once()

# edge_case - test_add_item_edge_zero_quantity - Test that add_item handles adding an item with zero quantity.
def test_add_item_edge_zero_quantity(cart, mock_add_item_to_cart_db):
    cart.add_item(item_id=2, quantity=0, price=5.0, name='Banana', category='Fruit', user_type='guest')
    assert cart.items == []
    mock_add_item_to_cart_db.assert_not_called()

# edge_case - test_remove_item_edge_non_existing - Test that remove_item handles attempting to remove an item not in the cart.
def test_remove_item_edge_non_existing(setup_cart_with_items, mock_add_item_to_cart_db):
    setup_cart_with_items.remove_item(item_id=999)
    assert setup_cart_with_items.items == [{'item_id': 1, 'quantity': 2, 'price': 10.0, 'name': 'Apple', 'category': 'Fruit', 'user_type': 'regular'}]
    mock_add_item_to_cart_db.assert_called_once()

# edge_case - test_update_item_quantity_edge_non_existing - Test that update_item_quantity handles updating quantity for non-existing item.
def test_update_item_quantity_edge_non_existing(setup_cart_with_items, mock_add_item_to_cart_db):
    setup_cart_with_items.update_item_quantity(item_id=999, new_quantity=3)
    assert setup_cart_with_items.items == [{'item_id': 1, 'quantity': 2}]
    mock_add_item_to_cart_db.assert_called_once()

# edge_case - test_calculate_total_price_edge_empty_cart - Test that calculate_total_price handles an empty cart.
def test_calculate_total_price_edge_empty_cart(cart):
    total_price = cart.calculate_total_price()
    assert total_price == 0.0

# edge_case - test_list_items_edge_empty_cart - Test that list_items handles an empty cart without errors.
def test_list_items_edge_empty_cart(cart, mock_print):
    cart.list_items()
    mock_print.assert_not_called()

# edge_case - test_empty_cart_edge_already_empty - Test that empty_cart on an already empty cart does not cause errors.
def test_empty_cart_edge_already_empty(cart, mock_add_item_to_cart_db):
    cart.empty_cart()
    assert cart.items == []
    mock_add_item_to_cart_db.assert_called_once()

# edge_case - test_add_item_negative_quantity - Test adding an item with a negative quantity.
def test_add_item_negative_quantity(cart, mock_add_item_to_cart_db):
    try:
        cart.add_item(item_id=1, quantity=-1, price=10.0, name='Apple', category='Fruit', user_type='regular')
    except ValueError as e:
        assert str(e) == 'Invalid quantity'
    else:
        assert False, 'Exception not raised'
    mock_add_item_to_cart_db.assert_not_called()

# edge_case - test_remove_item_not_exists - Test removing an item that does not exist in the cart.
def test_remove_item_not_exists(cart, mock_add_item_to_cart_db):
    cart.remove_item(item_id=99)
    assert cart.items == []
    mock_add_item_to_cart_db.assert_called_once()

# edge_case - test_update_item_quantity_not_exists - Test updating the quantity of an item not in the cart.
def test_update_item_quantity_not_exists(cart, mock_add_item_to_cart_db):
    try:
        cart.update_item_quantity(item_id=99, new_quantity=5)
    except ValueError as e:
        assert str(e) == 'Item not found'
    else:
        assert False, 'Exception not raised'
    mock_add_item_to_cart_db.assert_not_called()

# edge_case - test_calculate_total_price_empty - Test calculating total price with no items in the cart.
def test_calculate_total_price_empty(cart):
    total_price = cart.calculate_total_price()
    assert total_price == 0.0

# edge_case - test_list_items_empty - Test listing items when the cart is empty.
def test_list_items_empty(cart, mock_print):
    cart.list_items()
    mock_print.assert_called_once_with('No items in the cart')

# edge_case - test_empty_cart_already_empty - Test emptying an already empty cart.
def test_empty_cart_already_empty(cart, mock_add_item_to_cart_db):
    cart.empty_cart()
    assert cart.items == []
    mock_add_item_to_cart_db.assert_called_once()

# edge_case - test_add_item_zero_quantity - Test that adding an item with zero quantity does not add it to the cart or database.
def test_add_item_zero_quantity(cart, mock_add_item_to_cart_db):
    cart.add_item(item_id=2, quantity=0, price=15.0, name='Banana', category='Fruit', user_type='regular')
    assert cart.items == []
    mock_add_item_to_cart_db.assert_not_called()

# edge_case - test_remove_nonexistent_item - Test that removing an item not present in the cart does not affect the cart or database.
def test_remove_nonexistent_item(cart, mock_add_item_to_cart_db):
    cart.remove_item(item_id=999)
    assert cart.items == []
    mock_add_item_to_cart_db.assert_called_once()

# edge_case - test_update_quantity_nonexistent_item - Test that updating the quantity of a nonexistent item does not affect the cart or database.
def test_update_quantity_nonexistent_item(cart, mock_add_item_to_cart_db):
    cart.update_item_quantity(item_id=999, new_quantity=3)
    assert cart.items == []
    mock_add_item_to_cart_db.assert_called_once()

# edge_case - test_calculate_total_price_empty_cart - Test that calculating total price for an empty cart returns zero.
def test_calculate_total_price_empty_cart(cart):
    total_price = cart.calculate_total_price()
    assert total_price == 0.0

# edge_case - test_list_items_empty_cart - Test that listing items for an empty cart outputs no item details.
def test_list_items_empty_cart(cart, mock_print):
    cart.list_items()
    mock_print.assert_not_called()

# edge_case - test_empty_already_empty_cart - Test that emptying an already empty cart does not cause errors or database changes.
def test_empty_already_empty_cart(cart, mock_add_item_to_cart_db):
    cart.empty_cart()
    assert cart.items == []
    mock_add_item_to_cart_db.assert_called_once()

# edge_case - test_add_item_zero_quantity - Test adding an item with zero quantity to the cart.
def test_add_item_zero_quantity(cart, mock_add_item_to_cart_db):
    cart.add_item(item_id=2, quantity=0, price=5.0, name='Banana', category='Fruit', user_type='regular')
    assert cart.items == []
    mock_add_item_to_cart_db.assert_not_called()

# edge_case - test_remove_item_nonexistent - Test removing an item that does not exist in the cart.
def test_remove_item_nonexistent(cart, mock_add_item_to_cart_db):
    cart.remove_item(item_id=99)
    assert cart.items == []
    mock_add_item_to_cart_db.assert_called_once()

# edge_case - test_update_item_quantity_nonexistent - Test updating the quantity of an item not present in the cart.
def test_update_item_quantity_nonexistent(cart, mock_add_item_to_cart_db):
    cart.update_item_quantity(item_id=99, new_quantity=3)
    assert cart.items == []
    mock_add_item_to_cart_db.assert_called_once()

# edge_case - test_calculate_total_price_empty_cart - Test calculating total price when the cart is empty.
def test_calculate_total_price_empty_cart(cart):
    total_price = cart.calculate_total_price()
    assert total_price == 0.0

# edge_case - test_list_items_empty_cart - Test listing items when the cart is empty.
def test_list_items_empty_cart(cart, mock_print):
    cart.list_items()
    mock_print.assert_not_called()

# edge_case - test_empty_cart_already_empty - Test emptying an already empty cart.
def test_empty_cart_already_empty(cart, mock_add_item_to_cart_db):
    cart.empty_cart()
    assert cart.items == []
    mock_add_item_to_cart_db.assert_called_once()

