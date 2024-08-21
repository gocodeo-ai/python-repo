import pytest
from unittest.mock import MagicMock

@pytest.fixture
def mock_cart():
    cart = MagicMock()
    cart.calculate_total_price = MagicMock(return_value=100)
    cart.user_type = 'regular'
    cart.items = [{'item_id': 1, 'category': 'electronics', 'price': 100, 'quantity': 1}]
    cart.total_price = 0.0
    return cart

@pytest.fixture
def discount():
    return Discount(discount_rate=0.05, min_purchase_amount=50)

@pytest.fixture
def mock_cart_premium():
    cart = MagicMock()
    cart.calculate_total_price = MagicMock(return_value=100)
    cart.user_type = 'premium'
    cart.items = [{'item_id': 1, 'category': 'electronics', 'price': 100, 'quantity': 1}]
    cart.total_price = 0.0
    return cart

@pytest.fixture
def mock_cart_regular_no_electronics():
    cart = MagicMock()
    cart.calculate_total_price = MagicMock(return_value=100)
    cart.user_type = 'regular'
    cart.items = [{'item_id': 2, 'category': 'clothing', 'price': 100, 'quantity': 1}]
    cart.total_price = 0.0
    return cart

@pytest.fixture
def mock_cart_bulk():
    cart = MagicMock()
    cart.items = [{'item_id': 3, 'category': 'clothing', 'price': 50, 'quantity': 5}]
    return cart

@pytest.fixture
def mock_cart_holiday():
    cart = MagicMock()
    cart.calculate_total_price = MagicMock(return_value=200)
    cart.items = [{'item_id': 4, 'category': 'toys', 'price': 200, 'quantity': 1}]
    cart.total_price = 0.0
    return cart

@pytest.fixture
def mock_cart_clothing():
    cart = MagicMock()
    cart.items = [{'item_id': 5, 'category': 'clothing', 'price': 80, 'quantity': 1}]
    return cart

@pytest.fixture
def mock_cart_loyal():
    cart = MagicMock()
    cart.calculate_total_price = MagicMock(return_value=300)
    cart.user_type = 'loyal'
    cart.items = [{'item_id': 6, 'category': 'electronics', 'price': 300, 'quantity': 1}]
    cart.total_price = 0.0
    return cart

@pytest.fixture
def mock_cart_empty():
    cart = MagicMock()
    cart.calculate_total_price = MagicMock(return_value=0)
    cart.user_type = 'regular'
    cart.items = []
    cart.total_price = 0.0
    return cart

@pytest.fixture
def mock_cart_no_items():
    cart = MagicMock()
    cart.items = []
    return cart

@pytest.fixture
def mock_cart_invalid_season():
    cart = MagicMock()
    cart.calculate_total_price = MagicMock(return_value=500)
    cart.items = [{'item_id': 7, 'category': 'furniture', 'price': 500, 'quantity': 1}]
    cart.total_price = 0.0
    return cart

@pytest.fixture
def mock_cart_no_match():
    cart = MagicMock()
    cart.items = [{'item_id': 8, 'category': 'accessories', 'price': 100, 'quantity': 1}]
    return cart

@pytest.fixture
def mock_cart_non_loyal():
    cart = MagicMock()
    cart.calculate_total_price = MagicMock(return_value=400)
    cart.user_type = 'regular'
    cart.items = [{'item_id': 9, 'category': 'electronics', 'price': 400, 'quantity': 1}]
    cart.total_price = 0.0
    return cart# happy_path - apply_discount - Applying discount for a premium user with electronics in cart.
def test_apply_discount_premium_electronics(mock_cart_premium, discount):
    assert discount.apply_discount(mock_cart_premium) == 102.5

# happy_path - apply_discount - Applying discount for a regular user without electronics in cart.
def test_apply_discount_regular_no_electronics(mock_cart_regular_no_electronics, discount):
    assert discount.apply_discount(mock_cart_regular_no_electronics) == 105.0

# happy_path - apply_bulk_discount - Applying bulk discount for items above bulk quantity.
def test_apply_bulk_discount(mock_cart_bulk, discount):
    discount.apply_bulk_discount(mock_cart_bulk, bulk_quantity=5, bulk_discount_rate=0.1)
    assert mock_cart_bulk.items[0]['price'] == 45.0

# happy_path - apply_seasonal_discount - Applying seasonal discount during holiday season.
def test_apply_seasonal_discount_holiday(mock_cart_holiday, discount):
    assert discount.apply_seasonal_discount(mock_cart_holiday, season='holiday', seasonal_discount_rate=0.2) == 160.0

# happy_path - apply_category_discount - Applying category discount for clothing category.
def test_apply_category_discount(mock_cart_clothing, discount):
    discount.apply_category_discount(mock_cart_clothing, category='clothing', category_discount_rate=0.15)
    assert mock_cart_clothing.items[0]['price'] == 68.0

# happy_path - apply_loyalty_discount - Applying loyalty discount for loyal user with more than 2 years.
def test_apply_loyalty_discount(mock_cart_loyal, discount):
    assert discount.apply_loyalty_discount(mock_cart_loyal, loyalty_years=3, loyalty_discount_rate=0.1) == 270.0

# edge_case - apply_discount - Applying discount with an empty cart.
def test_apply_discount_empty_cart(mock_cart_empty, discount):
    assert discount.apply_discount(mock_cart_empty) == 0.0

# edge_case - apply_bulk_discount - Applying bulk discount with no items in cart.
def test_apply_bulk_discount_no_items(mock_cart_no_items, discount):
    discount.apply_bulk_discount(mock_cart_no_items, bulk_quantity=5, bulk_discount_rate=0.1)
    assert mock_cart_no_items.items == []

# edge_case - apply_seasonal_discount - Applying seasonal discount with an invalid season.
def test_apply_seasonal_discount_invalid_season(mock_cart_invalid_season, discount):
    assert discount.apply_seasonal_discount(mock_cart_invalid_season, season='invalid_season', seasonal_discount_rate=0.3) == 500.0

# edge_case - apply_category_discount - Applying category discount with no matching category.
def test_apply_category_discount_no_match(mock_cart_no_match, discount):
    discount.apply_category_discount(mock_cart_no_match, category='clothing', category_discount_rate=0.2)
    assert mock_cart_no_match.items[0]['price'] == 100.0

# edge_case - apply_loyalty_discount - Applying loyalty discount for a non-loyal user.
def test_apply_loyalty_discount_non_loyal(mock_cart_non_loyal, discount):
    assert discount.apply_loyalty_discount(mock_cart_non_loyal, loyalty_years=1, loyalty_discount_rate=0.1) == 400.0

