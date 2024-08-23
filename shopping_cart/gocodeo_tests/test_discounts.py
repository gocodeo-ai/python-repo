import pytest
from unittest.mock import MagicMock

@pytest.fixture
def cart():
    cart = MagicMock()
    cart.calculate_total_price = MagicMock()
    return cart

@pytest.fixture
def discount():
    return Discount

@pytest.fixture
def setup_mocks(cart):
    cart.calculate_total_price.return_value = 150
    cart.user_type = "regular"
    cart.items = [{"category": "clothing", "price": 100}]
    return cart

# happy_path - apply_discount - Test that discount is applied correctly when total price exceeds minimum purchase amount and user is not premium.
def test_apply_discount_regular_user(discount, setup_mocks):
    discount_instance = discount(0.1, 100)
    setup_mocks.calculate_total_price.return_value = 150
    setup_mocks.user_type = 'regular'
    setup_mocks.items = [{'category': 'clothing', 'price': 100}]
    result = discount_instance.apply_discount(setup_mocks)
    assert result == 165.0

# happy_path - apply_discount - Test that premium user with electronics gets 1.5 times discount rate applied when total price exceeds minimum purchase amount.
def test_apply_discount_premium_user_electronics(discount, setup_mocks):
    discount_instance = discount(0.1, 150)
    setup_mocks.calculate_total_price.return_value = 200
    setup_mocks.user_type = 'premium'
    setup_mocks.items = [{'category': 'electronics', 'price': 200}]
    result = discount_instance.apply_discount(setup_mocks)
    assert result == 230.0

# happy_path - apply_discount - Test that no discount is applied when total price is below minimum purchase amount.
def test_apply_discount_below_min_purchase(discount, setup_mocks):
    discount_instance = discount(0.1, 100)
    setup_mocks.calculate_total_price.return_value = 50
    setup_mocks.user_type = 'regular'
    setup_mocks.items = [{'category': 'clothing', 'price': 50}]
    result = discount_instance.apply_discount(setup_mocks)
    assert result == 50.0

# happy_path - apply_bulk_discount - Test that bulk discount is applied correctly on items meeting bulk quantity requirement.
def test_apply_bulk_discount(discount, setup_mocks):
    discount_instance = discount(0.1)
    setup_mocks.items = [{'category': 'clothing', 'price': 100, 'quantity': 10}]
    discount_instance.apply_bulk_discount(setup_mocks, 5, 0.2)
    assert setup_mocks.items[0]['price'] == 80.0

# happy_path - apply_seasonal_discount - Test that seasonal discount is applied correctly during holiday season.
def test_apply_seasonal_discount_holiday(discount, setup_mocks):
    discount_instance = discount(0.1)
    setup_mocks.calculate_total_price.return_value = 100
    setup_mocks.items = [{'category': 'clothing', 'price': 100}]
    result = discount_instance.apply_seasonal_discount(setup_mocks, 'holiday', 0.3)
    assert result == 70.0

# edge_case - apply_discount - Test that no discount is applied when discount rate is zero.
def test_apply_discount_zero_rate(discount, setup_mocks):
    discount_instance = discount(0.0, 100)
    setup_mocks.calculate_total_price.return_value = 150
    setup_mocks.user_type = 'regular'
    setup_mocks.items = [{'category': 'clothing', 'price': 100}]
    result = discount_instance.apply_discount(setup_mocks)
    assert result == 150.0

# edge_case - apply_bulk_discount - Test that bulk discount is not applied when item quantity is below bulk quantity requirement.
def test_apply_bulk_discount_below_bulk_quantity(discount, setup_mocks):
    discount_instance = discount(0.1)
    setup_mocks.items = [{'category': 'clothing', 'price': 100, 'quantity': 4}]
    discount_instance.apply_bulk_discount(setup_mocks, 5, 0.2)
    assert setup_mocks.items[0]['price'] == 100.0

# edge_case - apply_seasonal_discount - Test that seasonal discount is not applied during non-holiday season.
def test_apply_seasonal_discount_non_holiday(discount, setup_mocks):
    discount_instance = discount(0.1)
    setup_mocks.calculate_total_price.return_value = 100
    setup_mocks.items = [{'category': 'clothing', 'price': 100}]
    result = discount_instance.apply_seasonal_discount(setup_mocks, 'spring', 0.3)
    assert result == 100.0

# edge_case - apply_category_discount - Test that category discount is not applied when no items match the specified category.
def test_apply_category_discount_no_matching_category(discount, setup_mocks):
    discount_instance = discount(0.1)
    setup_mocks.items = [{'category': 'clothing', 'price': 100}]
    discount_instance.apply_category_discount(setup_mocks, 'electronics', 0.2)
    assert setup_mocks.items[0]['price'] == 100.0

# edge_case - apply_loyalty_discount - Test that loyalty discount is not applied when loyalty years are insufficient.
def test_apply_loyalty_discount_insufficient_years(discount, setup_mocks):
    discount_instance = discount(0.1)
    setup_mocks.calculate_total_price.return_value = 100
    setup_mocks.user_type = 'loyal'
    setup_mocks.items = [{'category': 'clothing', 'price': 100}]
    result = discount_instance.apply_loyalty_discount(setup_mocks, 1, 0.2)
    assert result == 100.0

