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
    return app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def cart_mock():
    with patch('shopping_cart.cart.Cart', autospec=True) as CartMock:
        cart_instance = CartMock.return_value
        cart_instance.add_item = MagicMock()
        cart_instance.remove_item = MagicMock()
        cart_instance.update_item_quantity = MagicMock()
        cart_instance.calculate_total_price = MagicMock(return_value=0.0)
        yield cart_instance

@pytest.fixture
def discount_mock():
    with patch('shopping_cart.discounts.Discount', autospec=True) as DiscountMock:
        discount_instance = DiscountMock.return_value
        discount_instance.apply_discount = Mock()
        yield discount_instance

@pytest.fixture
def promotion_mock():
    with patch('shopping_cart.payments.Promotion', autospec=True) as PromotionMock:
        promotion_instance = PromotionMock.return_value
        yield promotion_instance

@pytest.fixture
def apply_promotions_mock():
    with patch('shopping_cart.payments.apply_promotions', autospec=True) as apply_promotions_fn:
        apply_promotions_fn.return_value = None
        yield apply_promotions_fn

@pytest.fixture
def get_all_items_from_cart_mock():
    with patch('shopping_cart.utils.get_all_items_from_cart', autospec=True) as get_all_items_mock:
        get_all_items_mock.return_value = []
        yield get_all_items_mock
```

# happy_path - test_add_item_success - Test that item is added to cart with valid input data
def test_add_item_success(client, cart_mock):
    response = client.post('/add_item', json={
        'item_id': 1,
        'quantity': 2,
        'price': 10.99,
        'name': 'T-shirt',
        'category': 'Clothing'
    })
    assert response.status_code == 201
    assert response.json == {'message': 'Item added to cart'}
    cart_mock.add_item.assert_called_once_with(1, 2, 190.99, 'T-shirt', 'Clothing', 'regular')

# happy_path - test_update_item_quantity_success - Test that item quantity is updated successfully with valid data
def test_update_item_quantity_success(client, cart_mock):
    response = client.post('/update_item_quantity', json={
        'item_id': 1,
        'new_quantity': 3
    })
    assert response.status_code == 200
    assert response.json == {'message': 'Item quantity updated'}
    cart_mock.update_item_quantity.assert_called_once_with(1, 3)

# happy_path - test_get_cart_items_success - Test that all items are retrieved from the cart
def test_get_cart_items_success(client, get_all_items_from_cart_mock):
    get_all_items_from_cart_mock.return_value = [{
        'item_id': 1,
        'quantity': 2,
        'price': 19.99,
        'name': 'T-shirt',
        'category': 'Clothing'
    }]
    response = client.get('/get_cart_items')
    assert response.status_code == 200
    assert response.json == {'items': [{
        'item_id': 1,
        'quantity': 2,
        'price': 19.99,
        'name': 'T-shirt',
        'category': 'Clothing'
    }]}

# happy_path - test_apply_discount_to_cart_success - Test that discount is applied correctly to the cart
def test_apply_discount_to_cart_success(client, cart_mock, discount_mock):
    cart_mock.total_price = 39.98
    response = client.post('/apply_discount', json={
        'discount_rate': 0.1,
        'min_purchase_amount': 30.0
    })
    assert response.status_code == 200
    assert response.json == {'discounted_total': 39.98}
    discount_mock.apply_discount.assert_called_once_with(cart_mock)

# happy_path - test_apply_promotions_to_cart_success - Test that promotions are applied successfully to the cart
def test_apply_promotions_to_cart_success(client, cart_mock, apply_promotions_mock):
    response = client.post('/apply_promotions')
    assert response.status_code == 200
    assert response.json == {'message': 'Promotions applied'}
    apply_promotions_mock.assert_called_once_with(cart_mock, [
        Promotion("Spring Sale", 0.10),
        Promotion("Black Friday", 0.25)
    ])

# edge_case - test_remove_item_not_in_cart - Test that removing an item not in cart returns appropriate message
def test_remove_item_not_in_cart(client, cart_mock):
    cart_mock.remove_item.side_effect = Exception('Item not found in cart')
    response = client.post('/remove_item', json={'item_id': 99})
    assert response.status_code == 500
    assert 'Item not found in cart' in response.json['message']
    cart_mock.remove_item.assert_called_once_with(99)

# edge_case - test_update_item_quantity_to_zero - Test that updating item quantity to zero removes the item from cart
def test_update_item_quantity_to_zero(client, cart_mock):
    response = client.post('/update_item_quantity', json={
        'item_id': 1,
        'new_quantity': 0
    })
    assert response.status_code == 200
    assert response.json == {'message': 'Item removed from cart'}
    cart_mock.update_item_quantity.assert_called_once_with(1, 0)

# edge_case - test_get_cart_items_empty_cart - Test that retrieving items from an empty cart returns an empty list
def test_get_cart_items_empty_cart(client, get_all_items_from_cart_mock):
    get_all_items_from_cart_mock.return_value = []
    response = client.get('/get_cart_items')
    assert response.status_code == 200
    assert response.json == {'items': []}

# edge_case - test_calculate_total_price_empty_cart - Test that calculating total price for an empty cart returns zero
def test_calculate_total_price_empty_cart(client, cart_mock):
    cart_mock.calculate_total_price.return_value = 0.0
    response = client.get('/calculate_total_price')
    assert response.status_code == 200
    assert response.json == {'total_price': 0.0}
    cart_mock.calculate_total_price.assert_called_once()

# edge_case - test_apply_discount_high_min_purchase - Test that applying discount with higher min purchase amount does not apply discount
def test_apply_discount_high_min_purchase(client, cart_mock, discount_mock):
    cart_mock.total_price = 39.98
    response = client.post('/apply_discount', json={
        'discount_rate': 0.15,
        'min_purchase_amount': 100.0
    })
    assert response.status_code == 200
    assert response.json == {'discounted_total': 39.98}
    discount_mock.apply_discount.assert_not_called()

# edge_case - test_apply_promotions_no_applicable - Test that applying promotions with no applicable promotions returns original total
def test_apply_promotions_no_applicable(client, cart_mock, apply_promotions_mock):
    apply_promotions_mock.return_value = None
    response = client.post('/apply_promotions')
    assert response.status_code == 200
    assert response.json == {'message': 'No applicable promotions'}
    apply_promotions_mock.assert_called_once_with(cart_mock, [
        Promotion("Spring Sale", 0.10),
        Promotion("Black Friday", 0.25)
    ])

