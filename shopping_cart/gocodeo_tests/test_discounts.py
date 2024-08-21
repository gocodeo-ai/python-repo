import pytest
from unittest.mock import Mock

@pytest.fixture
def cart_mock():
    cart = Mock()
    cart.calculate_total_price = Mock()
    return cart

@pytest.fixture
def discount():
    return Discount(discount_rate=0.1, min_purchase_amount=100)

@pytest.fixture
def premium_cart_with_electronics(cart_mock):
    cart_mock.user_type = "premium"
    cart_mock.items = [{"item_id": 1, "category": "electronics", "price": 100, "quantity": 1}]
    cart_mock.calculate_total_price.return_value = sum(item['price'] * item['quantity'] for item in cart_mock.items)
    return cart_mock

@pytest.fixture
def regular_cart_above_min(cart_mock):
    cart_mock.user_type = "regular"
    cart_mock.items = [{"item_id": 2, "category": "clothing", "price": 200, "quantity": 1}]
    cart_mock.calculate_total_price.return_value = sum(item['price'] * item['quantity'] for item in cart_mock.items)
    return cart_mock

@pytest.fixture
def bulk_cart(cart_mock):
    cart_mock.items = [{"item_id": 3, "category": "groceries", "price": 50, "quantity": 10}]
    return cart_mock

@pytest.fixture
def holiday_cart(cart_mock):
    cart_mock.items = []
    cart_mock.calculate_total_price.return_value = 200
    return cart_mock

@pytest.fixture
def category_cart(cart_mock):
    cart_mock.items = [{"item_id": 4, "category": "toys", "price": 100, "quantity": 1}]
    return cart_mock

@pytest.fixture
def loyal_cart(cart_mock):
    cart_mock.user_type = "loyal"
    cart_mock.items = []
    cart_mock.calculate_total_price.return_value = 300
    return cart_mock

@pytest.fixture
def premium_cart_no_items(cart_mock):
    cart_mock.user_type = "premium"
    cart_mock.items = []
    cart_mock.calculate_total_price.return_value = 0
    return cart_mock

@pytest.fixture
def regular_cart_below_min(cart_mock):
    cart_mock.user_type = "regular"
    cart_mock.items = [{"item_id": 5, "category": "clothing", "price": 50, "quantity": 1}]
    cart_mock.calculate_total_price.return_value = 50
    return cart_mock

@pytest.fixture
def bulk_cart_not_met(cart_mock):
    cart_mock.items = [{"item_id": 6, "category": "groceries", "price": 30, "quantity": 2}]
    return cart_mock

@pytest.fixture
def unsupported_season_cart(cart_mock):
    cart_mock.items = []
    cart_mock.calculate_total_price.return_value = 100
    return cart_mock

@pytest.fixture
def empty_category_cart(cart_mock):
    cart_mock.items = []
    return cart_mock

@pytest.fixture
def loyal_cart_insufficient_years(cart_mock):
    cart_mock.user_type = "loyal"
    cart_mock.items = []
    cart_mock.calculate_total_price.return_value = 200
    return cart_mock# happy_path - apply_discount - Applying a discount for a premium user with electronics in the cart.
def test_apply_discount_premium_electronics(premium_cart_with_electronics, discount):
    total_price = discount.apply_discount(premium_cart_with_electronics)
    assert total_price == 1050.0

# edge_case - apply_discount - Applying a discount for a premium user with no items in the cart.
def test_apply_discount_premium_no_items(premium_cart_no_items, discount):
    total_price = discount.apply_discount(premium_cart_no_items)
    assert total_price == 0.0

# edge_case - apply_discount - Applying a discount with total price below minimum purchase amount.
def test_apply_discount_below_min(regular_cart_below_min, discount):
    total_price = discount.apply_discount(regular_cart_below_min)
    assert total_price == 50.0

# edge_case - apply_bulk_discount - Applying a bulk discount when no items meet the bulk requirement.
def test_apply_bulk_discount_not_met(bulk_cart_not_met, discount):
    discount.apply_bulk_discount(bulk_cart_not_met, bulk_quantity=5, bulk_discount_rate=0.1)
    assert bulk_cart_not_met.items[0]['price'] == 30.0

# edge_case - apply_seasonal_discount - Applying a seasonal discount for an unsupported season.
def test_apply_seasonal_discount_unsupported_season(unsupported_season_cart, discount):
    total_price = discount.apply_seasonal_discount(unsupported_season_cart, season='winter', seasonal_discount_rate=0.2)
    assert total_price == 100.0

# edge_case - apply_category_discount - Applying a category discount to an empty cart.
def test_apply_category_discount_empty_cart(empty_category_cart, discount):
    discount.apply_category_discount(empty_category_cart, category='toys', category_discount_rate=0.15)
    assert empty_category_cart.items == []

# edge_case - apply_loyalty_discount - Applying a loyalty discount for a loyal user with insufficient loyalty years.
def test_apply_loyalty_discount_insufficient_years(loyal_cart_insufficient_years, discount):
    total_price = discount.apply_loyalty_discount(loyal_cart_insufficient_years, loyalty_years=1, loyalty_discount_rate=0.1)
    assert total_price == 200.0

