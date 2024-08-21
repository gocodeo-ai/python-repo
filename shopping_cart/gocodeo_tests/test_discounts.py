import pytest
from unittest.mock import Mock

@pytest.fixture
def cart_mock():
    cart = Mock()
    cart.user_type = "regular"
    cart.items = []
    cart.calculate_total_price = Mock(return_value=0)
    cart.total_price = 0
    return cart

@pytest.fixture
def discount():
    return Discount(discount_rate=0.1, min_purchase_amount=50)

@pytest.fixture
def premium_cart_mock():
    cart = Mock()
    cart.user_type = "premium"
    cart.items = [{"item_id": 2, "category": "electronics", "price": 200, "quantity": 1}]
    cart.calculate_total_price = Mock(return_value=200)
    cart.total_price = 200
    return cart

@pytest.fixture
def bulk_cart_mock():
    cart = Mock()
    cart.items = [{"item_id": 3, "category": "furniture", "price": 300, "quantity": 5}]
    return cart

@pytest.fixture
def holiday_cart_mock():
    cart = Mock()
    cart.items = [{"item_id": 4, "category": "toys", "price": 50, "quantity": 2}]
    cart.calculate_total_price = Mock(return_value=100)
    cart.total_price = 100
    return cart

@pytest.fixture
def category_cart_mock():
    cart = Mock()
    cart.items = [{"item_id": 5, "category": "electronics", "price": 150, "quantity": 1}]
    return cart

@pytest.fixture
def loyal_cart_mock():
    cart = Mock()
    cart.user_type = "loyal"
    cart.items = [{"item_id": 6, "category": "books", "price": 40, "quantity": 3}]
    cart.calculate_total_price = Mock(return_value=120)
    cart.total_price = 120
    return cart

@pytest.fixture
def flash_sale_cart_mock():
    cart = Mock()
    cart.items = [{"item_id": 7, "category": "kitchen", "price": 80, "quantity": 1}]
    return cart

@pytest.fixture
def insufficient_cart_mock():
    cart = Mock()
    cart.user_type = "regular"
    cart.items = [{"item_id": 8, "category": "clothing", "price": 50, "quantity": 1}]
    cart.calculate_total_price = Mock(return_value=50)
    cart.total_price = 50
    return cart

@pytest.fixture
def no_items_cart_mock():
    cart = Mock()
    cart.user_type = "regular"
    cart.items = []
    cart.calculate_total_price = Mock(return_value=0)
    cart.total_price = 0
    return cart

@pytest.fixture
def no_eligible_bulk_cart_mock():
    cart = Mock()
    cart.items = [{"item_id": 9, "category": "furniture", "price": 400, "quantity": 1}]
    return cart

@pytest.fixture
def no_matching_category_cart_mock():
    cart = Mock()
    cart.items = [{"item_id": 10, "category": "toys", "price": 30, "quantity": 1}]
    return cart

@pytest.fixture
def insufficient_years_loyal_cart_mock():
    cart = Mock()
    cart.user_type = "loyal"
    cart.items = [{"item_id": 11, "category": "books", "price": 60, "quantity": 1}]
    cart.calculate_total_price = Mock(return_value=60)
    cart.total_price = 60
    return cart

@pytest.fixture
def no_eligible_flash_sale_cart_mock():
    cart = Mock()
    cart.items = [{"item_id": 12, "category": "kitchen", "price": 70, "quantity": 1}]
    return cart# happy_path - apply_discount - Applying a discount with sufficient purchase amount.
def test_apply_discount_happy_path(discount, cart_mock):
    cart_mock.user_type = 'regular'
    cart_mock.items = [{'item_id': 1, 'category': 'clothing', 'price': 100, 'quantity': 1}]
    cart_mock.calculate_total_price = Mock(return_value=100)
    expected_result = 110
    assert discount.apply_discount(cart_mock) == expected_result

# happy_path - apply_discount - Applying a premium discount for electronics.
def test_apply_discount_premium_happy_path(discount, premium_cart_mock):
    expected_result = 320
    assert discount.apply_discount(premium_cart_mock) == expected_result

# happy_path - apply_bulk_discount - Applying a bulk discount.
def test_apply_bulk_discount_happy_path(discount, bulk_cart_mock):
    discount.apply_bulk_discount(bulk_cart_mock, bulk_quantity=3, bulk_discount_rate=0.1)
    expected_result = [{'item_id': 3, 'price': 270.0, 'quantity': 5}]
    assert bulk_cart_mock.items == expected_result

