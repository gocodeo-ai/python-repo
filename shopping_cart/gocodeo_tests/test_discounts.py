import pytest
from unittest.mock import Mock

@pytest.fixture
def mock_cart():
    cart = Mock()
    cart.calculate_total_price = Mock()
    return cart

@pytest.fixture
def discount():
    return Discount(discount_rate=0.1)

@pytest.fixture
def setup_discount_tests(mock_cart):
    # Mocking cart's attributes
    mock_cart.user_type = 'regular'
    mock_cart.items = [{'category': 'clothing', 'price': 50}]
    mock_cart.total_price = 50

    return mock_cart

@pytest.fixture
def setup_bulk_discount_tests(mock_cart):
    mock_cart.items = [{'quantity': 10, 'price': 20}]
    return mock_cart

@pytest.fixture
def setup_seasonal_discount_tests(mock_cart):
    mock_cart.items = [{'price': 100}]
    mock_cart.total_price = 100
    return mock_cart

@pytest.fixture
def setup_loyalty_discount_tests(mock_cart):
    mock_cart.user_type = 'loyal'
    mock_cart.items = [{'price': 100}]
    mock_cart.total_price = 100
    return mock_cart

@pytest.fixture
def setup_flash_sale_discount_tests(mock_cart):
    mock_cart.items = [{'item_id': 1, 'price': 50}, {'item_id': 2, 'price': 100}]
    return mock_cart

# happy_path - test_apply_discount_premium_with_electronics - Test that discount is applied correctly for premium users with electronics
def test_apply_discount_premium_with_electronics(mock_cart, discount):
    mock_cart.user_type = 'premium'
    mock_cart.items = [{'category': 'electronics', 'price': 100}]
    mock_cart.calculate_total_price.return_value = 100
    expected_total_price = 250.0
    assert discount.apply_discount(mock_cart) == expected_total_price

# happy_path - test_apply_discount_non_premium - Test that discount is applied correctly for non-premium users
def test_apply_discount_non_premium(mock_cart, discount):
    mock_cart.user_type = 'regular'
    mock_cart.items = [{'category': 'clothing', 'price': 100}]
    mock_cart.calculate_total_price.return_value = 100
    expected_total_price = 110.0
    assert discount.apply_discount(mock_cart) == expected_total_price

# happy_path - test_apply_bulk_discount - Test that bulk discount is applied to items meeting quantity threshold
def test_apply_bulk_discount(setup_bulk_discount_tests, discount):
    bulk_quantity = 5
    bulk_discount_rate = 0.1
    discount.apply_bulk_discount(setup_bulk_discount_tests, bulk_quantity, bulk_discount_rate)
    expected_price = 18.0
    assert setup_bulk_discount_tests.items[0]['price'] == expected_price

# happy_path - test_apply_seasonal_discount_holiday - Test that seasonal discount is applied during holiday season
def test_apply_seasonal_discount_holiday(setup_seasonal_discount_tests, discount):
    season = 'holiday'
    seasonal_discount_rate = 0.2
    expected_total_price = 80.0
    assert discount.apply_seasonal_discount(setup_seasonal_discount_tests, season, seasonal_discount_rate) == expected_total_price

# happy_path - test_apply_loyalty_discount_loyal_user - Test that loyalty discount is applied for loyal users over 2 years
def test_apply_loyalty_discount_loyal_user(setup_loyalty_discount_tests, discount):
    loyalty_years = 3
    loyalty_discount_rate = 0.15
    expected_total_price = 85.0
    assert discount.apply_loyalty_discount(setup_loyalty_discount_tests, loyalty_years, loyalty_discount_rate) == expected_total_price

# edge_case - test_apply_discount_below_min_purchase - Test that discount is not applied when total is below minimum purchase amount
def test_apply_discount_below_min_purchase(setup_discount_tests, discount):
    setup_discount_tests.calculate_total_price.return_value = 50
    expected_total_price = 50.0
    assert discount.apply_discount(setup_discount_tests) == expected_total_price

# edge_case - test_apply_bulk_discount_below_threshold - Test that bulk discount is not applied when quantity is below threshold
def test_apply_bulk_discount_below_threshold(mock_cart, discount):
    mock_cart.items = [{'quantity': 4, 'price': 20}]
    bulk_quantity = 5
    bulk_discount_rate = 0.1
    discount.apply_bulk_discount(mock_cart, bulk_quantity, bulk_discount_rate)
    expected_price = 20.0
    assert mock_cart.items[0]['price'] == expected_price

# edge_case - test_apply_seasonal_discount_non_holiday - Test that no seasonal discount is applied during non-holiday season
def test_apply_seasonal_discount_non_holiday(setup_seasonal_discount_tests, discount):
    season = 'spring'
    seasonal_discount_rate = 0.2
    expected_total_price = 100.0
    assert discount.apply_seasonal_discount(setup_seasonal_discount_tests, season, seasonal_discount_rate) == expected_total_price

# edge_case - test_apply_loyalty_discount_non_loyal_user - Test that no loyalty discount is applied for users with less than 3 years
def test_apply_loyalty_discount_non_loyal_user(setup_loyalty_discount_tests, discount):
    loyalty_years = 2
    loyalty_discount_rate = 0.15
    expected_total_price = 100.0
    assert discount.apply_loyalty_discount(setup_loyalty_discount_tests, loyalty_years, loyalty_discount_rate) == expected_total_price

# edge_case - test_apply_flash_sale_discount - Test that flash sale discount is applied only to items on sale
def test_apply_flash_sale_discount(setup_flash_sale_discount_tests, discount):
    flash_sale_rate = 0.2
    items_on_sale = [1]
    discount.apply_flash_sale_discount(setup_flash_sale_discount_tests, flash_sale_rate, items_on_sale)
    expected_prices = [40.0, 100.0]
    assert [item['price'] for item in setup_flash_sale_discount_tests.items] == expected_prices

