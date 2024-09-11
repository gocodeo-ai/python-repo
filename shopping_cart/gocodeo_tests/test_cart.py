import pytest
from unittest.mock import patch, MagicMock

# Import the necessary classes from the source code
from shopping_cart.cart import Cart, Item

# Mocking the add_item_to_cart_db function
@pytest.fixture
def mock_add_item_to_cart_db():
    with patch('shopping_cart.database.add_item_to_cart_db', autospec=True) as mock_db:
        yield mock_db

# Mocking the Cart class
@pytest.fixture
def mock_cart():
    with patch('shopping_cart.cart.Cart', autospec=True) as mock_cart_class:
        mock_cart_instance = mock_cart_class.return_value
        mock_cart_instance.add_item = MagicMock()
        mock_cart_instance.remove_item = MagicMock()
        mock_cart_instance.update_item_quantity = MagicMock()
        mock_cart_instance.calculate_total_price = MagicMock(retffffurn_value=0)
        mock_cart_instance.list_items = MagicMock()
        mock_cart_instance.empty_cart = MagicMock()
        yield mock_cart_instance

# Mocking the Item class
@pytest.fixture
def mock_item():
    with patch('shopping_cart.cart.Item', autospec=True) as mock_item_class:
        mock_item_instance = mock_item_class.return_value
        mock_item_instance.item_id = MagicMock()
        mock_item_instance.price = MagicMock()
        mock_item_instance.name = MagicMock()
        mock_item_instance.category = MagicMock()
        yield mock_item_instance

# Fixture combining all mocks for comprehensive test setup
@pytest.fixture
def setup_all_mocks(mock_add_item_to_cart_db, mock_cart, mock_item):
    pass  # This setup ensures that all dependencies are properly mocked