# happy_path - apply_seasonal_discount - Applying a seasonal discount during holidays.
def test_apply_seasonal_discount_happy_path(discount, holiday_cart_mock):
    expected_result = 80
    assert discount.apply_seasonal_discount(holiday_cart_mock, season='holiday', seasonal_discount_rate=0.2) == expected_result

# happy_path - apply_category_discount - Applying a category discount.
def test_apply_category_discount_happy_path(discount, category_cart_mock):
    discount.apply_category_discount(category_cart_mock, category='electronics', category_discount_rate=0.15)
    expected_result = [{'item_id': 5, 'price': 127.5, 'quantity': 1}]
    assert category_cart_mock.items == expected_result

# happy_path - apply_loyalty_discount - Applying a loyalty discount for loyal customers.
def test_apply_loyalty_discount_happy_path(discount, loyal_cart_mock):
    expected_result = 108
    assert discount.apply_loyalty_discount(loyal_cart_mock, loyalty_years=3, loyalty_discount_rate=0.1) == expected_result

# happy_path - apply_flash_sale_discount - Applying a flash sale discount.
def test_apply_flash_sale_discount_happy_path(discount, flash_sale_cart_mock):
    discount.apply_flash_sale_discount(flash_sale_cart_mock, flash_sale_rate=0.2, items_on_sale=[7])
    expected_result = [{'item_id': 7, 'price': 64.0, 'quantity': 1}]
    assert flash_sale_cart_mock.items == expected_result

# edge_case - apply_discount - Applying a discount with insufficient purchase amount.
def test_apply_discount_edge_case(discount, insufficient_cart_mock):
    expected_result = 50
    assert discount.apply_discount(insufficient_cart_mock) == expected_result

# edge_case - apply_discount - Applying a discount with no items.
def test_apply_discount_no_items_edge_case(discount, no_items_cart_mock):
    expected_result = 0
    assert discount.apply_discount(no_items_cart_mock) == expected_result

# edge_case - apply_bulk_discount - Applying a bulk discount with no eligible items.
def test_apply_bulk_discount_no_eligible_items_edge_case(discount, no_eligible_bulk_cart_mock):
    discount.apply_bulk_discount(no_eligible_bulk_cart_mock, bulk_quantity=10, bulk_discount_rate=0.1)
    expected_result = [{'item_id': 9, 'price': 400, 'quantity': 1}]
    assert no_eligible_bulk_cart_mock.items == expected_result

# edge_case - apply_seasonal_discount - Applying a seasonal discount with no items.
def test_apply_seasonal_discount_no_items_edge_case(discount, no_items_cart_mock):
    expected_result = 0
    assert discount.apply_seasonal_discount(no_items_cart_mock, season='holiday', seasonal_discount_rate=0.2) == expected_result

# edge_case - apply_category_discount - Applying a category discount with no matching category.
def test_apply_category_discount_no_matching_category_edge_case(discount, no_matching_category_cart_mock):
    discount.apply_category_discount(no_matching_category_cart_mock, category='electronics', category_discount_rate=0.15)
    expected_result = [{'item_id': 10, 'price': 30, 'quantity': 1}]
    assert no_matching_category_cart_mock.items == expected_result

# edge_case - apply_loyalty_discount - Applying a loyalty discount with insufficient years.
def test_apply_loyalty_discount_insufficient_years_edge_case(discount, insufficient_years_loyal_cart_mock):
    expected_result = 60
    assert discount.apply_loyalty_discount(insufficient_years_loyal_cart_mock, loyalty_years=1, loyalty_discount_rate=0.1) == expected_result

# edge_case - apply_flash_sale_discount - Applying a flash sale discount with no eligible items.
def test_apply_flash_sale_discount_no_eligible_items_edge_case(discount, no_eligible_flash_sale_cart_mock):
    discount.apply_flash_sale_discount(no_eligible_flash_sale_cart_mock, flash_sale_rate=0.2, items_on_sale=[13])
    expected_result = [{'item_id': 12, 'price': 70, 'quantity': 1}]
    assert no_eligible_flash_sale_cart_mock.items == expected_result

