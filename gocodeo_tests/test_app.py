import pytest
from unittest.mock import patch, MagicMock
from shopping_cart.cart import Cart
from shopping_cart.discounts import Discount
from shopping_cart.payments import apply_promotions, Promotion
from shopping_cart.utils import get_all_items_from_cart
from app import app

@pytest.fixture
def mock_cart():
    with patch('shopping_cart.cart.Cart') as MockCart:
        instance = MockCart.return_value
        instance.add_item = MagicMock()
        instance.remove_item = MagicMock()
        instance.update_item_quantity = MagicMock()
        instance.calculate_total_price = MagicMock(return_value=50.0)
        yield instance

@pytest.fixture
def mock_discount():
    with patch('shopping_cart.discounts.Discount') as MockDiscount:
        instance = MockDiscount.return_value
        instance.apply_discount = MagicMock()
        yield instance

@pytest.fixture
def mock_apply_promotions():
    with patch('shopping_cart.payments.apply_promotions') as mock_apply:
        yield mock_apply

@pytest.fixture
def mock_promotion():
    with patch('shopping_cart.payments.Promotion') as MockPromotion:
        instance = MockPromotion.return_value
        yield instance

@pytest.fixture
def mock_get_all_items_from_cart():
    with patch('shopping_cart.utils.get_all_items_from_cart') as mock_get_items:
        mock_get_items.return_value = [{'item_id': 1, 'quantity': 5, 'price': 10.0, 'name': 'Test Item', 'category': 'Electronics'}]
        yield mock_get_items

@pytest.fixture
def client(mock_cart, mock_discount, mock_apply_promotions, mock_promotion, mock_get_all_items_from_cart):
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

# happy path - add_item - Test that item is added to cart successfully
def test_add_item_success(client):
    response = client.post('/add_item', json={
        'item_id': 1,
        'quantity': 2,
        'price': 10.0,
        'name': 'Test Item',
        'category': 'Electronics'
    })
    assert response.status_code == 201
    assert response.json['message'] == 'Item added to cart'


# happy path - remove_item - Test that item is removed from cart successfully
def test_remove_item_success(client):
    response = client.post('/remove_item', json={
        'item_id': 1
    })
    assert response.status_code == 200
    assert response.json['message'] == 'Item removed from cart'


# happy path - update_item_quantity - Test that item quantity is updated successfully
def test_update_item_quantity_success(client):
    response = client.post('/update_item_quantity', json={
        'item_id': 1,
        'new_quantity': 5
    })
    assert response.status_code == 200
    assert response.json['message'] == 'Item quantity updated'


# happy path - get_cart_items - Test that all items are retrieved from cart successfully
def test_get_cart_items_success(client):
    response = client.get('/get_cart_items')
    assert response.status_code == 200
    assert response.json['items'] == [{'item_id': 1, 'quantity': 5, 'price': 10.0, 'name': 'Test Item', 'category': 'Electronics'}]


# happy path - calculate_total_price - Test that total price is calculated successfully
def test_calculate_total_price_success(client):
    response = client.get('/calculate_total_price')
    assert response.status_code == 200
    assert response.json['total_price'] == 50.0


# happy path - apply_discount_to_cart - Test that discount is applied to cart successfully
def test_apply_discount_success(client):
    response = client.post('/apply_discount', json={
        'discount_rate': 0.1,
        'min_purchase_amount': 0
    })
    assert response.status_code == 200
    assert response.json['discounted_total'] == 45.0


# happy path - apply_promotions_to_cart - Test that promotions are applied to cart successfully
def test_apply_promotions_success(client):
    response = client.post('/apply_promotions')
    assert response.status_code == 200
    assert response.json['message'] == 'Promotions applied'


# edge case - add_item - Test adding item with zero quantity
def test_add_item_zero_quantity(client):
    response = client.post('/add_item', json={
        'item_id': 2,
        'quantity': 0,
        'price': 10.0,
        'name': 'Test Item Zero',
        'category': 'Books'
    })
    assert response.status_code == 400
    assert response.json['message'] == 'Invalid quantity'


# edge case - remove_item - Test removing item not in cart
def test_remove_item_not_in_cart(client):
    response = client.post('/remove_item', json={
        'item_id': 99
    })
    assert response.status_code == 404
    assert response.json['message'] == 'Item not found in cart'


# edge case - update_item_quantity - Test updating item quantity to negative
def test_update_item_quantity_negative(client):
    response = client.post('/update_item_quantity', json={
        'item_id': 1,
        'new_quantity': -1
    })
    assert response.status_code == 400
    assert response.json['message'] == 'Invalid quantity'


# edge case - get_cart_items - Test retrieving items from empty cart
def test_get_cart_items_empty(client, mock_get_all_items_from_cart):
    mock_get_all_items_from_cart.return_value = []
    response = client.get('/get_cart_items')
    assert response.status_code == 200
    assert response.json['items'] == []


# edge case - calculate_total_price - Test calculating total price of empty cart
def test_calculate_total_price_empty_cart(client, mock_cart):
    mock_cart.calculate_total_price.return_value = 0.0
    response = client.get('/calculate_total_price')
    assert response.status_code == 200
    assert response.json['total_price'] == 0.0


# edge case - apply_discount_to_cart - Test applying discount with higher min purchase than total
def test_apply_discount_high_min_purchase(client):
    response = client.post('/apply_discount', json={
        'discount_rate': 0.1,
        'min_purchase_amount': 100
    })
    assert response.status_code == 200
    assert response.json['discounted_total'] == 50.0


# edge case - apply_promotions_to_cart - Test applying promotions with no applicable promotions
def test_apply_promotions_no_applicable(client, mock_apply_promotions):
    mock_apply_promotions.return_value = None
    response = client.post('/apply_promotions')
    assert response.status_code == 200
    assert response.json['message'] == 'No promotions applicable'


