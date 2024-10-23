import pytest
from unittest import mock
from shopping_cart.cart import Cart
from shopping_cart.discounts import Discount
from shopping_cart.payments import apply_promotions, Promotion
from shopping_cart.utils import get_all_items_from_cart
from app import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

@pytest.fixture
def mock_cart():
    with mock.patch('shopping_cart.cart.Cart') as MockCart:
        instance = MockCart.return_value
        instance.calculate_total_price.return_value = 0.0
        instance.add_item = mock.MagicMock()
        instance.remove_item = mock.MagicMock()
        instance.update_item_quantity = mock.MagicMock()
        instance.total_price = 0.0
        yield instance

@pytest.fixture
def mock_discount():
    with mock.patch('shopping_cart.discounts.Discount') as MockDiscount:
        instance = MockDiscount.return_value
        instance.apply_discount = mock.MagicMock()
        yield instance

@pytest.fixture
def mock_apply_promotions():
    with mock.patch('shopping_cart.payments.apply_promotions') as mock_apply:
        yield mock_apply

@pytest.fixture
def mock_get_all_items_from_cart():
    with mock.patch('shopping_cart.utils.get_all_items_from_cart') as mock_get_items:
        mock_get_items.return_value = []
        yield mock_get_items

# happy path - add_item - Test that item is added to cart successfully
def test_add_item_success(client, mock_cart):
    response = client.post('/add_item', json={
        'item_id': 1,
        'quantity': 2,
        'price': 10.99,
        'name': 'Test Item',
        'category': 'Electronics'
    })
    assert response.status_code == 201
    assert response.json == {'message': 'Item added to cart'}
    mock_cart.add_item.assert_called_once_with(1, 2, 10.99, 'Test Item', 'Electronics', 'regular')


# happy path - remove_item - Test that item is removed from cart successfully
def test_remove_item_success(client, mock_cart):
    response = client.post('/remove_item', json={'item_id': 1})
    assert response.status_code == 200
    assert response.json == {'message': 'Item removed from cart'}
    mock_cart.remove_item.assert_called_once_with(1)


# happy path - update_item_quantity - Test that item quantity is updated successfully
def test_update_item_quantity_success(client, mock_cart):
    response = client.post('/update_item_quantity', json={'item_id': 1, 'new_quantity': 5})
    assert response.status_code == 200
    assert response.json == {'message': 'Item quantity updated'}
    mock_cart.update_item_quantity.assert_called_once_with(1, 5)


# happy path - get_cart_items - Test that cart items are retrieved successfully
def test_get_cart_items_success(client, mock_get_all_items_from_cart):
    response = client.get('/get_cart_items')
    assert response.status_code == 200
    assert response.json == {'items': []}
    mock_get_all_items_from_cart.assert_called_once_with(mock.ANY)


# happy path - calculate_total_price - Test that total price is calculated successfully
def test_calculate_total_price_success(client, mock_cart):
    response = client.get('/calculate_total_price')
    assert response.status_code == 200
    assert response.json == {'total_price': 0.0}
    mock_cart.calculate_total_price.assert_called_once_with()


# happy path - apply_discount_to_cart - Test that discount is applied to cart successfully
def test_apply_discount_to_cart_success(client, mock_cart, mock_discount):
    response = client.post('/apply_discount', json={'discount_rate': 0.1, 'min_purchase_amount': 50.0})
    assert response.status_code == 200
    assert response.json == {'discounted_total': 0.0}
    mock_discount.assert_called_once_with(0.1, 50.0)
    mock_discount.return_value.apply_discount.assert_called_once_with(mock_cart)


# happy path - apply_promotions_to_cart - Test that promotions are applied to cart successfully
def test_apply_promotions_to_cart_success(client, mock_cart, mock_apply_promotions):
    response = client.post('/apply_promotions')
    assert response.status_code == 200
    assert response.json == {'message': 'Promotions applied'}
    mock_apply_promotions.assert_called_once_with(mock_cart, mock.ANY)


# edge case - add_item - Test that adding item with invalid item_id raises error
def test_add_item_invalid_item_id(client):
    response = client.post('/add_item', json={
        'item_id': 'invalid',
        'quantity': 2,
        'price': 10.99,
        'name': 'Test Item',
        'category': 'Electronics'
    })
    assert response.status_code == 400


# edge case - remove_item - Test that removing non-existent item raises error
def test_remove_item_non_existent(client, mock_cart):
    mock_cart.remove_item.side_effect = Exception('Item not found')
    response = client.post('/remove_item', json={'item_id': 999})
    assert response.status_code == 404


# edge case - update_item_quantity - Test that updating item quantity with negative value raises error
def test_update_item_quantity_negative(client):
    response = client.post('/update_item_quantity', json={'item_id': 1, 'new_quantity': -5})
    assert response.status_code == 400


# edge case - get_cart_items - Test that retrieving cart items when cart is empty returns empty list
def test_get_cart_items_empty_cart(client, mock_get_all_items_from_cart):
    response = client.get('/get_cart_items')
    assert response.status_code == 200
    assert response.json == {'items': []}
    mock_get_all_items_from_cart.assert_called_once_with(mock.ANY)


# edge case - apply_discount_to_cart - Test that applying discount with rate more than 1 raises error
def test_apply_discount_excessive_rate(client):
    response = client.post('/apply_discount', json={'discount_rate': 1.5, 'min_purchase_amount': 50.0})
    assert response.status_code == 400


# edge case - apply_promotions_to_cart - Test that applying promotions with no eligible promotions does not alter cart
def test_apply_promotions_no_eligible(client, mock_cart, mock_apply_promotions):
    mock_apply_promotions.side_effect = lambda cart, promotions: None
    response = client.post('/apply_promotions')
    assert response.status_code == 200
    assert response.json == {'message': 'Promotions applied'}
    mock_apply_promotions.assert_called_once_with(mock_cart, mock.ANY)


