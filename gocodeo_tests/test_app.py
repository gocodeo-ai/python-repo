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
        instance.calculate_total_price = MagicMock(return_value=0)
        yield instance

@pytest.fixture
def mock_discount():
    with patch('app.Discount') as MockDiscount:
        instance = MockDiscount.return_value
        instance.apply_discount = MagicMock()
        yield instance

@pytest.fixture
def mock_apply_promotions():
    with patch('app.apply_promotions') as mock_apply_promotions_func:
        yield mock_apply_promotions_func

@pytest.fixture
def mock_get_all_items_from_cart():
    with patch('app.get_all_items_from_cart') as mock_get_items_func:
        mock_get_items_func.return_value = [{'item_id': 1, 'quantity': 3, 'price': 10.5, 'name': 'Test Item', 'category': 'Electronics'}]
        yield mock_get_items_func

@pytest.fixture
def mock_promotion():
    with patch('app.Promotion') as MockPromotion:
        yield MockPromotion

@pytest.fixture(autouse=True)
def setup_mocks(mock_cart, mock_discount, mock_apply_promotions, mock_get_all_items_from_cart, mock_promotion):
    pass

# happy_path - test_add_item_success - Test that item is added to cart with valid inputs
def test_add_item_success(client, mock_cart):
    response = client.post('/add_item', json={
        'item_id': 1,
        'quantity': 2,
        'price': 10.5,
        'name': 'Test Item',
        'category': 'Electronics'
    })
    assert response.status_code == 201
    assert response.json == {'message': 'Item added to cart'}
    mock_cart.add_item.assert_called_once_with(1, 2, 10.5, 'Test Item', 'Electronics', 'regular')

# happy_path - test_remove_item_success - Test that item is removed from cart with valid item_id
def test_remove_item_success(client, mock_cart):
    response = client.post('/remove_item', json={'item_id': 1})
    assert response.status_code == 200
    assert response.json == {'message': 'Item removed from cart'}
    mock_cart.remove_item.assert_called_once_with(1)

# happy_path - test_update_item_quantity_success - Test that item quantity is updated in cart with valid item_id and quantity
def test_update_item_quantity_success(client, mock_cart):
    response = client.post('/update_item_quantity', json={'item_id': 1, 'new_quantity': 3})
    assert response.status_code == 200
    assert response.json == {'message': 'Item quantity updated'}
    mock_cart.update_item_quantity.assert_called_once_with(1, 3)

# happy_path - test_get_cart_items_success - Test that all items are retrieved from cart
def test_get_cart_items_success(client, mock_get_all_items_from_cart):
    response = client.get('/get_cart_items')
    assert response.status_code == 200
    assert response.json == {'items': [{'item_id': 1, 'quantity': 3, 'price': 10.5, 'name': 'Test Item', 'category': 'Electronics'}]}
    mock_get_all_items_from_cart.assert_called_once()

# happy_path - test_calculate_total_price_success - Test that total price is calculated correctly
def test_calculate_total_price_success(client, mock_cart):
    mock_cart.calculate_total_price.return_value = 31.5
    response = client.get('/calculate_total_price')
    assert response.status_code == 200
    assert response.json == {'total_price': 31.5}
    mock_cart.calculate_total_price.assert_called_once()

# happy_path - test_apply_discount_success - Test that discount is applied to cart with valid discount rate
def test_apply_discount_success(client, mock_discount, mock_cart):
    mock_cart.total_price = 28.35
    response = client.post('/apply_discount', json={'discount_rate': 0.1, 'min_purchase_amount': 0})
    assert response.status_code == 200
    assert response.json == {'discounted_total': 28.35}
    mock_discount.assert_called_once_with(0.1, 0)
    mock_discount.return_value.apply_discount.assert_called_once_with(mock_cart)

# happy_path - test_apply_promotions_success - Test that promotions are applied to cart
def test_apply_promotions_success(client, mock_apply_promotions, mock_cart, mock_promotion):
    response = client.post('/apply_promotions')
    assert response.status_code == 200
    assert response.json == {'message': 'Promotions applied'}
    assert mock_apply_promotions.called
    assert mock_promotion.called

# edge_case - test_add_item_invalid_item_id - Test that adding item with invalid item_id raises error
def test_add_item_invalid_item_id(client):
    response = client.post('/add_item', json={
        'item_id': 'invalid',
        'quantity': 2,
        'price': 10.5,
        'name': 'Test Item',
        'category': 'Electronics'
    })
    assert response.status_code == 400
    assert response.json == {'error': 'Invalid item_id'}

# edge_case - test_remove_item_non_existent_item_id - Test that removing item with non-existent item_id raises error
def test_remove_item_non_existent_item_id(client, mock_cart):
    mock_cart.remove_item.side_effect = ValueError('Item not found')
    response = client.post('/remove_item', json={'item_id': 999})
    assert response.status_code == 404
    assert response.json == {'error': 'Item not found'}

# edge_case - test_update_item_quantity_zero_quantity - Test that updating item quantity with zero quantity raises error
def test_update_item_quantity_zero_quantity(client, mock_cart):
    mock_cart.update_item_quantity.side_effect = ValueError('Quantity must be greater than zero')
    response = client.post('/update_item_quantity', json={'item_id': 1, 'new_quantity': 0})
    assert response.status_code == 400
    assert response.json == {'error': 'Quantity must be greater than zero'}

# edge_case - test_calculate_total_price_empty_cart - Test that calculating total price with empty cart returns zero
def test_calculate_total_price_empty_cart(client, mock_cart):
    mock_cart.calculate_total_price.return_value = 0
    response = client.get('/calculate_total_price')
    assert response.status_code == 200
    assert response.json == {'total_price': 0}
    mock_cart.calculate_total_price.assert_called_once()

# edge_case - test_apply_discount_exceeding_rate - Test that applying discount with rate exceeding 1 raises error
def test_apply_discount_exceeding_rate(client):
    response = client.post('/apply_discount', json={'discount_rate': 1.5, 'min_purchase_amount': 0})
    assert response.status_code == 400
    assert response.json == {'error': 'Discount rate must be between 0 and 1'}

# edge_case - test_apply_promotions_no_promotions - Test that applying promotions with no promotions available returns no change
def test_apply_promotions_no_promotions(client, mock_apply_promotions):
    mock_apply_promotions.side_effect = lambda cart, promotions: None
    response = client.post('/apply_promotions')
    assert response.status_code == 200
    assert response.json == {'message': 'No promotions applied'}
    mock_apply_promotions.assert_called_once()

