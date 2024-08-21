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
def setup_discount():
    cart = cart_mock()
    discount = Discount(discount_rate=0.1, min_purchase_amount=100)
    return discount, cart

@pytest.fixture
def setup_bulk_discount():
    cart = cart_mock()
    discount = Discount(discount_rate=0.1, min_purchase_amount=100)
    return discount, cart

@pytest.fixture
def setup_seasonal_discount():
    cart = cart_mock()
    discount = Discount(discount_rate=0.1, min_purchase_amount=100)
    return discount, cart

@pytest.fixture
def setup_category_discount():
    cart = cart_mock()
    discount = Discount(discount_rate=0.1, min_purchase_amount=100)
    return discount, cart

@pytest.fixture
def setup_loyalty_discount():
    cart = cart_mock()
    discount = Discount(discount_rate=0.1, min_purchase_amount=100)
    return discount, cart

@pytest.fixture
def setup_flash_sale_discount():
    cart = cart_mock()
    discount = Discount(discount_rate=0.1, min_purchase_amount=100)
    return discount, cart

# happy_path - apply_discount - Applying discount to a cart with total price above min_purchase_amount and user type premium with electronics item
def test_apply_discount_premium_electronics(setup_discount):
    discount, cart = setup_discount
    cart.items = [{'item_id': 1, 'category': 'electronics', 'price': 100, 'quantity': 1}]
    cart.user_type = 'premium'
    cart.calculate_total_price.return_value = 100
    assert discount.apply_discount(cart) == 150.0


# happy_path - apply_discount - Applying discount to a cart with total price above min_purchase_amount and user type regular
def test_apply_discount_regular_user(setup_discount):
    discount, cart = setup_discount
    cart.items = [{'item_id': 2, 'category': 'clothing', 'price': 100, 'quantity': 1}]
    cart.user_type = 'regular'
    cart.calculate_total_price.return_value = 100
    assert discount.apply_discount(cart) == 110.0


# happy_path - apply_bulk_discount - Applying bulk discount for items meeting the bulk quantity requirement
def test_apply_bulk_discount(setup_bulk_discount):
    discount, cart = setup_bulk_discount
    cart.items = [{'item_id': 3, 'category': 'clothing', 'price': 50, 'quantity': 10}]
    discount.apply_bulk_discount(cart, bulk_quantity=5, bulk_discount_rate=0.1)
    assert cart.items[0]['price'] == 45.0


# happy_path - apply_seasonal_discount - Applying seasonal discount during holiday season
def test_apply_seasonal_discount_holiday(setup_seasonal_discount):
    discount, cart = setup_seasonal_discount
    cart.items = [{'item_id': 4, 'category': 'toys', 'price': 200, 'quantity': 1}]
    cart.calculate_total_price.return_value = 200
    assert discount.apply_seasonal_discount(cart, season='holiday', seasonal_discount_rate=0.2) == 160.0


# happy_path - apply_category_discount - Applying category discount to a cart with items in the specified category
def test_apply_category_discount(setup_category_discount):
    discount, cart = setup_category_discount
    cart.items = [{'item_id': 5, 'category': 'electronics', 'price': 300, 'quantity': 1}]
    discount.apply_category_discount(cart, category='electronics', category_discount_rate=0.15)
    assert cart.items[0]['price'] == 255.0


# happy_path - apply_loyalty_discount - Applying loyalty discount for loyal customers with sufficient loyalty years
def test_apply_loyalty_discount(setup_loyalty_discount):
    discount, cart = setup_loyalty_discount
    cart.items = [{'item_id': 6, 'category': 'clothing', 'price': 150, 'quantity': 1}]
    cart.user_type = 'loyal'
    cart.calculate_total_price.return_value = 150
    assert discount.apply_loyalty_discount(cart, loyalty_years=3, loyalty_discount_rate=0.1) == 135.0


# edge_case - apply_discount - Applying discount to a cart with total price below min_purchase_amount
def test_apply_discount_below_min_purchase(setup_discount):
    discount, cart = setup_discount
    cart.items = [{'item_id': 7, 'category': 'clothing', 'price': 50, 'quantity': 1}]
    cart.user_type = 'regular'
    cart.calculate_total_price.return_value = 50
    assert discount.apply_discount(cart) == 50.0


# edge_case - apply_bulk_discount - Applying bulk discount with no items meeting the bulk quantity requirement
def test_apply_bulk_discount_no_items(setup_bulk_discount):
    discount, cart = setup_bulk_discount
    cart.items = [{'item_id': 8, 'category': 'clothing', 'price': 30, 'quantity': 1}]
    discount.apply_bulk_discount(cart, bulk_quantity=5, bulk_discount_rate=0.1)
    assert cart.items[0]['price'] == 30.0


# edge_case - apply_seasonal_discount - Applying seasonal discount with invalid season
def test_apply_seasonal_discount_invalid_season(setup_seasonal_discount):
    discount, cart = setup_seasonal_discount
    cart.items = [{'item_id': 9, 'category': 'toys', 'price': 100, 'quantity': 1}]
    cart.calculate_total_price.return_value = 100
    assert discount.apply_seasonal_discount(cart, season='invalid_season', seasonal_discount_rate=0.2) == 100.0


# edge_case - apply_category_discount - Applying category discount to a cart with no items in the specified category
def test_apply_category_discount_no_matching_items(setup_category_discount):
    discount, cart = setup_category_discount
    cart.items = [{'item_id': 10, 'category': 'furniture', 'price': 500, 'quantity': 1}]
    discount.apply_category_discount(cart, category='electronics', category_discount_rate=0.15)
    assert cart.items[0]['price'] == 500.0


# edge_case - apply_loyalty_discount - Applying loyalty discount for loyal customers with insufficient loyalty years
def test_apply_loyalty_discount_insufficient_years(setup_loyalty_discount):
    discount, cart = setup_loyalty_discount
    cart.items = [{'item_id': 11, 'category': 'clothing', 'price': 200, 'quantity': 1}]
    cart.user_type = 'loyal'
    cart.calculate_total_price.return_value = 200
    assert discount.apply_loyalty_discount(cart, loyalty_years=1, loyalty_discount_rate=0.1) == 200.0


