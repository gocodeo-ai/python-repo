import pytest
from unittest.mock import patch, MagicMock
from flask import Flask
from shopping_cart.cart import Cart
from shopping_cart.discounts import Discount
from shopping_cart.payments import apply_promotions, Promotion
from shopping_cart.utils import get_all_items_from_cart

@pytest.fixture
def app():
    app = Flask(__name__)
    app.config['TESTING'] = True

    with app.app_context():
        yield app

@pytest.fixture
def mock_cart():
    with patch('shopping_cart.cart.Cart') as MockCart:
        mock_cart_instance = MockCart.return_value
        mock_cart_instance.calculate_total_price.return_value = 52.5
        yield mock_cart_instance

@pytest.fixture
def mock_discount():
    with patch('shopping_cart.discounts.Discount') as MockDiscount:
        mock_discount_instance = MockDiscount.return_value
        mock_discount_instance.apply_discount.return_value = None
        yield mock_discount_instance

@pytest.fixture
def mock_apply_promotions():
    with patch('shopping_cart.payments.apply_promotions') as mock_apply:
        yield mock_apply

@pytest.fixture
def mock_get_all_items_from_cart():
    with patch('shopping_cart.utils.get_all_items_from_cart') as mock_get_items:
        mock_get_items.return_value = [{'item_id': 1, 'quantity': 5, 'price': 10.5, 'name': 'Test Item', 'category': 'General'}]
        yield mock_get_items

@pytest.fixture
def mock_promotion():
    with patch('shopping_cart.payments.Promotion') as MockPromotion:
        yield MockPromotion

@pytest.fixture
def client(app):
    return app.test_client()

# happy_path - test_add_item_success - Test that item is added to the cart successfully
def test_add_item_success(client, mock_cart):
    response = client.post('/add_item', json={
        'item_id': 1,
        'quantity': 2,
        'price': 10.5,
        'name': 'Test Item',
        'category': 'General'
    })
    assert response.status_code == 201
    assert response.json['message'] == 'Item added to cart'
    mock_cart.add_item.assert_called_once_with(1, 2, 10.5, 'Test Item', 'General', 'regular')

# happy_path - test_remove_item_success - Test that item is removed from the cart successfully
def test_remove_item_success(client, mock_cart):
    response = client.post('/remove_item', json={'item_id': 1})
    assert response.status_code == 200
    assert response.json['message'] == 'Item removed from cart'
    mock_cart.remove_item.assert_called_once_with(1)

# happy_path - test_update_item_quantity_success - Test that item quantity is updated successfully
def test_update_item_quantity_success(client, mock_cart):
    response = client.post('/update_item_quantity', json={'item_id': 1, 'new_quantity': 5})
    assert response.status_code == 200
    assert response.json['message'] == 'Item quantity updated'
    mock_cart.update_item_quantity.assert_called_once_with(1, 5)

# happy_path - test_get_cart_items_success - Test that cart items are retrieved successfully
def test_get_cart_items_success(client, mock_get_all_items_from_cart):
    response = client.get('/get_cart_items')
    assert response.status_code == 200
    assert response.json['items'] == [{'item_id': 1, 'quantity': 5, 'price': 10.5, 'name': 'Test Item', 'category': 'General'}]
    mock_get_all_items_from_cart.assert_called_once()

# happy_path - test_calculate_total_price_success - Test that total price is calculated successfully
def test_calculate_total_price_success(client, mock_cart):
    response = client.get('/calculate_total_price')
    assert response.status_code == 200
    assert response.json['total_price'] == 52.5
    mock_cart.calculate_total_price.assert_called_once()

# happy_path - test_apply_discount_to_cart_success - Test that discount is applied to the cart successfully
def test_apply_discount_to_cart_success(client, mock_cart, mock_discount):
    response = client.post('/apply_discount', json={'discount_rate': 0.1, 'min_purchase_amount': 0})
    assert response.status_code == 200
    assert response.json['discounted_total'] == 47.25
    mock_discount.assert_called_once_with(0.1, 0)
    mock_discount.return_value.apply_discount.assert_called_once_with(mock_cart)

# happy_path - test_apply_promotions_to_cart_success - Test that promotions are applied to the cart successfully
def test_apply_promotions_to_cart_success(client, mock_cart, mock_apply_promotions, mock_promotion):
    response = client.post('/apply_promotions')
    assert response.status_code == 200
    assert response.json['message'] == 'Promotions applied'
    mock_apply_promotions.assert_called_once_with(mock_cart, mock_promotion.return_value)
    mock_promotion.assert_called()

# edge_case - test_add_item_invalid_data - Test that adding item with invalid data returns an error
def test_add_item_invalid_data(client):
    response = client.post('/add_item', json={
        'item_id': 'invalid',
        'quantity': 'invalid',
        'price': 'invalid',
        'name': 123,
        'category': 456
    })
    assert response.status_code == 400
    assert response.json['message'] == 'Invalid input data'

# edge_case - test_remove_item_not_in_cart - Test that removing an item not in the cart returns an error
def test_remove_item_not_in_cart(client, mock_cart):
    mock_cart.remove_item.side_effect = KeyError('Item not found')
    response = client.post('/remove_item', json={'item_id': 999})
    assert response.status_code == 404
    assert response.json['message'] == 'Item not found'
    mock_cart.remove_item.assert_called_once_with(999)

# edge_case - test_update_item_quantity_not_in_cart - Test that updating quantity for an item not in the cart returns an error
def test_update_item_quantity_not_in_cart(client, mock_cart):
    mock_cart.update_item_quantity.side_effect = KeyError('Item not found')
    response = client.post('/update_item_quantity', json={'item_id': 999, 'new_quantity': 5})
    assert response.status_code == 404
    assert response.json['message'] == 'Item not found'
    mock_cart.update_item_quantity.assert_called_once_with(999, 5)

# edge_case - test_apply_discount_invalid_rate - Test that applying discount with invalid rate returns an error
def test_apply_discount_invalid_rate(client):
    response = client.post('/apply_discount', json={'discount_rate': 'invalid', 'min_purchase_amount': 0})
    assert response.status_code == 400
    assert response.json['message'] == 'Invalid discount rate'

# edge_case - test_apply_no_promotions_available - Test that applying promotions with no promotions available returns a message
def test_apply_no_promotions_available(client, mock_apply_promotions):
    mock_apply_promotions.side_effect = ValueError('No promotions available')
    response = client.post('/apply_promotions')
    assert response.status_code == 200
    assert response.json['message'] == 'No promotions available'
    mock_apply_promotions.assert_called_once()

