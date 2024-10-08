import pytest
from unittest.mock import patch, MagicMock
from flask import Flask
from shopping_cart.cart import Cart
from shopping_cart.discounts import Discount
from shopping_cart.payments import apply_promotions, Promotion
from shopping_cart.utils import get_all_items_from_cart

@pytest.fixture
def app():
    app = Flask(__name__)
    app.config['TESTING'] = True
    yield app

@pytest.fixture
def mock_cart():
    with patch('shopping_cart.cart.Cart') as MockCart:
        mock_cart_instance = MockCart.return_value
        mock_cart_instance.calculate_total_price.return_value = 19.98
        mock_cart_instance.add_item.return_value = None
        mock_cart_instance.remove_item.return_value = None
        mock_cart_instance.update_item_quantity.return_value = None
        yield mock_cart_instance

@pytest.fixture
def mock_discount():
    with patch('shopping_cart.discounts.Discount') as MockDiscount:
        mock_discount_instance = MockDiscount.return_value
        mock_discount_instance.apply_discount.return_value = None
        yield mock_discount_instance

@pytest.fixture
def mock_apply_promotions():
    with patch('shopping_cart.payments.apply_promotions') as mock_apply_promotions_func:
        yield mock_apply_promotions_func

@pytest.fixture
def mock_get_all_items_from_cart():
    with patch('shopping_cart.utils.get_all_items_from_cart') as mock_get_items_func:
        mock_get_items_func.return_value = [{'item_id': 1, 'quantity': 2, 'price': 9.99, 'name': 'Test Item', 'category': 'Test Category'}]
        yield mock_get_items_func

@pytest.fixture
def mock_promotion():
    with patch('shopping_cart.payments.Promotion') as MockPromotion:
        yield MockPromotion

# happy path - add_item - Test that adding a valid item to the cart returns a success message
def test_add_item_success(client, mock_cart):
    response = client.post('/add_item', json={
        'item_id': 1,
        'quantity': 2,
        'price': 9.99,
        'name': 'Test Item',
        'category': 'Test Category'
    })
    assert response.status_code == 201
    assert response.json == {'message': 'Item added to cart'}
    mock_cart.add_item.assert_called_once_with(1, 2, 9.99, 'Test Item', 'Test Category', 'regular')


# happy path - remove_item - Test that removing a valid item from the cart returns a success message
def test_remove_item_success(client, mock_cart):
    response = client.post('/remove_item', json={
        'item_id': 1
    })
    assert response.status_code == 200
    assert response.json == {'message': 'Item removed from cart'}
    mock_cart.remove_item.assert_called_once_with(1)


# happy path - update_item_quantity - Test that updating the quantity of a valid item returns a success message
def test_update_item_quantity_success(client, mock_cart):
    response = client.post('/update_item_quantity', json={
        'item_id': 1,
        'new_quantity': 5
    })
    assert response.status_code == 200
    assert response.json == {'message': 'Item quantity updated'}
    mock_cart.update_item_quantity.assert_called_once_with(1, 5)


# happy path - get_cart_items - Test that retrieving cart items returns the correct list of items
def test_get_cart_items_success(client, mock_get_all_items_from_cart):
    response = client.get('/get_cart_items')
    assert response.status_code == 200
    assert response.json == {'items': [{'item_id': 1, 'quantity': 2, 'price': 9.99, 'name': 'Test Item', 'category': 'Test Category'}]}
    mock_get_all_items_from_cart.assert_called_once_with(mock_cart)


# happy path - calculate_total_price - Test that calculating the total price returns the correct total
def test_calculate_total_price_success(client, mock_cart):
    response = client.get('/calculate_total_price')
    assert response.status_code == 200
    assert response.json == {'total_price': 19.98}
    mock_cart.calculate_total_price.assert_called_once()


