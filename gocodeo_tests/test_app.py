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
        # MOCK HERE
        yield client


@pytest.fixture
def mock_discount():
    with patch('shopping_cart.discounts.Discount') as mock:
        instance = mock.return_value
        instance.apply_discount = MagicMock()
        yield instance

@pytest.fixture
def mock_get_all_items_from_cart():
    with patch('shopping_cart.utils.get_all_items_from_cart') as mock:
        mock.return_value = [{'item_id': 1, 'quantity': 2, 'price': 10.5, 'name': 'Test Item', 'category': 'Test Category'}]
        yield mock

@pytest.fixture
def mock_apply_promotions():
    with patch('shopping_cart.payments.apply_promotions') as mock:
        yield mock

@pytest.fixture
def mock_promotion():
    with patch('shopping_cart.payments.Promotion') as mock:
        instance = mock.return_value
        yield instance

# happy path - add_item - Test that an item is successfully added to the cart
def test_add_item_success(client):
    response = client.post('/add_item', json={
        'item_id': 1,
        'quantity': 2,
        'price': 10.5,
        'name': 'Test Item',
        'category': 'Test Category'
    })
    assert response.status_code == 201
    assert response.json['message'] == 'Item added to cart'

    # Validate if the item was added correctly
    with patch('shopping_cart.cart.Cart.add_item') as mock_add_item:
        mock_add_item.assert_called_once_with(1, 2, 10.5, 'Test Item', 'Test Category', 'regular')


# happy path - remove_item - Test that an item is successfully removed from the cart
def test_remove_item_success(client, mock_cart):
    response = client.post('/remove_item', json={'item_id': 1})
    assert response.status_code == 200
    assert response.json['message'] == 'Item removed from cart'
    mock_cart.remove_item.assert_called_once_with(1)


# happy path - update_item_quantity - Test that the item quantity is successfully updated in the cart
def test_update_item_quantity_success(client, mock_cart):
    response = client.post('/update_item_quantity', json={'item_id': 1, 'new_quantity': 5})
    assert response.status_code == 200
    assert response.json['message'] == 'Item quantity updated'
    mock_cart.update_item_quantity.assert_called_once_with(1, 5)


# happy path - get_cart_items - Test that all items are retrieved from the cart
def test_get_cart_items_success(client, mock_get_all_items_from_cart):
    response = client.get('/get_cart_items')
    assert response.status_code == 200
    assert response.json['items'] == [{'item_id': 1, 'quantity': 2, 'price': 10.5, 'name': 'Test Item', 'category': 'Test Category'}]
    mock_get_all_items_from_cart.assert_called_once()


# happy path - calculate_total_price - Test that the total price is calculated correctly
def test_calculate_total_price_success(client, mock_cart):
    response = client.get('/calculate_total_price')
    assert response.status_code == 200
    assert response.json['total_price'] == 21.0
    mock_cart.calculate_total_price.assert_called_once()


# happy path - apply_discount_to_cart - Test that a discount is applied correctly to the cart
def test_apply_discount_success(client, mock_cart, mock_discount):
    response = client.post('/apply_discount', json={'discount_rate': 0.2, 'min_purchase_amount': 10.0})
    assert response.status_code == 200
    assert response.json['discounted_total'] == 21.0
    mock_discount.assert_called_once_with(0.2, 10.0)
    mock_discount.return_value.apply_discount.assert_called_once_with(mock_cart)


# happy path - apply_promotions_to_cart - Test that promotions are applied correctly to the cart
def test_apply_promotions_success(client, mock_cart, mock_apply_promotions, mock_promotion):
    response = client.post('/apply_promotions', json={})
    assert response.status_code == 200
    assert response.json['message'] == 'Promotions applied'
    mock_apply_promotions.assert_called_once_with(mock_cart, mock_promotion.call_args_list)


# edge case - add_item - Test adding an item with zero quantity
def test_add_item_zero_quantity(client, mock_cart):
    response = client.post('/add_item', json={
        'item_id': 1,
        'quantity': 0,
        'price': 10.5,
        'name': 'Test Item',
        'category': 'Test Category'
    })
    assert response.status_code == 400
    assert response.json['message'] == 'Invalid quantity'
    mock_cart.add_item.assert_not_called()


# edge case - remove_item - Test removing an item not in the cart
def test_remove_item_not_in_cart(client, mock_cart):
    response = client.post('/remove_item', json={'item_id': 999})
    assert response.status_code == 404
    assert response.json['message'] == 'Item not found'
    mock_cart.remove_item.assert_called_once_with(999)


# edge case - update_item_quantity - Test updating the quantity of an item not in the cart
def test_update_item_quantity_not_in_cart(client, mock_cart):
    response = client.post('/update_item_quantity', json={'item_id': 999, 'new_quantity': 5})
    assert response.status_code == 404
    assert response.json['message'] == 'Item not found'
    mock_cart.update_item_quantity.assert_called_once_with(999, 5)


# edge case - apply_discount_to_cart - Test applying a discount with a rate greater than 1
def test_apply_discount_rate_greater_than_one(client, mock_cart, mock_discount):
    response = client.post('/apply_discount', json={'discount_rate': 1.5, 'min_purchase_amount': 10.0})
    assert response.status_code == 400
    assert response.json['message'] == 'Invalid discount rate'
    mock_discount.assert_not_called()


# edge case - apply_promotions_to_cart - Test applying promotions when cart is empty
def test_apply_promotions_empty_cart(client, mock_cart, mock_apply_promotions):
    mock_cart.total_price = 0.0
    response = client.post('/apply_promotions', json={})
    assert response.status_code == 400
    assert response.json['message'] == 'Cart is empty'
    mock_apply_promotions.assert_not_called()


