import pytest
from unittest.mock import patch, MagicMock
from shopping_cart.cart import Cart
from shopping_cart.discounts import Discount
from shopping_cart.payments import apply_promotions, Promotion
from shopping_cart.utils import get_all_items_from_cart
from app import app

@pytest.fixture
def mock_cart():
    with patch('app.cart', new_callable=MagicMock) as mock:
        yield mock

@pytest.fixture
def mock_discount():
    with patch('app.Discount', new_callable=MagicMock) as mock:
        yield mock

@pytest.fixture
def mock_apply_promotions():
    with patch('app.apply_promotions', new_callable=MagicMock) as mock:
        yield mock

@pytest.fixture
def mock_get_all_items_from_cart():
    with patch('app.get_all_items_from_cart', new_callable=MagicMock) as mock:
        yield mock

@pytest.fixture
def mock_promotion():
    with patch('app.Promotion', new_callable=MagicMock) as mock:
        yield mock

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

# happy path - add_item - Test that an item can be added to the cart successfully
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


# happy path - remove_item - Test that an item can be removed from the cart successfully
def test_remove_item_success(client, mock_cart):
    response = client.post('/remove_item', json={'item_id': 1})
    assert response.status_code == 200
    assert response.json == {'message': 'Item removed from cart'}
    mock_cart.remove_item.assert_called_once_with(1)


# happy path - update_item_quantity - Test that item quantity can be updated in the cart successfully
def test_update_item_quantity_success(client, mock_cart):
    response = client.post('/update_item_quantity', json={'item_id': 1, 'new_quantity': 5})
    assert response.status_code == 200
    assert response.json == {'message': 'Item quantity updated'}
    mock_cart.update_item_quantity.assert_called_once_with(1, 5)


# happy path - get_cart_items - Test that all items can be retrieved from the cart successfully
def test_get_cart_items_success(client, mock_get_all_items_from_cart):
    mock_get_all_items_from_cart.return_value = [{'item_id': 1, 'quantity': 5, 'price': 19.99, 'name': 'Widget', 'category': 'Gadgets'}]
    response = client.get('/get_cart_items')
    assert response.status_code == 200
    assert response.json == {'items': [{'item_id': 1, 'quantity': 5, 'price': 19.99, 'name': 'Widget', 'category': 'Gadgets'}]}
    mock_get_all_items_from_cart.assert_called_once_with(mock_cart)


# happy path - calculate_total_price - Test that total price can be calculated successfully for the cart
def test_calculate_total_price_success(client, mock_cart):
    mock_cart.calculate_total_price.return_value = 99.95
    response = client.get('/calculate_total_price')
    assert response.status_code == 200
    assert response.json == {'total_price': 99.95}
    mock_cart.calculate_total_price.assert_called_once()


# happy path - apply_discount_to_cart - Test that discount can be applied to the cart successfully
def test_apply_discount_to_cart_success(client, mock_discount, mock_cart):
    response = client.post('/apply_discount', json={'discount_rate': 0.1, 'min_purchase_amount': 50})
    assert response.status_code == 200
    assert response.json == {'discounted_total': mock_cart.total_price}
    mock_discount.assert_called_once_with(0.1, 50)
    mock_discount.return_value.apply_discount.assert_called_once_with(mock_cart)


# happy path - apply_promotions_to_cart - Test that promotions can be applied to the cart successfully
def test_apply_promotions_to_cart_success(client, mock_apply_promotions, mock_promotion, mock_cart):
    response = client.post('/apply_promotions')
    assert response.status_code == 200
    assert response.json == {'message': 'Promotions applied'}
    mock_apply_promotions.assert_called_once()
    mock_promotion.assert_any_call('Spring Sale', 0.10)
    mock_promotion.assert_any_call('Black Friday', 0.25)


# edge case - add_item - Test adding an item with an invalid item_id
def test_add_item_invalid_id(client, mock_cart):
    response = client.post('/add_item', json={
        'item_id': -1,
        'quantity': 2,
        'price': 19.99,
        'name': 'Widget',
        'category': 'Gadgets'
    })
    assert response.status_code == 400
    assert response.json == {'error': 'Invalid item_id'}


# edge case - remove_item - Test removing an item that does not exist in the cart
def test_remove_nonexistent_item(client, mock_cart):
    mock_cart.remove_item.side_effect = KeyError('Item not found')
    response = client.post('/remove_item', json={'item_id': 999})
    assert response.status_code == 404
    assert response.json == {'error': 'Item not found'}


# edge case - update_item_quantity - Test updating item quantity to zero
def test_update_item_quantity_to_zero(client, mock_cart):
    response = client.post('/update_item_quantity', json={'item_id': 1, 'new_quantity': 0})
    assert response.status_code == 400
    assert response.json == {'error': 'Invalid quantity'}


# edge case - calculate_total_price - Test calculating total price with an empty cart
def test_calculate_total_price_empty_cart(client, mock_cart):
    mock_cart.calculate_total_price.return_value = 0
    response = client.get('/calculate_total_price')
    assert response.status_code == 200
    assert response.json == {'total_price': 0}
    mock_cart.calculate_total_price.assert_called_once()


# edge case - apply_discount_to_cart - Test applying a discount with a rate greater than 1
def test_apply_discount_invalid_rate(client, mock_discount):
    response = client.post('/apply_discount', json={'discount_rate': 1.5, 'min_purchase_amount': 50})
    assert response.status_code == 400
    assert response.json == {'error': 'Invalid discount rate'}


# edge case - apply_promotions_to_cart - Test applying promotions with no applicable promotions
def test_apply_promotions_no_applicable(client, mock_apply_promotions):
    mock_apply_promotions.side_effect = ValueError('No promotions applicable')
    response = client.post('/apply_promotions')
    assert response.status_code == 400
    assert response.json == {'message': 'No promotions applicable'}