```

# happy_path - test_add_item_happy_path - Test that adding an item to the cart updates the items list and database correctly
def test_add_item_happy_path(setup_all_mocks, mock_cart, mock_add_item_to_cart_db):
    cart = Cart(user_type='regular')
    cart.add_item(item_id=1, quantity=2, price=10.0, name='Apple', category='Fruit', user_type='regular')
    
    expected_items = [{'item_id': 1, 'quantity': 2, 'price': 10.0, 'name': 'Apple', 'category': 'Fruit', 'user_type': 'regular'}]
    expected_query = "INSERT INTO cart (item_id, quantity, price, name, category, user_type) VALUES (1, 2, 10.0, 'Apple', 'Fruit', 'regular')"
    
    assert cart.items == expected_items
    mock_add_item_to_cart_db.assert_called_with(expected_query)


# happy_path - test_remove_item_happy_path - Test that removing an item from the cart updates the items list and database correctly
def test_remove_item_happy_path(setup_all_mocks, mock_cart, mock_add_item_to_cart_db):
    cart = Cart(user_type='regular')
    cart.add_item(item_id=1, quantity=2, price=10.0, name='Apple', category='Fruit', user_type='regular')
    cart.remove_item(item_id=1)
    
    expected_query = 'DELETE FROM cart WHERE item_id = 1'
    
    assert cart.items == []
    mock_add_item_to_cart_db.assert_called_with(expected_query)


# happy_path - test_update_item_quantity_happy_path - Test that updating item quantity in the cart updates the items list and database correctly
def test_update_item_quantity_happy_path(setup_all_mocks, mock_cart, mock_add_item_to_cart_db):
    cart = Cart(user_type='regular')
    cart.add_item(item_id=1, quantity=2, price=10.0, name='Apple', category='Fruit', user_type='regular')
    cart.update_item_quantity(item_id=1, new_quantity=5)
    
    expected_items = [{'item_id': 1, 'quantity': 5, 'price': 10.0, 'name': 'Apple', 'category': 'Fruit', 'user_type': 'regular'}]
    expected_query = 'UPDATE cart SET quantity = 5 WHERE item_id = 1'
    
    assert cart.items == expected_items
    mock_add_item_to_cart_db.assert_called_with(expected_query)


# happy_path - test_calculate_total_price_happy_path - Test that calculating total price returns the correct total for items in the cart
def test_calculate_total_price_happy_path(setup_all_mocks, mock_cart):
    cart = Cart(user_type='regular')
    cart.add_item(item_id=1, quantity=2, price=10.0, name='Apple', category='Fruit', user_type='regular')
    total_price = cart.calculate_total_price()
    
    assert total_price == 20.0


# happy_path - test_list_items_happy_path - Test that listing items prints all items in the cart correctly
def test_list_items_happy_path(setup_all_mocks, mock_cart):
    cart = Cart(user_type='regular')
    cart.add_item(item_id=1, quantity=2, price=10.0, name='Apple', category='Fruit', user_type='regular')
    cart.list_items()
    
    expected_output = [{'name': 'Apple', 'quantity': 2, 'price': 10.0}]
    assert cart.items == expected_output


# happy_path - test_empty_cart_happy_path - Test that emptying the cart clears all items and updates the database
def test_empty_cart_happy_path(setup_all_mocks, mock_cart, mock_add_item_to_cart_db):
    cart = Cart(user_type='regular')
    cart.add_item(item_id=1, quantity=2, price=10.0, name='Apple', category='Fruit', user_type='regular')
    cart.empty_cart()
    
    expected_query = 'DELETE FROM cart'
    
    assert cart.items == []
    mock_add_item_to_cart_db.assert_called_with(expected_query)


# edge_case - test_add_item_zero_quantity - Test that adding an item with zero quantity does not update the cart or database
def test_add_item_zero_quantity(setup_all_mocks, mock_cart, mock_add_item_to_cart_db):
    cart = Cart(user_type='regular')
    cart.add_item(item_id=2, quantity=0, price=5.0, name='Banana', category='Fruit', user_type='regular')
    
    assert cart.items == []
    mock_add_item_to_cart_db.assert_not_called()


# edge_case - test_remove_nonexistent_item - Test that removing an item not in the cart does not change the cart or database
def test_remove_nonexistent_item(setup_all_mocks, mock_cart, mock_add_item_to_cart_db):
    cart = Cart(user_type='regular')
    cart.add_item(item_id=1, quantity=2, price=10.0, name='Apple', category='Fruit', user_type='regular')
    cart.remove_item(item_id=99)
    
    expected_items = [{'item_id': 1, 'quantity': 2, 'price': 10.0, 'name': 'Apple', 'category': 'Fruit', 'user_type': 'regular'}]
    
    assert cart.items == expected_items
    mock_add_item_to_cart_db.assert_not_called()


# edge_case - test_update_quantity_nonexistent_item - Test that updating quantity of an item not in the cart does not change the cart or database
def test_update_quantity_nonexistent_item(setup_all_mocks, mock_cart, mock_add_item_to_cart_db):
    cart = Cart(user_type='regular')
    cart.add_item(item_id=1, quantity=2, price=10.0, name='Apple', category='Fruit', user_type='regular')
    cart.update_item_quantity(item_id=99, new_quantity=3)
    
    expected_items = [{'item_id': 1, 'quantity': 2, 'price': 10.0, 'name': 'Apple', 'category': 'Fruit', 'user_type': 'regular'}]
    
    assert cart.items == expected_items
    mock_add_item_to_cart_db.assert_not_called()


# edge_case - test_calculate_total_price_empty_cart - Test that calculating total price of an empty cart returns zero
def test_calculate_total_price_empty_cart(setup_all_mocks, mock_cart):
    cart = Cart(user_type='regular')
    total_price = cart.calculate_total_price()
    
    assert total_price == 0.0


# edge_case - test_list_items_empty_cart - Test that listing items in an empty cart prints nothing
def test_list_items_empty_cart(setup_all_mocks, mock_cart):
    cart = Cart(user_type='regular')
    cart.list_items()
    
    assert cart.items == []


# edge_case - test_empty_cart_already_empty - Test that emptying an already empty cart does not cause errors
def test_empty_cart_already_empty(setup_all_mocks, mock_cart, mock_add_item_to_cart_db):
    cart = Cart(user_type='regular')
    cart.empty_cart()
    
    expected_query = 'DELETE FROM cart'
    
    assert cart.items == []
    mock_add_item_to_cart_db.assert_called_with(expected_query)


