import pytest
from unittest.mock import MagicMock, patch
from shopping_cart.discounts import Discount

@pytest.fixture
def mock_cart():
    cart = MagicMock()
    cart.calculate_total_price = MagicMock(return_value=150)
    cart.user_type = 'regular'
    cart.items = [{'category': 'clothing'}]
    return cart

@pytest.fixture
def mock_cart_premium():
    cart = MagicMock()
    cart.calculate_total_price = MagicMock(return_value=200)
    cart.user_type = 'premium'
    cart.items = [{'category': 'electronics'}]
    return cart

@pytest.fixture
def mock_cart_bulk_discount():
    cart = MagicMock()
    cart.items = [{'quantity': 10, 'price': 100}]
    return cart

@pytest.fixture
def mock_cart_seasonal_discount():
    cart = MagicMock()
    cart.calculate_total_price = MagicMock(return_value=300)
    return cart

@pytest.fixture
def mock_cart_category_discount():
    cart = MagicMock()
    cart.items = [{'category': 'books', 'price': 50}, {'category': 'electronics', 'price': 200}]
    return cart

@pytest.fixture
def mock_cart_loyalty_discount():
    cart = MagicMock()
    cart.calculate_total_price = MagicMock(return_value=400)
    cart.user_type = 'loyal'
    return cart

@pytest.fixture
def mock_cart_flash_sale_discount():
    cart = MagicMock()
    cart.items = [{'item_id': 1, 'price': 100}, {'item_id': 2, 'price': 200}]
    return cart

@pytest.fixture
def discount():
    return Discount(discount_rate=0.1, min_purchase_amount=100)

@pytest.fixture
def discount_with_bulk():
    return Discount(discount_rate=0.2)

@pytest.fixture
def discount_with_seasonal():
    return Discount(discount_rate=0.2)

@pytest.fixture
def discount_with_category():
    return Discount(discount_rate=0.1)

@pytest.fixture
def discount_with_loyalty():
    return Discount(discount_rate=0.15)

@pytest.fixture
def discount_with_flash_sale():
    return Discount(discount_rate=0.25)

# happy_path - test_apply_discount_regular_user - Test that discount is applied correctly when total price is above minimum purchase amount and user is not premium.
def test_apply_discount_regular_user(discount, mock_cart):
    expected_price = 150 * (1 + 0.1)
    assert discount.apply_discount(mock_cart) == expected_price

# happy_path - test_apply_discount_premium_user_electronics - Test that premium user gets extra discount on electronics when total price is above minimum purchase amount.
def test_apply_discount_premium_user_electronics(discount, mock_cart_premium):
    expected_price = 200 + (0.1 * 1.5)
    assert discount.apply_discount(mock_cart_premium) == expected_price

# happy_path - test_apply_bulk_discount - Test that bulk discount is applied when item quantity is above threshold.
def test_apply_bulk_discount(discount_with_bulk, mock_cart_bulk_discount):
    discount_with_bulk.apply_bulk_discount(mock_cart_bulk_discount, bulk_quantity=5, bulk_discount_rate=0.2)
    assert mock_cart_bulk_discount.items[0]['price'] == 80

# happy_path - test_apply_seasonal_discount_holiday - Test that seasonal discount is applied during holiday season.
def test_apply_seasonal_discount_holiday(discount_with_seasonal, mock_cart_seasonal_discount):
    expected_price = 300 * (1 - 0.2)
    assert discount_with_seasonal.apply_seasonal_discount(mock_cart_seasonal_discount, season='holiday', seasonal_discount_rate=0.2) == expected_price

# happy_path - test_apply_category_discount - Test that category discount is applied correctly to specified category.
def test_apply_category_discount(discount_with_category, mock_cart_category_discount):
    discount_with_category.apply_category_discount(mock_cart_category_discount, category='electronics', category_discount_rate=0.1)
    assert mock_cart_category_discount.items[1]['price'] == 180

# happy_path - test_apply_loyalty_discount - Test that loyalty discount is applied for loyal users with more than 2 years.
def test_apply_loyalty_discount(discount_with_loyalty, mock_cart_loyalty_discount):
    expected_price = 400 * (1 - 0.15)
    assert discount_with_loyalty.apply_loyalty_discount(mock_cart_loyalty_discount, loyalty_years=3, loyalty_discount_rate=0.15) == expected_price

# happy_path - test_apply_flash_sale_discount - Test that flash sale discount is applied to items on sale.
def test_apply_flash_sale_discount(discount_with_flash_sale, mock_cart_flash_sale_discount):
    discount_with_flash_sale.apply_flash_sale_discount(mock_cart_flash_sale_discount, flash_sale_rate=0.25, items_on_sale=[1, 2])
    assert mock_cart_flash_sale_discount.items[0]['price'] == 75
    assert mock_cart_flash_sale_discount.items[1]['price'] == 150

# edge_case - test_apply_discount_below_min_purchase - Test that no discount is applied when total price is below minimum purchase amount.
def test_apply_discount_below_min_purchase(discount, mock_cart):
    mock_cart.calculate_total_price.return_value = 50
    assert discount.apply_discount(mock_cart) == 50

# edge_case - test_apply_bulk_discount_below_threshold - Test that no bulk discount is applied when item quantity is below threshold.
def test_apply_bulk_discount_below_threshold(discount_with_bulk, mock_cart_bulk_discount):
    mock_cart_bulk_discount.items[0]['quantity'] = 3
    discount_with_bulk.apply_bulk_discount(mock_cart_bulk_discount, bulk_quantity=5, bulk_discount_rate=0.2)
    assert mock_cart_bulk_discount.items[0]['price'] == 100

# edge_case - test_apply_seasonal_discount_non_holiday - Test that seasonal discount is not applied during non-holiday season.
def test_apply_seasonal_discount_non_holiday(discount_with_seasonal, mock_cart_seasonal_discount):
    expected_price = 300
    assert discount_with_seasonal.apply_seasonal_discount(mock_cart_seasonal_discount, season='winter', seasonal_discount_rate=0.2) == expected_price

# edge_case - test_apply_category_discount_other_category - Test that category discount does not affect items from other categories.
def test_apply_category_discount_other_category(discount_with_category, mock_cart_category_discount):
    discount_with_category.apply_category_discount(mock_cart_category_discount, category='clothing', category_discount_rate=0.1)
    assert mock_cart_category_discount.items[0]['price'] == 50
    assert mock_cart_category_discount.items[1]['price'] == 200

# edge_case - test_apply_loyalty_discount_less_than_3_years - Test that no loyalty discount is applied for users with less than 3 years.
def test_apply_loyalty_discount_less_than_3_years(discount_with_loyalty, mock_cart_loyalty_discount):
    expected_price = 400
    assert discount_with_loyalty.apply_loyalty_discount(mock_cart_loyalty_discount, loyalty_years=2, loyalty_discount_rate=0.15) == expected_price

# edge_case - test_apply_flash_sale_discount_no_sale_items - Test that flash sale discount is not applied to items not on sale.
def test_apply_flash_sale_discount_no_sale_items(discount_with_flash_sale, mock_cart_flash_sale_discount):
    discount_with_flash_sale.apply_flash_sale_discount(mock_cart_flash_sale_discount, flash_sale_rate=0.25, items_on_sale=[3])
    assert mock_cart_flash_sale_discount.items[0]['price'] == 100
    assert mock_cart_flash_sale_discount.items[1]['price'] == 200

