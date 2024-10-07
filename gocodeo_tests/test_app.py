import pytest
from unittest.mock import patch, MagicMock
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
    with patch('app.Cart') as MockCart:
        instance = MockCart.return_value
        instance.add_item = MagicMock()
        instance.remove_item = MagicMock()
        instance.update_item_quantity = MagicMock()
        instance.calculate_total_price = MagicMock(return_value=39.98)
        instance.total_price = 39.98
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
    with patch('app.get_all_items_from_cart') as mock_get:
        mock_get.return_value = [{'item_id': 1, 'quantity': 2, 'price': 19.99, 'name': 'T-shirt', 'category': 'clothing'}]
        yield mock_get

@pytest.fixture
def mock_promotion():
    with patch('app.Promotion') as MockPromotion:
        instance = MockPromotion.return_value
        yield instance

# happy_path - add_item - Test that item is added to the cart successfully with valid data
def test_add_item_success(client, mock_cart):
    response = client.post('/add_item', json={
        'item_id': 1,
        'quantity': 2,
        'price': 19.99,
        'name': 'T-shirt',
        'category': 'clothing'
    })
    assert response.status_code == 201
    assert response.json == {'message': 'Item added to cart'}
    mock_cart.add_item.assert_called_once_with(1, 2, 19.99, 'T-shirt', 'clothing', 'regular')

# happy_path - remove_item - Test that item is removed from the cart successfully
def test_remove_item_success(client, mock_cart):
    response = client.post('/remove_item', json={'item_id': 1})
    assert response.status_code == 200
    assert response.json == {'message': 'Item removed from cart'}
    mock_cart.remove_item.assert_called_once_with(1)

# happy_path - update_item_quantity - Test that item quantity is updated successfully
def test_update_item_quantity_success(client, mock_cart):
    response = client.post('/update_item_quantity', json={'item_id': 1, 'new_quantity': 5})
    assert response.status_code == 200
    assert response.json == {'message': 'Item quantity updated'}
    mock_cart.update_item_quantity.assert_called_once_with(1, 5)

# happy_path - get_cart_items - Test that all items are retrieved from the cart
def test_get_cart_items_success(client, mock_get_all_items_from_cart):
    response = client.get('/get_cart_items')
    assert response.status_code == 200
    assert response.json == {'items': [{'item_id': 1, 'quantity': 2, 'price': 19.99, 'name': 'T-shirt', 'category': 'clothing'}]}
    mock_get_all_items_from_cart.assert_called_once()

# happy_path - calculate_total_price - Test that total price is calculated successfully
def test_calculate_total_price_success(client, mock_cart):
    response = client.get('/calculate_total_price')
    assert response.status_code == 200
    assert response.json == {'total_price': 39.98}
    mock_cart.calculate_total_price.assert_called_once()

# happy_path - apply_discount_to_cart - Test that discount is applied to the cart successfully
def test_apply_discount_success(client, mock_cart, mock_discount):
    response = client.post('/apply_discount', json={'discount_rate': 0.1, 'min_purchase_amount': 20.0})
    assert response.status_code == 200
    assert response.json == {'discounted_total': 39.98}
    mock_discount.assert_called_once_with(0.1, 20.0)
    mock_discount.return_value.apply_discount.assert_called_once_with(mock_cart)

# happy_path - apply_promotions_to_cart - Test that promotions are applied to the cart successfully
def test_apply_promotions_success(client, mock_cart, mock_apply_promotions, mock_promotion):
    response = client.post('/apply_promotions')
    assert response.status_code == 200
    assert response.json == {'message': 'Promotions applied'}
    mock_apply_promotions.assert_called_once_with(mock_cart, [mock_promotion.return_value, mock_promotion.return_value])

# edge_case - add_item - Test adding an item with negative quantity
def test_add_item_negative_quantity(client, mock_cart):
    response = client.post('/add_item', json={
        'item_id': 1,
        'quantity': -1,
        'price': 19.99,
        'name': 'T-shirt',
        'category': 'clothing'
    })
    assert response.status_code == 400
    assert response.json == {'error': 'Invalid quantity'}
    mock_cart.add_item.assert_not_called()

# edge_case - remove_item - Test removing an item not in the cart
def test_remove_item_not_in_cart(client, mock_cart):
    response = client.post('/remove_item', json={'item_id': 999})
    assert response.status_code == 404
    assert response.json == {'error': 'Item not found'}
    mock_cart.remove_item.assert_called_once_with(999)

# edge_case - update_item_quantity - Test updating item quantity to zero
def test_update_item_quantity_to_zero(client, mock_cart):
    response = client.post('/update_item_quantity', json={'item_id': 1, 'new_quantity': 0})
    assert response.status_code == 400
    assert response.json == {'error': 'Invalid quantity'}
    mock_cart.update_item_quantity.assert_not_called()

# edge_case - get_cart_items - Test retrieving items from an empty cart
def test_get_cart_items_empty(client, mock_get_all_items_from_cart):
    mock_get_all_items_from_cart.return_value = []
    response = client.get('/get_cart_items')
    assert response.status_code == 200
    assert response.json == {'items': []}
    mock_get_all_items_from_cart.assert_called_once()

# edge_case - apply_discount_to_cart - Test applying discount with rate higher than 1
def test_apply_discount_rate_higher_than_one(client, mock_cart, mock_discount):
    response = client.post('/apply_discount', json={'discount_rate': 1.5, 'min_purchase_amount': 20.0})
    assert response.status_code == 400
    assert response.json == {'error': 'Invalid discount rate'}
    mock_discount.assert_not_called()

# edge_case - apply_promotions_to_cart - Test applying promotions when cart is empty
def test_apply_promotions_empty_cart(client, mock_cart, mock_apply_promotions, mock_promotion):
    mock_cart.total_price = 0
    response = client.post('/apply_promotions')
    assert response.status_code == 200
    assert response.json == {'message': 'No promotions applied'}
    mock_apply_promotions.assert_not_called()

