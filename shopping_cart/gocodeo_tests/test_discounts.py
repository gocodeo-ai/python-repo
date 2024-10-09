import pytest
from unittest import mock
from shopping_cart.discounts import Discount

@pytest.fixture
def mock_cart():
    cart_mock = mock.Mock()
    cart_mock.calculate_total_price = mock.Mock(return_value=150)
    cart_mock.user_type = "regular"
    cart_mock.items = [{'category': 'clothing'}]
    return cart_mock

@pytest.fixture
def discount():
    return Discount(discount_rate=0.1, min_purchase_amount=100)

@pytest.fixture
def mock_cart_premium():
    cart_mock = mock.Mock()
    cart_mock.calculate_total_price = mock.Mock(return_value=200)
    cart_mock.user_type = "premium"
    cart_mock.items = [{'category': 'electronics'}]
    return cart_mock

@pytest.fixture
def mock_cart_bulk_discount():
    cart_mock = mock.Mock()
    cart_mock.items = [{'quantity': 10, 'price': 100}]
    return cart_mock

@pytest.fixture
def mock_cart_seasonal_discount():
    cart_mock = mock.Mock()
    cart_mock.calculate_total_price = mock.Mock(return_value=300)
    return cart_mock

@pytest.fixture
def mock_cart_category_discount():
    cart_mock = mock.Mock()
    cart_mock.items = [{'category': 'books', 'price': 50}]
    return cart_mock

@pytest.fixture
def mock_cart_loyalty_discount():
    cart_mock = mock.Mock()
    cart_mock.calculate_total_price = mock.Mock(return_value=500)
    cart_mock.user_type = "loyal"
    return cart_mock

@pytest.fixture
def mock_cart_flash_sale_discount():
    cart_mock = mock.Mock()
    cart_mock.items = [{'item_id': 101, 'price': 200}]
    return cart_mock

# happy path - apply_discount - Test that a discount is applied if the total price is above the minimum purchase amount.
def test_apply_discount_above_minimum(mock_cart, discount):
    discount.apply_discount(mock_cart)
    assert mock_cart.total_price == 165


# happy path - apply_discount - Test that a premium user gets extra discount for electronics category.
def test_apply_discount_premium_user_electronics(mock_cart_premium, discount):
    discount.apply_discount(mock_cart_premium)
    assert mock_cart_premium.total_price == 230


# happy path - apply_bulk_discount - Test that bulk discount is applied when item quantity is above bulk quantity.
def test_apply_bulk_discount_above_quantity(mock_cart_bulk_discount, discount):
    discount.apply_bulk_discount(mock_cart_bulk_discount, bulk_quantity=5, bulk_discount_rate=0.1)
    assert mock_cart_bulk_discount.items[0]['price'] == 90


# happy path - apply_seasonal_discount - Test that seasonal discount is applied during holiday season.
def test_apply_seasonal_discount_holiday(mock_cart_seasonal_discount, discount):
    discount.apply_seasonal_discount(mock_cart_seasonal_discount, season='holiday', seasonal_discount_rate=0.2)
    assert mock_cart_seasonal_discount.total_price == 240


# happy path - apply_category_discount - Test that category discount is applied for specific category items.
def test_apply_category_discount_specific_category(mock_cart_category_discount, discount):
    discount.apply_category_discount(mock_cart_category_discount, category='books', category_discount_rate=0.15)
    assert mock_cart_category_discount.items[0]['price'] == 42.5


# happy path - apply_loyalty_discount - Test that loyalty discount is applied for loyal users with more than 2 years.
def test_apply_loyalty_discount_loyal_user(mock_cart_loyalty_discount, discount):
    discount.apply_loyalty_discount(mock_cart_loyalty_discount, loyalty_years=3, loyalty_discount_rate=0.1)
    assert mock_cart_loyalty_discount.total_price == 450


# happy path - apply_flash_sale_discount - Test that flash sale discount is applied on items on sale.
def test_apply_flash_sale_discount_items_on_sale(mock_cart_flash_sale_discount, discount):
    discount.apply_flash_sale_discount(mock_cart_flash_sale_discount, flash_sale_rate=0.25, items_on_sale=[101])
    assert mock_cart_flash_sale_discount.items[0]['price'] == 150


# edge case - apply_discount - Test that no discount is applied if the total price is below the minimum purchase amount.
def test_apply_discount_below_minimum(mock_cart, discount):
    mock_cart.calculate_total_price.return_value = 50
    discount.apply_discount(mock_cart)
    assert mock_cart.total_price == 50


# edge case - apply_bulk_discount - Test that no bulk discount is applied if item quantity is below bulk quantity.
def test_apply_bulk_discount_below_quantity(mock_cart_bulk_discount, discount):
    mock_cart_bulk_discount.items[0]['quantity'] = 3
    discount.apply_bulk_discount(mock_cart_bulk_discount, bulk_quantity=5, bulk_discount_rate=0.1)
    assert mock_cart_bulk_discount.items[0]['price'] == 100


# edge case - apply_seasonal_discount - Test that no seasonal discount is applied for non-holiday season.
def test_apply_seasonal_discount_non_holiday(mock_cart_seasonal_discount, discount):
    discount.apply_seasonal_discount(mock_cart_seasonal_discount, season='spring', seasonal_discount_rate=0.2)
    assert mock_cart_seasonal_discount.total_price == 300


# edge case - apply_category_discount - Test that no category discount is applied for items not in the specified category.
def test_apply_category_discount_non_matching_category(mock_cart_category_discount, discount):
    discount.apply_category_discount(mock_cart_category_discount, category='electronics', category_discount_rate=0.15)
    assert mock_cart_category_discount.items[0]['price'] == 50


# edge case - apply_loyalty_discount - Test that no loyalty discount is applied for non-loyal users.
def test_apply_loyalty_discount_non_loyal_user(mock_cart_loyalty_discount, discount):
    mock_cart_loyalty_discount.user_type = 'regular'
    discount.apply_loyalty_discount(mock_cart_loyalty_discount, loyalty_years=1, loyalty_discount_rate=0.1)
    assert mock_cart_loyalty_discount.total_price == 500


# edge case - apply_flash_sale_discount - Test that no flash sale discount is applied on items not on sale.
def test_apply_flash_sale_discount_items_not_on_sale(mock_cart_flash_sale_discount, discount):
    discount.apply_flash_sale_discount(mock_cart_flash_sale_discount, flash_sale_rate=0.25, items_on_sale=[102])
    assert mock_cart_flash_sale_discount.items[0]['price'] == 200


