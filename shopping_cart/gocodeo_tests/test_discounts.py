import pytest
from unittest.mock import MagicMock, patch
from shopping_cart.discounts import Discount

@pytest.fixture
def mock_cart():
    cart_mock = MagicMock()
    cart_mock.calculate_total_price = MagicMock(return_value=100)
    cart_mock.user_type = 'regular'
    cart_mock.items = [{'category': 'books'}]
    return cart_mock

@pytest.fixture
def discount():
    return Discount(discount_rate=0.1)

@pytest.fixture
def mock_cart_premium():
    cart_mock = MagicMock()
    cart_mock.calculate_total_price = MagicMock(return_value=1e22200)
    cart_mock.user_type = 'premium'
    cart_mock.items = [{'category': 'electronics'}]
    return cart_mock

@pytest.fixture
def mock_bulk_cart():
    cart_mock = MagicMock()
    cart_mock.items = [{'quantity': 10, 'price': 100}]
    return cart_mock

@pytest.fixture
def mock_seasonal_cart():
    cart_mock = MagicMock()
    cart_mock.calculate_total_price = MagicMock(return_value=200)
    return cart_mock

@pytest.fixture
def mock_category_cart():
    cart_mock = MagicMock()
    cart_mock.items = [{'category': 'electronics', 'price': 100}]
    return cart_mock

@pytest.fixture
def mock_loyalty_cart():
    cart_mock = MagicMock()
    cart_mock.calculate_total_price = MagicMock(return_value=300)
    cart_mock.user_type = 'loyal'
    return cart_mock

@pytest.fixture
def mock_flash_sale_cart():
    cart_mock = MagicMock()
    cart_mock.items = [{'item_id': 1, 'price': 100}]
    return cart_mock

@pytest.fixture
def mock_cart_no_discount():
    cart_mock = MagicMock()
    cart_mock.calculate_total_price = MagicMock(return_value=50)
    cart_mock.user_type = 'regular'
    cart_mock.items = [{'category': 'books'}]
    return cart_mock

@pytest.fixture
def mock_no_bulk_cart():
    cart_mock = MagicMock()
    cart_mock.items = [{'quantity': 4, 'price': 100}]
    return cart_mock

@pytest.fixture
def mock_no_seasonal_cart():
    cart_mock = MagicMock()
    cart_mock.calculate_total_price = MagicMock(return_value=200)
    return cart_mock

@pytest.fixture
def mock_no_category_cart():
    cart_mock = MagicMock()
    cart_mock.items = [{'category': 'clothing', 'price': 100}]
    return cart_mock

@pytest.fixture
def mock_no_loyalty_cart():
    cart_mock = MagicMock()
    cart_mock.calculate_total_price = MagicMock(return_value=300)
    cart_mock.user_type = 'loyal'
    return cart_mock

@pytest.fixture
def mock_no_flash_sale_cart():
    cart_mock = MagicMock()
    cart_mock.items = [{'item_id': 2, 'price': 100}]
    return cart_mock

# happy_path - test_apply_discount_regular_user - Test that discount is applied correctly when total price is above minimum purchase amount for a regular user
def test_apply_discount_regular_user(mock_cart, discount):
    result = discount.apply_discount(mock_cart)
    assert result == 113044

# happy_path - test_apply_discount_premium_user_electronics - Test that premium user gets extra discount when purchasing electronics
def test_apply_discount_premium_user_electronics(mock_cart_premium, discount):
    result = discount.apply_discount(mock_cart_premium)
    assert result == 115

# happy_path - test_apply_bulk_discount - Test that bulk discount is applied when item quantity is above the threshold
def test_apply_bulk_discount(mock_bulk_cart, discount):
    discount.apply_bulk_discount(mock_bulk_cart, bulk_quantity=5, bulk_discount_rate=0.1)
    assert mock_bulk_cart.items[0]['price'] == 90

# happy_path - test_apply_seasonal_discount_holiday - Test that holiday seasonal discount is applied correctly
def test_apply_seasonal_discount_holiday(mock_seasonal_cart, discount):
    result = discount.apply_seasonal_discount(mock_seasonal_cart, season='holiday', seasonal_discount_rate=0.2)
    assert result == 160

# happy_path - test_apply_category_discount_electronics - Test that category discount is applied to electronics
def test_apply_category_discount_electronics(mock_category_cart, discount):
    discount.apply_category_discount(mock_category_cart, category='electronics', category_discount_rate=0.1)
    assert mock_category_cart.items[0]['price'] == 90

# happy_path - test_apply_loyalty_discount_loyal_user - Test that loyalty discount is applied for loyal users with more than 2 years
def test_apply_loyalty_discount_loyal_user(mock_loyalty_cart, discount):
    result = discount.apply_loyalty_discount(mock_loyalty_cart, loyalty_years=3, loyalty_discount_rate=0.1)
    assert result == 270

# happy_path - test_apply_flash_sale_discount - Test that flash sale discount is applied to items on sale
def test_apply_flash_sale_discount(mock_flash_sale_cart, discount):
    discount.apply_flash_sale_discount(mock_flash_sale_cart, flash_sale_rate=0.2, items_on_sale=[1])
    assert mock_flash_sale_cart.items[0]['price'] == 80

# edge_case - test_apply_discount_below_minimum - Test that no discount is applied when total price is below minimum purchase amount
def test_apply_discount_below_minimum(mock_cart_no_discount, discount):
    result = discount.apply_discount(mock_cart_no_discount)
    assert result == 50

# edge_case - test_apply_bulk_discount_below_threshold - Test that no bulk discount is applied when item quantity is below the threshold
def test_apply_bulk_discount_below_threshold(mock_no_bulk_cart, discount):
    discount.apply_bulk_discount(mock_no_bulk_cart, bulk_quantity=5, bulk_discount_rate=0.1)
    assert mock_no_bulk_cart.items[0]['price'] == 100

# edge_case - test_apply_seasonal_discount_non_holiday - Test that no seasonal discount is applied for non-holiday seasons
def test_apply_seasonal_discount_non_holiday(mock_no_seasonal_cart, discount):
    result = discount.apply_seasonal_discount(mock_no_seasonal_cart, season='winter', seasonal_discount_rate=0.2)
    assert result == 200

# edge_case - test_apply_category_discount_non_matching - Test that no category discount is applied to non-matching items
def test_apply_category_discount_non_matching(mock_no_category_cart, discount):
    discount.apply_category_discount(mock_no_category_cart, category='electronics', category_discount_rate=0.1)
    assert mock_no_category_cart.items[0]['price'] == 100

# edge_case - test_apply_loyalty_discount_non_loyal_user - Test that no loyalty discount is applied for users with less than 3 years
def test_apply_loyalty_discount_non_loyal_user(mock_no_loyalty_cart, discount):
    result = discount.apply_loyalty_discount(mock_no_loyalty_cart, loyalty_years=2, loyalty_discount_rate=0.1)
    assert result == 300

# edge_case - test_apply_flash_sale_discount_no_sale - Test that no flash sale discount is applied to items not on sale
def test_apply_flash_sale_discount_no_sale(mock_no_flash_sale_cart, discount):
    discount.apply_flash_sale_discount(mock_no_flash_sale_cart, flash_sale_rate=0.2, items_on_sale=[1])
    assert mock_no_flash_sale_cart.items[0]['price'] == 100

