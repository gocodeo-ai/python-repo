import pytest
from unittest.mock import patch, MagicMock
from app import app
from shopping_cart.cart import Cart
from shopping_cart.discounts import Discount
from shopping_cart.payments import apply_promotions, Promotion
from shopping_cart.utils import get_all_items_from_cart

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

@pytest.fixture
def mock_cart():
    with patch('shopping_cart.cart.Cart') as MockCart:
        instance = MockCart.return_value
        instance.add_item = MagicMock()
        instance.remove_item = MagicMock()
        instance.update_item_quantity = MagicMock()
        instance.calculate_total_price = MagicMock(return_value=39.98)
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
        mock_get_items.return_value = [{'item_id': 1, 'quantity': 2, 'price': 19.99, 'name': 'T-shirt', 'category': 'Clothing'}]
        yield mock_get_items

# happy path - add_item - Test that an item is successfully added to the cart with valid input data
def test_add_item_success(client, mock_cart):
    response = client.post('/add_item', json={
        'item_id': 1,
        'quantity': 2,
        'price': 19.99,
        'name': 'T-shirt',
        'category': 'Clothing'
    })
    assert response.status_code == 201
    assert response.json == {'message': 'Item added to cart'}
    mock_cart.add_item.assert_called_once_with(1, 2, 19.99, 'T-shirt', 'Clothing', 'regular')


# happy path - remove_item - Test that an item is successfully removed from the cart with valid input data
def test_remove_item_success(client, mock_cart):
    response = client.post('/remove_item', json={'item_id': 1})
    assert response.status_code == 200
    assert response.json == {'message': 'Item removed from cart'}
    mock_cart.remove_item.assert_called_once_with(1)


# happy path - update_item_quantity - Test that item quantity is successfully updated in the cart with valid input data
def test_update_item_quantity_success(client, mock_cart):
    response = client.post('/update_item_quantity', json={
        'item_id': 1,
        'new_quantity': 5
    })
    assert response.status_code == 200
    assert response.json == {'message': 'Item quantity updated'}
    mock_cart.update_item_quantity.assert_called_once_with(1, 5)


# happy path - get_cart_items - Test that all items are retrieved from the cart successfully
def test_get_cart_items_success(client, mock_get_all_items_from_cart):
    response = client.get('/get_cart_items')
    assert response.status_code == 200
    assert response.json == {'items': [{'item_id': 1, 'quantity': 2, 'price': 19.99, 'name': 'T-shirt', 'category': 'Clothing'}]}
    mock_get_all_items_from_cart.assert_called_once()


# happy path - calculate_total_price - Test that total price is calculated correctly for the cart
def test_calculate_total_price_success(client, mock_cart):
    response = client.get('/calculate_total_price')
    assert response.status_code == 200
    assert response.json == {'total_price': 39.98}
    mock_cart.calculate_total_price.assert_called_once()


# happy path - apply_discount_to_cart - Test that discount is applied successfully with valid discount rate and minimum purchase amount
def test_apply_discount_to_cart_success(client, mock_cart, mock_discount):
    response = client.post('/apply_discount', json={
        'discount_rate': 0.1,
        'min_purchase_amount': 20.0
    })
    assert response.status_code == 200
    assert response.json == {'discounted_total': mock_cart.total_price}
    mock_discount.assert_called_once_with(0.1, 20.0)
    mock_discount.return_value.apply_discount.assert_called_once_with(mock_cart)


# happy path - apply_promotions_to_cart - Test that promotions are applied successfully to the cart
def test_apply_promotions_to_cart_success(client, mock_cart, mock_apply_promotions, mock_promotion):
    response = client.post('/apply_promotions')
    assert response.status_code == 200
    assert response.json == {'message': 'Promotions applied'}
    mock_apply_promotions.assert_called_once_with(mock_cart, [mock_promotion.return_value, mock_promotion.return_value])


# edge case - add_item - Test that adding an item with zero quantity returns an error
def test_add_item_zero_quantity(client, mock_cart):
    response = client.post('/add_item', json={
        'item_id': 1,
        'quantity': 0,
        'price': 19.99,
        'name': 'T-shirt',
        'category': 'Clothing'
    })
    assert response.status_code == 400
    assert response.json == {'error': 'Quantity must be greater than zero'}
    mock_cart.add_item.assert_not_called()


# edge case - remove_item - Test that removing an item not in the cart returns an error
def test_remove_item_not_in_cart(client, mock_cart):
    mock_cart.remove_item.side_effect = ValueError('Item not found in cart')
    response = client.post('/remove_item', json={'item_id': 999})
    assert response.status_code == 404
    assert response.json == {'error': 'Item not found in cart'}
    mock_cart.remove_item.assert_called_once_with(999)


# edge case - update_item_quantity - Test that updating item quantity to zero removes the item from the cart
def test_update_item_quantity_to_zero(client, mock_cart):
    response = client.post('/update_item_quantity', json={
        'item_id': 1,
        'new_quantity': 0
    })
    assert response.status_code == 200
    assert response.json == {'message': 'Item removed from cart'}
    mock_cart.update_item_quantity.assert_called_once_with(1, 0)


# edge case - get_cart_items - Test that retrieving items from an empty cart returns an empty list
def test_get_cart_items_empty(client, mock_get_all_items_from_cart):
    mock_get_all_items_from_cart.return_value = []
    response = client.get('/get_cart_items')
    assert response.status_code == 200
    assert response.json == {'items': []}
    mock_get_all_items_from_cart.assert_called_once()


# edge case - apply_discount_to_cart - Test that applying a discount with a rate greater than 1 returns an error
def test_apply_discount_rate_greater_than_one(client, mock_cart, mock_discount):
    response = client.post('/apply_discount', json={
        'discount_rate': 1.5,
        'min_purchase_amount': 20.0
    })
    assert response.status_code == 400
    assert response.json == {'error': 'Invalid discount rate'}
    mock_discount.assert_not_called()


# edge case - apply_promotions_to_cart - Test that applying promotions to an empty cart returns a specific message
def test_apply_promotions_to_empty_cart(client, mock_cart, mock_apply_promotions, mock_get_all_items_from_cart):
    mock_get_all_items_from_cart.return_value = []
    response = client.post('/apply_promotions')
    assert response.status_code == 200
    assert response.json == {'message': 'No promotions applied to empty cart'}
    mock_apply_promotions.assert_called_once_with(mock_cart, [mock_promotion.return_value, mock_promotion.return_value])


