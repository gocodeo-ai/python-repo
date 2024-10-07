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
    with patch('shopping_cart.cart.Cart', autospec=True) as mock_cart_class:
        yield mock_cart_class.return_value

@pytest.fixture
def mock_discount():
    with patch('shopping_cart.discounts.Discount', autospec=True) as mock_discount_class:
        yield mock_discount_class.return_value

@pytest.fixture
def mock_apply_promotions():
    with patch('shopping_cart.payments.apply_promotions', autospec=True) as mock_apply_promotions_func:
        yield mock_apply_promotions_func

@pytest.fixture
def mock_promotion():
    with patch('shopping_cart.payments.Promotion', autospec=True) as mock_promotion_class:
        yield mock_promotion_class.return_value

@pytest.fixture
def mock_get_all_items_from_cart():
    with patch('shopping_cart.utils.get_all_items_from_cart', autospec=True) as mock_get_all_items:
        yield mock_get_all_items

@pytest.fixture
def client(app):
    return app.test_client()

# happy_path - add_item - Test that an item is added to the cart successfully with valid inputs.
def test_add_item_success(client, mock_cart):
    response = client.post('/add_item', json={
        'item_id': 1,
        'quantity': 2,
        'price': 10.0,
        'name': 'Test Item',
        'category': 'Test Category'
    })
    assert response.status_code == 201
    assert response.json == {'message': 'Item added to cart'}
    mock_cart.add_item.assert_called_once_with(1, 2, 10.0, 'Test Item', 'Test Category', 'regular')

# happy_path - remove_item - Test that an item is removed from the cart successfully with valid item_id.
def test_remove_item_success(client, mock_cart):
    response = client.post('/remove_item', json={'item_id': 1})
    assert response.status_code == 200
    assert response.json == {'message': 'Item removed from cart'}
    mock_cart.remove_item.assert_called_once_with(1)

# happy_path - update_item_quantity - Test that the item quantity is updated successfully with valid item_id and new_quantity.
def test_update_item_quantity_success(client, mock_cart):
    response = client.post('/update_item_quantity', json={
        'item_id': 1,
        'new_quantity': 5
    })
    assert response.status_code == 200
    assert response.json == {'message': 'Item quantity updated'}
    mock_cart.update_item_quantity.assert_called_once_with(1, 5)

# happy_path - get_cart_items - Test that all items in the cart are retrieved successfully.
def test_get_cart_items_success(client, mock_get_all_items_from_cart):
    mock_get_all_items_from_cart.return_value = [{
        'item_id': 1,
        'quantity': 5,
        'price': 10.0,
        'name': 'Test Item',
        'category': 'Test Category'
    }]
    response = client.get('/get_cart_items')
    assert response.status_code == 200
    assert response.json == {'items': mock_get_all_items_from_cart.return_value}

# happy_path - calculate_total_price - Test that the total price of the cart is calculated correctly.
def test_calculate_total_price_success(client, mock_cart):
    mock_cart.calculate_total_price.return_value = 50.0
    response = client.get('/calculate_total_price')
    assert response.status_code == 200
    assert response.json == {'total_price': 50.0}
    mock_cart.calculate_total_price.assert_called_once()

# happy_path - apply_discount_to_cart - Test that a discount is applied to the cart successfully with valid discount rate.
def test_apply_discount_success(client, mock_cart, mock_discount):
    response = client.post('/apply_discount', json={
        'discount_rate': 0.1,
        'min_purchase_amount': 0
    })
    assert response.status_code == 200
    assert response.json == {'discounted_total': mock_cart.total_price}
    mock_discount.apply_discount.assert_called_once_with(mock_cart)

# happy_path - apply_promotions_to_cart - Test that promotions are applied to the cart successfully.
def test_apply_promotions_success(client, mock_cart, mock_apply_promotions, mock_promotion):
    response = client.post('/apply_promotions')
    assert response.status_code == 200
    assert response.json == {'message': 'Promotions applied'}
    mock_apply_promotions.assert_called_once_with(mock_cart, [mock_promotion, mock_promotion])

# edge_case - add_item - Test that adding an item with zero quantity returns an error.
def test_add_item_zero_quantity(client, mock_cart):
    response = client.post('/add_item', json={
        'item_id': 2,
        'quantity': 0,
        'price': 20.0,
        'name': 'Test Item 2',
        'category': 'Test Category'
    })
    assert response.status_code == 400
    assert response.json == {'error': 'Quantity must be greater than zero'}

# edge_case - remove_item - Test that removing an item not in the cart returns an error.
def test_remove_item_not_in_cart(client, mock_cart):
    mock_cart.remove_item.side_effect = ValueError('Item not found in cart')
    response = client.post('/remove_item', json={'item_id': 99})
    assert response.status_code == 404
    assert response.json == {'error': 'Item not found in cart'}

# edge_case - update_item_quantity - Test that updating quantity to a negative number returns an error.
def test_update_item_quantity_negative(client, mock_cart):
    response = client.post('/update_item_quantity', json={
        'item_id': 1,
        'new_quantity': -5
    })
    assert response.status_code == 400
    assert response.json == {'error': 'Quantity must be a positive integer'}

# edge_case - calculate_total_price - Test that calculating total price with no items in the cart returns zero.
def test_calculate_total_price_empty_cart(client, mock_cart):
    mock_cart.calculate_total_price.return_value = 0.0
    response = client.get('/calculate_total_price')
    assert response.status_code == 200
    assert response.json == {'total_price': 0.0}
    mock_cart.calculate_total_price.assert_called_once()

# edge_case - apply_discount_to_cart - Test that applying a discount with a negative rate returns an error.
def test_apply_discount_negative_rate(client, mock_cart, mock_discount):
    response = client.post('/apply_discount', json={
        'discount_rate': -0.1,
        'min_purchase_amount': 0
    })
    assert response.status_code == 400
    assert response.json == {'error': 'Discount rate must be positive'}

# edge_case - apply_promotions_to_cart - Test that applying promotions with an empty promotion list returns no changes.
def test_apply_promotions_empty_list(client, mock_cart, mock_apply_promotions):
    mock_apply_promotions.return_value = None
    response = client.post('/apply_promotions')
    assert response.status_code == 200
    assert response.json == {'message': 'No promotions available'}
    mock_apply_promotions.assert_called_once_with(mock_cart, [])