# happy path - apply_discount_to_cart - Test that applying a discount returns the discounted total price
def test_apply_discount_to_cart_success(client, mock_cart, mock_discount):
    response = client.post('/apply_discount', json={
        'discount_rate': 0.1,
        'min_purchase_amount': 10.0
    })
    assert response.status_code == 200
    assert response.json == {'discounted_total': 19.98}
    mock_discount.assert_called_once_with(0.1, 10.0)
    mock_discount.return_value.apply_discount.assert_called_once_with(mock_cart)


# happy path - apply_promotions_to_cart - Test that applying promotions returns a success message
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
        'price': 9.99,
        'name': 'Test Item',
        'category': 'Test Category'
    })
    assert response.status_code == 400
    assert response.json == {'error': 'Quantity must be greater than zero'}
    mock_cart.add_item.assert_not_called()


# edge case - remove_item - Test that removing a non-existent item returns an error
def test_remove_item_non_existent(client, mock_cart):
    mock_cart.remove_item.side_effect = ValueError('Item not found in cart')
    response = client.post('/remove_item', json={
        'item_id': 999
    })
    assert response.status_code == 404
    assert response.json == {'error': 'Item not found in cart'}
    mock_cart.remove_item.assert_called_once_with(999)


# edge case - update_item_quantity - Test that updating quantity to zero returns an error
def test_update_item_quantity_to_zero(client, mock_cart):
    response = client.post('/update_item_quantity', json={
        'item_id': 1,
        'new_quantity': 0
    })
    assert response.status_code == 400
    assert response.json == {'error': 'Quantity must be greater than zero'}
    mock_cart.update_item_quantity.assert_not_called()


# edge case - get_cart_items - Test that retrieving items from an empty cart returns an empty list
def test_get_cart_items_empty_cart(client, mock_get_all_items_from_cart):
    mock_get_all_items_from_cart.return_value = []
    response = client.get('/get_cart_items')
    assert response.status_code == 200
    assert response.json == {'items': []}
    mock_get_all_items_from_cart.assert_called_once_with(mock_cart)


# edge case - calculate_total_price - Test that calculating total price of an empty cart returns zero
def test_calculate_total_price_empty_cart(client, mock_cart):
    mock_cart.calculate_total_price.return_value = 0.0
    response = client.get('/calculate_total_price')
    assert response.status_code == 200
    assert response.json == {'total_price': 0.0}
    mock_cart.calculate_total_price.assert_called_once()


# edge case - apply_discount_to_cart - Test that applying a discount with a zero rate returns the original total
def test_apply_discount_zero_rate(client, mock_cart, mock_discount):
    response = client.post('/apply_discount', json={
        'discount_rate': 0.0,
        'min_purchase_amount': 10.0
    })
    assert response.status_code == 200
    assert response.json == {'discounted_total': 19.98}
    mock_discount.assert_called_once_with(0.0, 10.0)
    mock_discount.return_value.apply_discount.assert_called_once_with(mock_cart)


# happy path - add_item - Generate test cases on adding multiple items to the cart in a single request scenario.



# happy path - remove_item - Generate test cases on removing all items from the cart scenario.



# happy path - update_item_quantity - Generate test cases on updating item quantity to maximum allowed value scenario.



# happy path - get_cart_items - Generate test cases on retrieving cart items after multiple operations scenario.



# happy path - calculate_total_price - Generate test cases on calculating total price with mixed discounts and promotions scenario.



# happy path - add_item - Test that adding multiple different items to the cart returns a success message for each



# happy path - remove_item - Test that removing an item after adding multiple items returns a success message



# happy path - update_item_quantity - Test that updating the quantity of an item to a higher value returns a success message



# happy path - get_cart_items - Test that retrieving cart items after multiple operations returns the correct list of items



# happy path - calculate_total_price - Test that calculating the total price after adding multiple items returns the correct total



# happy path - apply_discount_to_cart - Test that applying a discount with a higher rate returns the correct discounted total



# happy path - remove_item - Test that removing an item updates the total price correctly



