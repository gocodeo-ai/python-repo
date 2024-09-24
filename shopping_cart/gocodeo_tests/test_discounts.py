import pytest
from unittest import mock
from shopping_cart.discounts import Discount

@pytest.fixture
def mock_cart():
    cart_mock = mock.Mock()
    cart_mock.calculate_total_price.return_value = 100
    cart_mock.user_type = 'regular'
    cart_mock.items = [{'category': 'clothing', 'price': 100}]
    cart_mock.total_price = 100
    return cart_mock

@pytest.fixture
def discount():
    return Discount(discount_rate=0.1, min_purchase_amount=50)

@pytest.fixture
def mock_cart_premium():
    cart_mock = mock.Mock()
    cart_mock.calculate_total_price.return_value = 100
    cart_mock.user_type = 'premium'
    cart_mock.items = [{'category': 'electronics', 'price': 100}]
    cart_mock.total_price = 100
    return cart_mock

@pytest.fixture
def mock_cart_loyal():
    cart_mock = mock.Mock()
    cart_mock.calculate_total_price.return_value = 100
    cart_mock.user_type = 'loyal'
    cart_mock.total_price = 100
    return cart_mock

@pytest.fixture
def mock_cart_bulk():
    cart_mock = mock.Mock()
    cart_mock.items = [{'quantity': 10, 'price': 100}]
    return cart_mock

@pytest.fixture
def mock_cart_seasonal():
    cart_mock = mock.Mock()
    cart_mock.calculate_total_price.return_value = 100
    return cart_mock

@pytest.fixture
def mock_cart_category():
    cart_mock = mock.Mock()
    cart_mock.items = [{'category': 'electronics', 'price': 100}]
    return cart_mock

@pytest.fixture
def mock_cart_flash_sale():
    cart_mock = mock.Mock()
    cart_mock.items = [{'item_id': 1, 'price': 100}]
    return cart_mock

# happy_path - test_apply_discount_premium_electronics - Test that discount is applied correctly for premium users with electronics
def test_apply_discount_premium_electronics(mock_cart_premium, discount):
    discount.apply_discount(mock_cart_premium)
    assert mock_cart_premium.total_price == 115

# happy_path - test_apply_discount_regular_user - Test that discount is applied correctly for regular users
def test_apply_discount_regular_user(mock_cart, discount):
    discount.apply_discount(mock_cart)
    assert mock_cart.total_price == 110

# happy_path - test_apply_bulk_discount - Test that bulk discount is applied when quantity is sufficient
def test_apply_bulk_discount(mock_cart_bulk, discount):
    discount.apply_bulk_discount(mock_cart_bulk, bulk_quantity=5, bulk_discount_rate=0.2)
    assert mock_cart_bulk.items[0]['price'] == 80

# happy_path - test_apply_seasonal_discount_holiday - Test that seasonal discount is applied during holiday season
def test_apply_seasonal_discount_holiday(mock_cart_seasonal, discount):
    discount.apply_seasonal_discount(mock_cart_seasonal, season='holiday', seasonal_discount_rate=0.2)
    assert mock_cart_seasonal.total_price == 80

# happy_path - test_apply_category_discount_electronics - Test that category discount is applied to electronics
def test_apply_category_discount_electronics(mock_cart_category, discount):
    discount.apply_category_discount(mock_cart_category, category='electronics', category_discount_rate=0.1)
    assert mock_cart_category.items[0]['price'] == 90

# happy_path - test_apply_loyalty_discount_loyal_user - Test that loyalty discount is applied for loyal users with more than 2 years
def test_apply_loyalty_discount_loyal_user(mock_cart_loyal, discount):
    discount.apply_loyalty_discount(mock_cart_loyal, loyalty_years=3, loyalty_discount_rate=0.1)
    assert mock_cart_loyal.total_price == 90

# happy_path - test_apply_flash_sale_discount - Test that flash sale discount is applied to items on sale
def test_apply_flash_sale_discount(mock_cart_flash_sale, discount):
    discount.apply_flash_sale_discount(mock_cart_flash_sale, flash_sale_rate=0.3, items_on_sale=[1])
    assert mock_cart_flash_sale.items[0]['price'] == 70

# edge_case - test_apply_discount_below_min_purchase - Test that no discount is applied if total price is below minimum purchase amount
def test_apply_discount_below_min_purchase(mock_cart, discount):
    mock_cart.calculate_total_price.return_value = 40
    discount.apply_discount(mock_cart)
    assert mock_cart.total_price == 40

# edge_case - test_apply_bulk_discount_insufficient_quantity - Test that no bulk discount is applied when quantity is insufficient
def test_apply_bulk_discount_insufficient_quantity(mock_cart_bulk, discount):
    mock_cart_bulk.items[0]['quantity'] = 3
    discount.apply_bulk_discount(mock_cart_bulk, bulk_quantity=5, bulk_discount_rate=0.2)
    assert mock_cart_bulk.items[0]['price'] == 100

# edge_case - test_apply_seasonal_discount_non_season - Test that no seasonal discount is applied outside of specified seasons
def test_apply_seasonal_discount_non_season(mock_cart_seasonal, discount):
    discount.apply_seasonal_discount(mock_cart_seasonal, season='winter', seasonal_discount_rate=0.2)
    assert mock_cart_seasonal.total_price == 100

# edge_case - test_apply_category_discount_non_matching - Test that no category discount is applied to non-matching categories
def test_apply_category_discount_non_matching(mock_cart_category, discount):
    mock_cart_category.items[0]['category'] = 'furniture'
    discount.apply_category_discount(mock_cart_category, category='electronics', category_discount_rate=0.1)
    assert mock_cart_category.items[0]['price'] == 100

# edge_case - test_apply_loyalty_discount_non_loyal_user - Test that no loyalty discount is applied for users with less than 2 years
def test_apply_loyalty_discount_non_loyal_user(mock_cart_loyal, discount):
    discount.apply_loyalty_discount(mock_cart_loyal, loyalty_years=1, loyalty_discount_rate=0.1)
    assert mock_cart_loyal.total_price == 100

# edge_case - test_apply_flash_sale_discount_non_sale_items - Test that no flash sale discount is applied to items not on sale
def test_apply_flash_sale_discount_non_sale_items(mock_cart_flash_sale, discount):
    mock_cart_flash_sale.items[0]['item_id'] = 2
    discount.apply_flash_sale_discount(mock_cart_flash_sale, flash_sale_rate=0.3, items_on_sale=[1])
    assert mock_cart_flash_sale.items[0]['price'] == 100

