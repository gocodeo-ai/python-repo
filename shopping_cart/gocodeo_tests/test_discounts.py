import pytest
from unittest.mock import MagicMock, patch
from shopping_cart.discounts import Discount

@pytest.fixture
def mock_cart():
    cart = MagicMock()
    cart.calculate_total_price = MagicMock(return_value=100)
    return cart

@pytest.fixture
def discount():
    return Discount(discount_rate=0.1, min_purchase_amount=50)

@pytest.fixture
def mock_cart_with_items():
    cart = MagicMock()
    cart.items = [{'category': 'electronics', 'price': 100, 'quantity': 1}]
    cart.user_type = 'premium'
    cart.calculate_total_price = MagicMock(return_value=100)
    return cart

@pytest.fixture
def mock_cart_loyal():
    cart = MagicMock()
    cart.user_type = 'loyal'
    cart.calculate_total_price = MagicMock(return_value=100)
    return cart

@pytest.fixture
def mock_cart_non_loyal():
    cart = MagicMock()
    cart.user_type = 'new'
    cart.calculate_total_price = MagicMock(return_value=100)
    return cart

@pytest.fixture
def mock_cart_bulk():
    cart = MagicMock()
    cart.items = [{'category': 'books', 'quantity': 10, 'price': 100}]
    return cart

@pytest.fixture
def mock_cart_seasonal():
    cart = MagicMock()
    cart.calculate_total_price = MagicMock(return_value=100)
    return cart

@pytest.fixture
def mock_cart_category_discount():
    cart = MagicMock()
    cart.items = [{'category': 'clothing', 'price': 100}]
    return cart

@pytest.fixture
def mock_cart_flash_sale():
    cart = MagicMock()
    cart.items = [{'item_id': 1, 'price': 100}]
    return cart

# happy path - apply_discount - Test that apply_discount applies premium electronics discount correctly
def test_apply_discount_premium_electronics(mock_cart_with_items, discount):
    cart = mock_cart_with_items
    discount.apply_discount(cart)
    assert cart.total_price == 251.5


# happy path - apply_bulk_discount - Test that apply_bulk_discount applies discount for bulk items
def test_apply_bulk_discount(mock_cart_bulk, discount):
    cart = mock_cart_bulk
    discount.apply_bulk_discount(cart, bulk_quantity=5, bulk_discount_rate=0.1)
    assert cart.items[0]['price'] == 90


# happy path - apply_seasonal_discount - Test that apply_seasonal_discount applies holiday discount
def test_apply_seasonal_discount_holiday(mock_cart_seasonal, discount):
    cart = mock_cart_seasonal
    discount.apply_seasonal_discount(cart, season='holiday', seasonal_discount_rate=0.2)
    assert cart.total_price == 80


# happy path - apply_category_discount - Test that apply_category_discount applies discount to specified category
def test_apply_category_discount(mock_cart_category_discount, discount):
    cart = mock_cart_category_discount
    discount.apply_category_discount(cart, category='clothing', category_discount_rate=0.15)
    assert cart.items[0]['price'] == 85


# happy path - apply_loyalty_discount - Test that apply_loyalty_discount applies discount for loyal customers
def test_apply_loyalty_discount(mock_cart_loyal, discount):
    cart = mock_cart_loyal
    discount.apply_loyalty_discount(cart, loyalty_years=3, loyalty_discount_rate=0.1)
    assert cart.total_price == 90


# happy path - apply_flash_sale_discount - Test that apply_flash_sale_discount applies discount to items on sale
def test_apply_flash_sale_discount(mock_cart_flash_sale, discount):
    cart = mock_cart_flash_sale
    discount.apply_flash_sale_discount(cart, flash_sale_rate=0.25, items_on_sale=[1])
    assert cart.items[0]['price'] == 75


# edge case - apply_discount - Test that apply_discount does not apply discount below minimum purchase
def test_apply_discount_below_minimum(mock_cart, discount):
    cart = mock_cart
    cart.items = [{'category': 'books', 'price': 50}]
    cart.user_type = 'regular'
    discount.min_purchase_amount = 100
    discount.apply_discount(cart)
    assert cart.total_price == 50


# edge case - apply_bulk_discount - Test that apply_bulk_discount does not apply discount for non-bulk items
def test_apply_bulk_discount_non_bulk(mock_cart, discount):
    cart = mock_cart
    cart.items = [{'category': 'books', 'quantity': 2, 'price': 100}]
    discount.apply_bulk_discount(cart, bulk_quantity=5, bulk_discount_rate=0.1)
    assert cart.items[0]['price'] == 100


# edge case - apply_seasonal_discount - Test that apply_seasonal_discount applies no discount for non-season
def test_apply_seasonal_discount_non_season(mock_cart_seasonal, discount):
    cart = mock_cart_seasonal
    discount.apply_seasonal_discount(cart, season='winter', seasonal_discount_rate=0.2)
    assert cart.total_price == 100


# edge case - apply_category_discount - Test that apply_category_discount does not apply discount to other categories
def test_apply_category_discount_other_category(mock_cart, discount):
    cart = mock_cart
    cart.items = [{'category': 'electronics', 'price': 100}]
    discount.apply_category_discount(cart, category='clothing', category_discount_rate=0.15)
    assert cart.items[0]['price'] == 100


# edge case - apply_loyalty_discount - Test that apply_loyalty_discount does not apply discount for non-loyal customers
def test_apply_loyalty_discount_non_loyal(mock_cart_non_loyal, discount):
    cart = mock_cart_non_loyal
    discount.apply_loyalty_discount(cart, loyalty_years=1, loyalty_discount_rate=0.1)
    assert cart.total_price == 100


# edge case - apply_flash_sale_discount - Test that apply_flash_sale_discount does not apply discount to non-sale items
def test_apply_flash_sale_discount_non_sale(mock_cart, discount):
    cart = mock_cart
    cart.items = [{'item_id': 2, 'price': 100}]
    discount.apply_flash_sale_discount(cart, flash_sale_rate=0.25, items_on_sale=[1])
    assert cart.items[0]['price'] == 100


