import pytest
from unittest.mock import patch, MagicMock
from flask import jsonify
from shopping_cart.cart import Cart
from shopping_cart.discounts import Discount
from shopping_cart.payments import apply_promotions, Promotion
from shopping_cart.utils import get_all_items_from_cart
from app import app  # Import the Flask app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

@pytest.fixture
def mock_cart():
    with patch('app.Cart') as MockCart:
        instance = MockCart.return_value
        instance.add_item = MagicMock()
        instance.remove_item = MagicMock()
        instance.update_item_quantity = MagicMock()
        instance.calculate_total_price = MagicMock(return_value=20.0)
        instance.total_price = 18.0  # Set total_price for discount test
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
        mock_get_items.return_value = [{'item_id': 1, 'name': 'Test Item', 'quantity': 2}]
        yield mock_get_items

@pytest.fixture
def mock_promotion():
    with patch('app.Promotion') as MockPromotion:
        instance = MockPromotion.return_value
        yield instance

@pytest.fixture(autouse=True)
def setup_mocks(mock_cart, mock_discount, mock_apply_promotions, mock_get_all_items_from_cart, mock_promotion):
    # This fixture will automatically apply all mocks for each test
    pass

# happy_path - add_item - Test that an item is added to the cart successfully
def test_add_item_success(client, mock_cart):
    response = client.post('/add_item', json={
        'item_id': 1,
        'quantity': 2,
        'price': 10.0,
        'name': 'Test Item',
        'category': 'Test Category'
    })
    assert response.status_code == 201
    assert response.get_json() == {'message': 'Item added to cart'}
    mock_cart.add_item.assert_called_once_with(1, 2, 10.0, 'Test Item', 'Test Category', 'regular')

# happy_path - remove_item - Test that an item is removed from the cart successfully
def test_remove_item_success(client, mock_cart):
    response = client.post('/remove_item', json={'item_id': 1})
    assert response.status_code == 200
    assert response.get_json() == {'message': 'Item removed from cart'}
    mock_cart.remove_item.assert_called_once_with(1)

# happy_path - update_item_quantity - Test that item quantity is updated successfully
def test_update_item_quantity_success(client, mock_cart):
    response = client.post('/update_item_quantity', json={'item_id': 1, 'new_quantity': 5})
    assert response.status_code == 200
    assert response.get_json() == {'message': 'Item quantity updated'}
    mock_cart.update_item_quantity.assert_called_once_with(1, 5)

# happy_path - get_cart_items - Test that cart items are retrieved successfully
def test_get_cart_items_success(client, mock_get_all_items_from_cart):
    response = client.get('/get_cart_items')
    assert response.status_code == 200
    assert response.get_json() == {'items': [{'item_id': 1, 'name': 'Test Item', 'quantity': 2}]}
    mock_get_all_items_from_cart.assert_called_once()

# happy_path - calculate_total_price - Test that total price is calculated successfully
def test_calculate_total_price_success(client, mock_cart):
    response = client.get('/calculate_total_price')
    assert response.status_code == 200
    assert response.get_json() == {'total_price': 20.0}
    mock_cart.calculate_total_price.assert_called_once()

# happy_path - apply_discount_to_cart - Test that discount is applied to the cart successfully
def test_apply_discount_success(client, mock_cart, mock_discount):
    response = client.post('/apply_discount', json={'discount_rate': 0.1, 'min_purchase_amount': 0})
    assert response.status_code == 200
    assert response.get_json() == {'discounted_total': 18.0}
    mock_discount.apply_discount.assert_called_once_with(mock_cart)

# happy_path - apply_promotions_to_cart - Test that promotions are applied to the cart successfully
def test_apply_promotions_success(client, mock_cart, mock_apply_promotions, mock_promotion):
    response = client.post('/apply_promotions')
    assert response.status_code == 200
    assert response.get_json() == {'message': 'Promotions applied'}
    mock_apply_promotions.assert_called_once_with(mock_cart, [mock_promotion.return_value, mock_promotion.return_value])

# edge_case - add_item - Test that adding an item with invalid data returns an error
def test_add_item_invalid_data(client):
    response = client.post('/add_item', json={
        'item_id': 'invalid',
        'quantity': 2,
        'price': 10.0,
        'name': 'Test Item',
        'category': 'Test Category'
    })
    assert response.status_code == 400
    assert response.get_json() == {'error': 'Invalid item_id'}

# edge_case - remove_item - Test that removing an item not in the cart returns an error
def test_remove_item_not_in_cart(client, mock_cart):
    mock_cart.remove_item.side_effect = Exception('Item not found')
    response = client.post('/remove_item', json={'item_id': 999})
    assert response.status_code == 404
    assert response.get_json() == {'error': 'Item not found'}

# edge_case - update_item_quantity - Test that updating quantity of non-existent item returns an error
def test_update_item_quantity_non_existent(client, mock_cart):
    mock_cart.update_item_quantity.side_effect = Exception('Item not found')
    response = client.post('/update_item_quantity', json={'item_id': 999, 'new_quantity': 5})
    assert response.status_code == 404
    assert response.get_json() == {'error': 'Item not found'}

# edge_case - apply_discount_to_cart - Test that applying discount with invalid rate returns an error
def test_apply_discount_invalid_rate(client):
    response = client.post('/apply_discount', json={'discount_rate': 'invalid', 'min_purchase_amount': 0})
    assert response.status_code == 400
    assert response.get_json() == {'error': 'Invalid discount rate'}

# edge_case - apply_promotions_to_cart - Test that applying promotions with no promotions available returns no change
def test_apply_promotions_no_promotions(client, mock_apply_promotions):
    mock_apply_promotions.return_value = None
    response = client.post('/apply_promotions')
    assert response.status_code == 200
    assert response.get_json() == {'message': 'No promotions applied'}

