import pytest
from unittest.mock import MagicMock, patch
from shopping_cart.cart import Cart
from shopping_cart.discounts import Discount
from demo.shopping_cart.payments import apply_promotions, Promotion
from shopping_cart.utils import get_all_items_from_cart
from app import app

@pytest.fixture
def mock_cart():
    with patch('shopping_cart.cart.Cart', autospec=True) as mock:
        yield mock

@pytest.fixture
def mock_discount():
    with patch('shopping_cart.discounts.Discount', autospec=True) as mock:
        yield mock

@pytest.fixture
def mock_apply_promotions():
    with patch('demo.shopping_cart.payments.apply_promotions', autospec=True) as mock:
        yield mock

@pytest.fixture
def mock_promotion():
    with patch('demo.shopping_cart.payments.Promotion', autospec=True) as mock:
        yield mock

@pytest.fixture
def mock_get_all_items_from_cart():
    with patch('shopping_cart.utils.get_all_items_from_cart', autospec=True) as mock:
        yield mock

@pytest.fixture
def client():
    app.testing = True
    with app.test_client() as client:
        yield client

# happy path - add_item - Test that an item can be added to the cart successfully
def test_add_item_success(client, mock_cart):
    response = client.post('/add_item', json={
        'item_id': 1,
        'quantity': 2,
        'price': 10.0,
        'name': 'Apple',
        'category': 'Fruit'
    })
    assert response.json == {'message': 'Item added to cart'}
    assert response.status_code == 201
    mock_cart.return_value.add_item.assert_called_once_with(1, 2, 10.0, 'Apple', 'Fruit')


# happy path - remove_item - Test that an item can be removed from the cart successfully
def test_remove_item_success(client, mock_cart):
    response = client.post('/remove_item', json={'item_id': 1})
    assert response.json == {'message': 'Item removed from cart'}
    assert response.status_code == 200
    mock_cart.return_value.remove_item.assert_called_once_with(1)


# happy path - update_item_quantity - Test that the quantity of an item can be updated successfully
def test_update_item_quantity_success(client, mock_cart):
    response = client.post('/update_item_quantity', json={'item_id': 1, 'new_quantity': 5})
    assert response.json == {'message': 'Item quantity updated'}
    assert response.status_code == 200
    mock_cart.return_value.update_item_quantity.assert_called_once_with(1, 5)


# happy path - get_cart_items - Test that all items in the cart can be retrieved successfully
def test_get_cart_items_success(client, mock_get_all_items_from_cart):
    mock_get_all_items_from_cart.return_value = [{'item_id': 1, 'quantity': 2, 'price': 10.0, 'name': 'Apple', 'category': 'Fruit'}]
    response = client.get('/get_cart_items')
    assert response.json == {'items': [{'item_id': 1, 'quantity': 2, 'price': 10.0, 'name': 'Apple', 'category': 'Fruit'}]}
    mock_get_all_items_from_cart.assert_called_once()


# happy path - calculate_total_price - Test that the total price of the cart can be calculated successfully
def test_calculate_total_price_success(client, mock_cart):
    mock_cart.return_value.calculate_total_price.return_value = 20.0
    response = client.get('/calculate_total_price')
    assert response.json == {'total_price': 20.0}
    mock_cart.return_value.calculate_total_price.assert_called_once()


# happy path - apply_discount_to_cart - Test that a discount can be applied to the cart successfully
def test_apply_discount_success(client, mock_cart, mock_discount):
    response = client.post('/apply_discount', json={'discount_rate': 0.1, 'min_purchase_amount': 0})
    assert response.json == {'discounted_total': mock_cart.return_value.total_price}
    mock_discount.assert_called_once_with(0.1, 0)
    mock_discount.return_value.apply_discount.assert_called_once_with(mock_cart.return_value)


# happy path - apply_promotions_to_cart - Test that promotions can be applied to the cart successfully
def test_apply_promotions_success(client, mock_cart, mock_apply_promotions, mock_promotion):
    response = client.post('/apply_promotions')
    assert response.json == {'message': 'Promotions applied'}
    mock_apply_promotions.assert_called_once_with(mock_cart.return_value, [mock_promotion.return_value, mock_promotion.return_value])


# edge case - add_item - Test adding an item with zero quantity
def test_add_item_zero_quantity(client, mock_cart):
    response = client.post('/add_item', json={
        'item_id': 1,
        'quantity': 0,
        'price': 10.0,
        'name': 'Apple',
        'category': 'Fruit'
    })
    assert response.json == {'message': 'Item added to cart'}
    assert response.status_code == 201
    mock_cart.return_value.add_item.assert_called_once_with(1, 0, 10.0, 'Apple', 'Fruit')


# edge case - remove_item - Test removing an item not present in the cart
def test_remove_nonexistent_item(client, mock_cart):
    response = client.post('/remove_item', json={'item_id': 999})
    assert response.json == {'message': 'Item removed from cart'}
    assert response.status_code == 200
    mock_cart.return_value.remove_item.assert_called_once_with(999)


# edge case - update_item_quantity - Test updating item quantity to zero
def test_update_item_quantity_to_zero(client, mock_cart):
    response = client.post('/update_item_quantity', json={'item_id': 1, 'new_quantity': 0})
    assert response.json == {'message': 'Item quantity updated'}
    assert response.status_code == 200
    mock_cart.return_value.update_item_quantity.assert_called_once_with(1, 0)


# edge case - get_cart_items - Test retrieving items from an empty cart
def test_get_cart_items_empty_cart(client, mock_get_all_items_from_cart):
    mock_get_all_items_from_cart.return_value = []
    response = client.get('/get_cart_items')
    assert response.json == {'items': []}
    mock_get_all_items_from_cart.assert_called_once()


# edge case - calculate_total_price - Test calculating total price of an empty cart
def test_calculate_total_price_empty_cart(client, mock_cart):
    mock_cart.return_value.calculate_total_price.return_value = 0.0
    response = client.get('/calculate_total_price')
    assert response.json == {'total_price': 0.0}
    mock_cart.return_value.calculate_total_price.assert_called_once()


# edge case - apply_discount_to_cart - Test applying discount with a rate higher than 100%
def test_apply_discount_over_100_percent(client, mock_cart, mock_discount):
    response = client.post('/apply_discount', json={'discount_rate': 1.5, 'min_purchase_amount': 0})
    assert response.json == {'discounted_total': 0.0}
    mock_discount.assert_called_once_with(1.5, 0)
    mock_discount.return_value.apply_discount.assert_called_once_with(mock_cart.return_value)


# edge case - apply_promotions_to_cart - Test applying promotions with conflicting rules
def test_apply_conflicting_promotions(client, mock_cart, mock_apply_promotions, mock_promotion):
    response = client.post('/apply_promotions')
    assert response.json == {'message': 'Promotions applied'}
    mock_apply_promotions.assert_called_once_with(mock_cart.return_value, [mock_promotion.return_value, mock_promotion.return_value])


