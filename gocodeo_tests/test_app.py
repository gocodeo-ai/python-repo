import pytest
from unittest.mock import patch, MagicMock
from shopping_cart.cart import Cart
from shopping_cart.discounts import Discount
from shopping_cart.payments import apply_promotions, Promotion
from shopping_cart.utils import get_all_items_from_cart
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.fixture
def mock_cart():
    with patch('app.Cart') as MockCart:
        instance = MockCart.return_value
        instance.calculate_total_price.return_value = 39.98
        instance.add_item = MagicMock()
        instance.remove_item = MagicMock()
        instance.update_item_quantity = MagicMock()
        instance.total_price = 39.98  # Set a default total price
        yield instance

@pytest.fixture
def mock_discount():
    with patch('app.Discount') as MockDiscount:
        instance = MockDiscount.return_value
        instance.apply_discount = MagicMock()
        yield instance

@pytest.fixture
def mock_apply_promotions():
    with patch('app.apply_promotions') as mock_apply:
        yield mock_apply

@pytest.fixture
def mock_get_all_items_from_cart():
    with patch('app.get_all_items_from_cart') as mock_get_items:
        mock_get_items.return_value = [{'item_id': 1, 'quantity': 2, 'price': 19.99}]
        yield mock_get_items

@pytest.fixture(autouse=True)
def setup_mocks(mock_cart, mock_discount, mock_apply_promotions, mock_get_all_items_from_cart):
    # This fixture will automatically apply the mocks for each test
    pass

# happy_path - test_add_item_success - Test that item is added to the cart successfully with valid details.
def test_add_item_success(client, mock_cart):
    response = client.post('/add_item', json={
        'item_id': 1,
        'quantity': 2,
        'price': 19.99,
        'name': 'Widget',
        'category': 'Gadgets'
    })
    assert response.status_code == 201
    assert response.json == {'message': 'Item added to cart'}
    mock_cart.add_item.assert_called_once_with(1, 2, 19.99, 'Widget', 'Gadgets', 'regular')

# happy_path - test_remove_item_success - Test that item is removed from the cart successfully when it exists.
def test_remove_item_success(client, mock_cart):
    response = client.post('/remove_item', json={'item_id': 1})
    assert response.status_code == 200
    assert response.json == {'message': 'Item removed from cart'}
    mock_cart.remove_item.assert_called_once_with(1)

# happy_path - test_update_item_quantity_success - Test that item quantity is updated successfully in the cart.
def test_update_item_quantity_success(client, mock_cart):
    response = client.post('/update_item_quantity', json={'item_id': 1, 'new_quantity': 5})
    assert response.status_code == 200
    assert response.json == {'message': 'Item quantity updated'}
    mock_cart.update_item_quantity.assert_called_once_with(1, 5)

# happy_path - test_get_cart_items_success - Test that all items are retrieved from the cart successfully.
def test_get_cart_items_success(client, mock_get_all_items_from_cart):
    response = client.get('/get_cart_items')
    assert response.status_code == 200
    assert response.json == {'items': [{'item_id': 1, 'quantity': 2, 'price': 19.99}]}

# edge_case - test_add_item_invalid_id - Test that adding an item with invalid item_id returns an error.
def test_add_item_invalid_id(client):
    response = client.post('/add_item', json={
        'item_id': 'abc',
        'quantity': 2,
        'price': 19.99,
        'name': 'Widget',
        'category': 'Gadgets'
    })
    assert response.status_code == 400
    assert response.json == {'message': 'Invalid item_id'}

# edge_case - test_remove_non_existent_item - Test that removing a non-existent item returns an error.
def test_remove_non_existent_item(client, mock_cart):
    mock_cart.remove_item.side_effect = Exception('Item not found')
    response = client.post('/remove_item', json={'item_id': 999})
    assert response.status_code == 404
    assert response.json == {'message': 'Item not found'}

