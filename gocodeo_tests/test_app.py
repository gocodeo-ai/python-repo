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
def mock_promotion():
    with patch('app.Promotion', new_callable=MagicMock) as mock:
        yield mock

@pytest.fixture
def mock_get_all_items_from_cart():
    with patch('app.get_all_items_from_cart', new_callable=MagicMock) as mock:
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
        'price': 9.99,
        'name': 'Widget',
        'category': 'Gadgets'
    })
    assert response.status_code == 201
    assert response.json == {'message': 'Item added to cart'}
    mock_cart.add_item.assert_called_once_with(1, 2, 9.99, 'Widget', 'Gadgets', 'regular')


# happy path - remove_item - Test that an item can be removed from the cart successfully
def test_remove_item_success(client, mock_cart):
    response = client.post('/remove_item', json={'item_id': 1})
    assert response.status_code == 200
    assert response.json == {'message': 'Item removed from cart'}
    mock_cart.remove_item.assert_called_once_with(1)


# happy path - update_item_quantity - Test that the quantity of an item can be updated successfully
def test_update_item_quantity_success(client, mock_cart):
    response = client.post('/update_item_quantity', json={'item_id': 1, 'new_quantity': 5})
    assert response.status_code == 200
    assert response.json == {'message': 'Item quantity updated'}
    mock_cart.update_item_quantity.assert_called_once_with(1, 5)


# happy path - get_cart_items - Test that all items can be retrieved from the cart
def test_get_cart_items_success(client, mock_get_all_items_from_cart):
    mock_get_all_items_from_cart.return_value = [{'item_id': 1, 'quantity': 2, 'price': 9.99, 'name': 'Widget', 'category': 'Gadgets'}]
    response = client.get('/get_cart_items')
    assert response.status_code == 200
    assert response.json == {'items': [{'item_id': 1, 'quantity': 2, 'price': 9.99, 'name': 'Widget', 'category': 'Gadgets'}]}
    mock_get_all_items_from_cart.assert_called_once()


# happy path - calculate_total_price - Test that the total price of the cart is calculated correctly
def test_calculate_total_price_success(client, mock_cart):
    mock_cart.calculate_total_price.return_value = 19.98
    response = client.get('/calculate_total_price')
    assert response.status_code == 200
    assert response.json == {'total_price': 19.98}
    mock_cart.calculate_total_price.assert_called_once()


# happy path - apply_discount_to_cart - Test that a discount can be applied to the cart successfully
def test_apply_discount_success(client, mock_cart, mock_discount):
    response = client.post('/apply_discount', json={'discount_rate': 0.1, 'min_purchase_amount': 0})
    assert response.status_code == 200
    assert response.json == {'discounted_total': mock_cart.total_price}
    mock_discount.assert_called_once_with(0.1, 0)
    mock_discount().apply_discount.assert_called_once_with(mock_cart)


# happy path - apply_promotions_to_cart - Test that promotions can be applied to the cart successfully
def test_apply_promotions_success(client, mock_cart, mock_apply_promotions, mock_promotion):
    response = client.post('/apply_promotions')
    assert response.status_code == 200
    assert response.json == {'message': 'Promotions applied'}
    mock_apply_promotions.assert_called_once_with(mock_cart, [mock_promotion(), mock_promotion()])


# edge case - add_item - Test adding an item with a negative quantity
def test_add_item_negative_quantity(client, mock_cart):
    response = client.post('/add_item', json={
        'item_id': 1,
        'quantity': -1,
        'price': 9.99,
        'name': 'Widget',
        'category': 'Gadgets'
    })
    assert response.status_code == 400
    assert response.json == {'error': 'Invalid quantity'}
    mock_cart.add_item.assert_not_called()


# edge case - remove_item - Test removing an item not present in the cart
def test_remove_item_not_in_cart(client, mock_cart):
    mock_cart.remove_item.side_effect = Exception('Item not found in cart')
    response = client.post('/remove_item', json={'item_id': 999})
    assert response.status_code == 404
    assert response.json == {'error': 'Item not found in cart'}
    mock_cart.remove_item.assert_called_once_with(999)


# edge case - update_item_quantity - Test updating the quantity of an item not present in the cart
def test_update_item_quantity_not_in_cart(client, mock_cart):
    mock_cart.update_item_quantity.side_effect = Exception('Item not found in cart')
    response = client.post('/update_item_quantity', json={'item_id': 999, 'new_quantity': 5})
    assert response.status_code == 404
    assert response.json == {'error': 'Item not found in cart'}
    mock_cart.update_item_quantity.assert_called_once_with(999, 5)


# edge case - calculate_total_price - Test calculating total price with an empty cart
def test_calculate_total_price_empty_cart(client, mock_cart):
    mock_cart.calculate_total_price.return_value = 0
    response = client.get('/calculate_total_price')
    assert response.status_code == 200
    assert response.json == {'total_price': 0}
    mock_cart.calculate_total_price.assert_called_once()


# edge case - apply_discount_to_cart - Test applying a discount with rate greater than 1
def test_apply_discount_rate_greater_than_one(client, mock_cart, mock_discount):
    response = client.post('/apply_discount', json={'discount_rate': 1.5, 'min_purchase_amount': 0})
    assert response.status_code == 400
    assert response.json == {'error': 'Invalid discount rate'}
    mock_discount.assert_not_called()


# edge case - apply_promotions_to_cart - Test applying promotions when none are applicable
def test_apply_no_applicable_promotions(client, mock_cart, mock_apply_promotions):
    mock_apply_promotions.return_value = False
    response = client.post('/apply_promotions')
    assert response.status_code == 200
    assert response.json == {'message': 'No promotions applied'}
    mock_apply_promotions.assert_called_once_with(mock_cart, [mock_promotion(), mock_promotion()])


