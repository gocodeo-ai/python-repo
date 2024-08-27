import pytest
from unittest.mock import Mock

@pytest.fixture
def mock_cart():
    cart = Mock()
    cart.calculate_total_price = Mock()
    cart.items = []
    return cart

@pytest.fixture
def discount():
    return Discount(0.1)

@pytest.fixture
def premium_electronics_cart(mock_cart):
    mock_cart.calculate_total_price.return_value = 1000
    mock_cart.user_type = "premium"
    mock_cart.items = [{"category": "electronics", "price": 500}]
    return mock_cart

@pytest.fixture
def regular_cart(mock_cart):
    mock_cart.calculate_total_price.return_value = 500
    mock_cart.user_type = "regular"
    mock_cart.items = [{"category": "clothing", "price": 500}]
    return mock_cart

@pytest.fixture
def bulk_cart(mock_cart):
    mock_cart.items = [{"quantity": 10, "price": 100}]
    return mock_cart

@pytest.fixture
def holiday_cart(mock_cart):
    mock_cart.calculate_total_price.return_value = 1000
    return mock_cart

@pytest.fixture
def books_cart(mock_cart):
    mock_cart.items = [{"category": "books", "price": 50}]
    return mock_cart

@pytest.fixture
def loyal_cart(mock_cart):
    mock_cart.calculate_total_price.return_value = 1000
    mock_cart.user_type = "loyal"
    return mock_cart

@pytest.fixture
def flash_sale_cart(mock_cart):
    mock_cart.items = [{"item_id": 101, "price": 100}]
    return mock_cart

@pytest.fixture
def below_minimum_cart(mock_cart):
    mock_cart.calculate_total_price.return_value = 50
    mock_cart.user_type = "regular"
    mock_cart.items = [{"category": "clothing", "price": 50}]
    return mock_cart

@pytest.fixture
def below_bulk_quantity_cart(mock_cart):
    mock_cart.items = [{"quantity": 4, "price": 100}]
    return mock_cart

@pytest.fixture
def non_holiday_cart(mock_cart):
    mock_cart.calculate_total_price.return_value = 1000
    return mock_cart

@pytest.fixture
def non_matching_category_cart(mock_cart):
    mock_cart.items = [{"category": "toys", "price": 50}]
    return mock_cart

@pytest.fixture
def non_loyal_cart(mock_cart):
    mock_cart.calculate_total_price.return_value = 1000
    mock_cart.user_type = "regular"
    return mock_cart

@pytest.fixture
def non_sale_item_cart(mock_cart):
    mock_cart.items = [{"item_id": 102, "price": 100}]
    return mock_cart

# happy_path - test_apply_discount_premium_electronics - Test that apply_discount applies premium discount to electronics category
def test_apply_discount_premium_electronics(discount, mock_cart_premium_electronics):
    result = discount.apply_discount(mock_cart_premium_electronics)
    assert result == 0
    assert mock_cart_premium_electronics.total_price == 0

# happy_path - test_apply_discount_standard - Test that apply_discount applies standard discount when total price meets minimum purchase amount
def test_apply_discount_standard(discount, regular_cart):
    expected_total = 500 * 1.1
    result = discount.apply_discount(regular_cart)
    assert result == expected_total

# happy_path - test_apply_bulk_discount - Test that apply_bulk_discount applies discount to items meeting bulk quantity
def test_apply_bulk_discount(discount, bulk_cart):
    discount.apply_bulk_discount(bulk_cart, bulk_quantity=5, bulk_discount_rate=0.1)
    assert bulk_cart.items[0]["price"] == 90

# happy_path - test_apply_seasonal_discount_holiday - Test that apply_seasonal_discount applies holiday discount
def test_apply_seasonal_discount_holiday(discount, holiday_cart):
    expected_total = 1000 * 0.8
    result = discount.apply_seasonal_discount(holiday_cart, season='holiday', seasonal_discount_rate=0.2)
    assert result == expected_total

# happy_path - test_apply_category_discount - Test that apply_category_discount applies discount to specified category
def test_apply_category_discount(discount, books_cart):
    discount.apply_category_discount(books_cart, category='books', category_discount_rate=0.2)
    assert books_cart.items[0]["price"] == 40

# happy_path - test_apply_loyalty_discount - Test that apply_loyalty_discount applies discount for loyal users over 2 years
def test_apply_loyalty_discount(discount, loyal_cart):
    expected_total = 1000 * 0.85
    result = discount.apply_loyalty_discount(loyal_cart, loyalty_years=3, loyalty_discount_rate=0.15)
    assert result == expected_total

# happy_path - test_apply_flash_sale_discount - Test that apply_flash_sale_discount applies discount to items on sale
def test_apply_flash_sale_discount(discount, flash_sale_cart):
    discount.apply_flash_sale_discount(flash_sale_cart, flash_sale_rate=0.25, items_on_sale=[101])
    assert flash_sale_cart.items[0]["price"] == 75

# edge_case - test_apply_discount_below_minimum - Test that apply_discount does not apply discount when total price is below minimum purchase amount
def test_apply_discount_below_minimum(discount, below_minimum_cart):
    expected_total = 50
    result = discount.apply_discount(below_minimum_cart)
    assert result == expected_total

# edge_case - test_apply_bulk_discount_below_quantity - Test that apply_bulk_discount does not apply discount to items below bulk quantity
def test_apply_bulk_discount_below_quantity(discount, below_bulk_quantity_cart):
    discount.apply_bulk_discount(below_bulk_quantity_cart, bulk_quantity=5, bulk_discount_rate=0.1)
    assert below_bulk_quantity_cart.items[0]["price"] == 100

# edge_case - test_apply_seasonal_discount_non_holiday - Test that apply_seasonal_discount applies no discount for non-holiday season
def test_apply_seasonal_discount_non_holiday(discount, non_holiday_cart):
    expected_total = 1000
    result = discount.apply_seasonal_discount(non_holiday_cart, season='spring', seasonal_discount_rate=0.2)
    assert result == expected_total

# edge_case - test_apply_category_discount_non_matching - Test that apply_category_discount does not apply discount to non-specified category
def test_apply_category_discount_non_matching(discount, non_matching_category_cart):
    discount.apply_category_discount(non_matching_category_cart, category='books', category_discount_rate=0.2)
    assert non_matching_category_cart.items[0]["price"] == 50

# edge_case - test_apply_loyalty_discount_non_loyal - Test that apply_loyalty_discount does not apply discount for non-loyal users
def test_apply_loyalty_discount_non_loyal(discount, non_loyal_cart):
    expected_total = 1000
    result = discount.apply_loyalty_discount(non_loyal_cart, loyalty_years=3, loyalty_discount_rate=0.15)
    assert result == expected_total

# edge_case - test_apply_flash_sale_discount_non_sale_item - Test that apply_flash_sale_discount does not apply discount to items not on sale
def test_apply_flash_sale_discount_non_sale_item(discount, non_sale_item_cart):
    discount.apply_flash_sale_discount(non_sale_item_cart, flash_sale_rate=0.25, items_on_sale=[101])
    assert non_sale_item_cart.items[0]["price"] == 100

