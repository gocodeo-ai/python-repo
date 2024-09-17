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
        instance.calculate_total_price.return_value = 21.0
        instance.total_price = 21.0
        yield instance

@pytest.fixture
def mock_discount():
    with patch('app.Discount') as MockDiscount:
        instance = MockDiscount.return_value
        instance.apply_discount.return_value = None
        yield instance

@pytest.fixture
def mock_apply_promotions():
    with patch('app.apply_promotions') as mock_apply:
        yield mock_apply

@pytest.fixture
def mock_get_all_items_from_cart():
    with patch('app.get_all_items_from_cart') as mock_get_all:
        mock_get_all.return_value = [{'item_id': 1, 'quantity': 2, 'price': 10.5, 'name': 'Test Item', 'category': 'Electronics'}]
        yield mock_get_all

@pytest.fixture
def mock_promotion():
    with patch('app.Promotion') as MockPromotion:
        instance = MockPromotion.return_value
        yield instance

# happy_path - test_add_item_success - Test that adding an item to the cart returns a success message
def test_add_item_success(client, mock_cart):
    response = client.post('/add_item', json={
        'item_id': 1, 'quantity': 2, 'price': 10.5, 'name': 'Test Item', 'category': 'Electronics'
    })
    assert response.status_code == 201
    assert response.json == {'message': 'Item added to cart'}
    mock_cart.add_item.assert_called_once_with(1, 2, 10.5, 'Test Item', 'Electronics', 'regular')

# happy_path - test_remove_item_success - Test that removing an item from the cart returns a success message
def test_remove_item_success(client, mock_cart):
    response = client.post('/remove_item', json={'item_id': 1})
    assert response.status_code == 200
    assert response.json == {'message': 'Item removed from cart'}
    mock_cart.remove_item.assert_called_once_with(1)

# happy_path - test_update_item_quantity_success - Test that updating an item quantity in the cart returns a success message
def test_update_item_quantity_success(client, mock_cart):
    response = client.post('/update_item_quantity', json={'item_id': 1, 'new_quantity': 5})
    assert response.status_code == 200
    assert response.json == {'message': 'Item quantity updated'}
    mock_cart.update_item_quantity.assert_called_once_with(1, 5)

# happy_path - test_get_cart_items_success - Test that retrieving cart items returns the correct items list
def test_get_cart_items_success(client, mock_get_all_items_from_cart):
    response = client.get('/get_cart_items')
    assert response.status_code == 200
    assert response.json == {'items': [{'item_id': 1, 'quantity': 2, 'price': 10.5, 'name': 'Test Item', 'category': 'Electronics'}]}
    mock_get_all_items_from_cart.assert_called_once_with(mock_cart)

# happy_path - test_calculate_total_price_success - Test that calculating total price returns the correct total
def test_calculate_total_price_success(client, mock_cart):
    response = client.get('/calculate_total_price')
    assert response.status_code == 200
    assert response.json == {'total_price': 21.0}
    mock_cart.calculate_total_price.assert_called_once()

# happy_path - test_apply_discount_success - Test that applying a discount returns the correct discounted total
def test_apply_discount_success(client, mock_cart, mock_discount):
    response = client.post('/apply_discount', json={'discount_rate': 0.1, 'min_purchase_amount': 0})
    assert response.status_code == 200
    assert response.json == {'discounted_total': 18.9}
    mock_discount.assert_called_once_with(0.1, 0)
    mock_discount.return_value.apply_discount.assert_called_once_with(mock_cart)

# happy_path - test_apply_promotions_success - Test that applying promotions returns a success message
def test_apply_promotions_success(client, mock_cart, mock_apply_promotions, mock_promotion):
    response = client.post('/apply_promotions')
    assert response.status_code == 200
    assert response.json == {'message': 'Promotions applied'}
    mock_apply_promotions.assert_called_once_with(mock_cart, [mock_promotion.return_value, mock_promotion.return_value])

# edge_case - test_add_item_zero_quantity - Test that adding an item with zero quantity returns an error
def test_add_item_zero_quantity(client, mock_cart):
    response = client.post('/add_item', json={
        'item_id': 1, 'quantity': 0, 'price': 10.5, 'name': 'Test Item', 'category': 'Electronics'
    })
    assert response.status_code == 400
    assert response.json == {'message': 'Quantity must be greater than zero'}

# edge_case - test_remove_non_existent_item - Test that removing a non-existent item returns an error
def test_remove_non_existent_item(client, mock_cart):
    mock_cart.remove_item.side_effect = KeyError('Item not found')
    response = client.post('/remove_item', json={'item_id': 999})
    assert response.status_code == 404
    assert response.json == {'message': 'Item not found'}

# edge_case - test_update_quantity_to_zero - Test that updating quantity to zero removes the item
def test_update_quantity_to_zero(client, mock_cart):
    response = client.post('/update_item_quantity', json={'item_id': 1, 'new_quantity': 0})
    assert response.status_code == 200
    assert response.json == {'message': 'Item removed from cart'}
    mock_cart.update_item_quantity.assert_called_once_with(1, 0)

# edge_case - test_get_cart_items_empty_cart - Test that retrieving items from an empty cart returns an empty list
def test_get_cart_items_empty_cart(client, mock_get_all_items_from_cart):
    mock_get_all_items_from_cart.return_value = []
    response = client.get('/get_cart_items')
    assert response.status_code == 200
    assert response.json == {'items': []}
    mock_get_all_items_from_cart.assert_called_once_with(mock_cart)

# edge_case - test_apply_discount_above_minimum - Test that applying a discount with a minimum purchase amount higher than total returns no discount
def test_apply_discount_above_minimum(client, mock_cart, mock_discount):
    response = client.post('/apply_discount', json={'discount_rate': 0.1, 'min_purchase_amount': 100})
    assert response.status_code == 200
    assert response.json == {'discounted_total': 21.0}
    mock_discount.assert_called_once_with(0.1, 100)
    mock_discount.return_value.apply_discount.assert_called_once_with(mock_cart)

# edge_case - test_apply_promotions_empty_cart - Test that applying promotions on an empty cart returns a success message but no changes
def test_apply_promotions_empty_cart(client, mock_cart, mock_apply_promotions, mock_promotion):
    response = client.post('/apply_promotions')
    assert response.status_code == 200
    assert response.json == {'message': 'Promotions applied'}
    mock_apply_promotions.assert_called_once_with(mock_cart, [mock_promotion.return_value, mock_promotion.return_value])

