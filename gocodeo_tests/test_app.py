import pytest
from unittest.mock import patch, MagicMock
from shopping_cart.cart import Cart
from shopping_cart.discounts import Discount
from shopping_cart.payments import apply_promotions, Promotion
from shopping_cart.utils import get_all_items_from_cart
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.fixture
def mock_cart():
    with patch('app.Cart') as MockCart:
        instance = MockCart.return_value
        instance.calculate_total_price.return_value = 52.5
        instance.total_price = 52.5
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
    with patch('app.get_all_items_from_cart') as mock_get_items:
        mock_get_items.return_value = [{'item_id': 1, 'quantity': 5, 'price': 10.5, 'name': 'Widget', 'category': 'Gadgets'}]
        yield mock_get_items

@pytest.fixture
def mock_promotion():
    with patch('app.Promotion') as MockPromotion:
        yield MockPromotion

@pytest.fixture(autouse=True)
def setup_mocks(mock_cart, mock_discount, mock_apply_promotions, mock_get_all_items_from_cart, mock_promotion):
    pass

# happy path - add_item - Test that adding an item to the cart returns a success message
def test_add_item_success(client, mock_cart):
    response = client.post('/add_item', json={
        'item_id': 1,
        'quantity': 2,
        'price': 10.5,
        'name': 'Widget',
        'category': 'Gadgets'
    })
    assert response.status_code == 201
    assert response.json == {'message': 'Item added to cart'}


# happy path - remove_item - Test that removing an item from the cart returns a success message
def test_remove_item_success(client, mock_cart):
    response = client.post('/remove_item', json={'item_id': 1})
    assert response.status_code == 200
    assert response.json == {'message': 'Item removed from cart'}


# happy path - update_item_quantity - Test that updating item quantity returns a success message
def test_update_item_quantity_success(client, mock_cart):
    response = client.post('/update_item_quantity', json={
        'item_id': 1,
        'new_quantity': 5
    })
    assert response.status_code == 200
    assert response.json == {'message': 'Item quantity updated'}


# happy path - get_cart_items - Test that retrieving cart items returns the correct list
def test_get_cart_items_success(client, mock_get_all_items_from_cart):
    response = client.get('/get_cart_items')
    assert response.status_code == 200
    assert response.json == {'items': [{'item_id': 1, 'quantity': 5, 'price': 10.5, 'name': 'Widget', 'category': 'Gadgets'}]}


# happy path - calculate_total_price - Test that calculating total price returns the correct total
def test_calculate_total_price_success(client, mock_cart):
    response = client.get('/calculate_total_price')
    assert response.status_code == 200
    assert response.json == {'total_price': 52.5}


# happy path - apply_discount_to_cart - Test that applying discount returns the correct discounted total
def test_apply_discount_success(client, mock_discount, mock_cart):
    response = client.post('/apply_discount', json={
        'discount_rate': 0.1,
        'min_purchase_amount': 0
    })
    assert response.status_code == 200
    assert response.json == {'discounted_total': 47.25}


# happy path - apply_promotions_to_cart - Test that applying promotions returns a success message
def test_apply_promotions_success(client, mock_apply_promotions):
    response = client.post('/apply_promotions')
    assert response.status_code == 200
    assert response.json == {'message': 'Promotions applied'}


# edge case - add_item - Test adding an item with zero quantity
def test_add_item_zero_quantity(client, mock_cart):
    response = client.post('/add_item', json={
        'item_id': 1,
        'quantity': 0,
        'price': 10.5,
        'name': 'Widget',
        'category': 'Gadgets'
    })
    assert response.status_code == 201
    assert response.json == {'message': 'Item added to cart'}


# edge case - remove_item - Test removing an item not in the cart
def test_remove_nonexistent_item(client, mock_cart):
    response = client.post('/remove_item', json={'item_id': 999})
    assert response.status_code == 200
    assert response.json == {'message': 'Item removed from cart'}


# edge case - update_item_quantity - Test updating item quantity to zero
def test_update_item_quantity_to_zero(client, mock_cart):
    response = client.post('/update_item_quantity', json={
        'item_id': 1,
        'new_quantity': 0
    })
    assert response.status_code == 200
    assert response.json == {'message': 'Item quantity updated'}


# edge case - get_cart_items - Test retrieving cart items when cart is empty
def test_get_cart_items_empty(client, mock_get_all_items_from_cart):
    mock_get_all_items_from_cart.return_value = []
    response = client.get('/get_cart_items')
    assert response.status_code == 200
    assert response.json == {'items': []}


# edge case - calculate_total_price - Test calculating total price with no items in the cart
def test_calculate_total_price_empty_cart(client, mock_cart):
    mock_cart.calculate_total_price.return_value = 0.0
    response = client.get('/calculate_total_price')
    assert response.status_code == 200
    assert response.json == {'total_price': 0.0}


# edge case - apply_discount_to_cart - Test applying discount with a rate greater than 1
def test_apply_discount_rate_greater_than_one(client, mock_discount, mock_cart):
    response = client.post('/apply_discount', json={
        'discount_rate': 1.5,
        'min_purchase_amount': 0
    })
    assert response.status_code == 200
    assert response.json == {'discounted_total': 0.0}


# edge case - apply_promotions_to_cart - Test applying promotions with no active promotions
def test_apply_promotions_no_active(client, mock_apply_promotions):
    mock_apply_promotions.return_value = None
    response = client.post('/apply_promotions')
    assert response.status_code == 200
    assert response.json == {'message': 'Promotions applied'}


