import pytest
from unittest.mock import Mock

@pytest.fixture
def mock_cart():
    cart = Mock()
    cart.calculate_total_price = Mock(return_value=200)
    cart.user_type = "regular"
    cart.items = [
        {"item_id": 1, "category": "electronics", "quantity": 1, "price": 100},
        {"item_id": 2, "category": "clothing", "quantity": 2, "price": 50}
    ]
    cart.total_price = 0
    return cart

@pytest.fixture
def discount():
    return Discount(discount_rate=0.1, min_purchase_amount=100)# happy_path - apply_discount - Apply discount for a regular user with total price above minimum purchase amount
def test_apply_discount_regular_user_above_minimum(discount, mock_cart):
    mock_cart.user_type = 'regular'
    assert discount.apply_discount(mock_cart) == 220.0


# edge_case - apply_discount - Apply discount for a user with total price below minimum purchase amount
def test_apply_discount_below_minimum(discount, mock_cart):
    mock_cart.calculate_total_price = Mock(return_value=50)
    assert discount.apply_discount(mock_cart) == 50.0


# edge_case - apply_bulk_discount - Apply bulk discount for items in the cart
def test_apply_bulk_discount(discount, mock_cart):
    discount.apply_bulk_discount(mock_cart, bulk_quantity=1, bulk_discount_rate=0.2)
    assert mock_cart.items[0]['price'] == 80.0


# edge_case - apply_seasonal_discount - Apply seasonal discount for holiday season
def test_apply_seasonal_discount_holiday(discount, mock_cart):
    assert discount.apply_seasonal_discount(mock_cart, 'holiday', 0.1) == 180.0


# edge_case - apply_loyalty_discount - Apply loyalty discount for loyal user with more than 2 years
def test_apply_loyalty_discount(discount, mock_cart):
    mock_cart.user_type = 'loyal'
    assert discount.apply_loyalty_discount(mock_cart, loyalty_years=3, loyalty_discount_rate=0.1) == 180.0


