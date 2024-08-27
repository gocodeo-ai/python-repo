import pytest
from unittest.mock import Mock

@pytest.fixture
def mock_cart():
    cart = Mock()
    cart.calculate_total_price = Mock()
    cart.user_type = None
    cart.items = []
    cart.total_price = 0
    return cart

@pytest.fixture
def discount():
    from your_module import your_discount  # Replace 'your_module' with the actual module name
    return your_discount

@pytest.fixture
def mock_dependencies():
    # Mock any other dependencies if necessary
    pass

# happy_path - apply_discount - Test that premium user gets additional discount on electronics when discount is applied.
def test_apply_discount_premium_user(mock_cart, discount):
    mock_cart.calculate_total_price.return_value = 200
    mock_cart.user_type = 'premium'
    mock_cart.items = [{'category': 'electronics', 'price': 100}, {'category': 'books', 'price': 100}]
    discount_instance = discount(0.1, 50)
    result = discount_instance.apply_discount(mock_cart)
    assert result == 215

# happy_path - apply_bulk_discount - Test that bulk discount is applied correctly when quantity meets bulk quantity.
def test_apply_bulk_discount_happy_path(mock_cart, discount):
    mock_cart.items = [{'category': 'books', 'quantity': 10, 'price': 15}, {'category': 'clothing', 'quantity': 5, 'price': 20}]
    discount_instance = discount(0.1)
    discount_instance.apply_bulk_discount(mock_cart, 5, 0.2)
    assert mock_cart.items[0]['price'] == 15
    assert mock_cart.items[1]['price'] == 16

# happy_path - apply_seasonal_discount - Test that seasonal discount is applied correctly during holiday season.
def test_apply_seasonal_discount_holiday(mock_cart, discount):
    mock_cart.calculate_total_price.return_value = 300
    discount_instance = discount(0.1)
    result = discount_instance.apply_seasonal_discount(mock_cart, 'holiday', 0.3)
    assert result == 210

# happy_path - apply_category_discount - Test that category discount is applied correctly to specified category items.
def test_apply_category_discount_happy_path(mock_cart, discount):
    mock_cart.items = [{'category': 'electronics', 'price': 100}, {'category': 'books', 'price': 50}]
    discount_instance = discount(0.1)
    discount_instance.apply_category_discount(mock_cart, 'electronics', 0.2)
    assert mock_cart.items[0]['price'] == 80
    assert mock_cart.items[1]['price'] == 50

# happy_path - apply_loyalty_discount - Test that loyalty discount is applied correctly for loyal users with more than 2 years.
def test_apply_loyalty_discount_happy_path(mock_cart, discount):
    mock_cart.calculate_total_price.return_value = 400
    mock_cart.user_type = 'loyal'
    discount_instance = discount(0.1)
    result = discount_instance.apply_loyalty_discount(mock_cart, 13, 0.1)
    assert result == 360

# happy_path - apply_flash_sale_discount - Test that flash sale discount is applied correctly to items on sale.
def test_apply_flash_sale_discount_happy_path(mock_cart, discount):
    mock_cart.items = [{'item_id': 1, 'price': 50}, {'item_id': 2, 'price': 100}]
    discount_instance = discount(0.1)
    discount_instance.apply_flash_sale_discount(mock_cart, 0.3, [1])
    assert mock_cart.items[0]['price'] == 35
    assert mock_cart.items[1]['price'] == 100

# edge_case - apply_discount - Test that no discount is applied when total price is below minimum purchase amount.
def test_apply_discount_edge_case_below_minimum(mock_cart, discount):
    mock_cart.calculate_total_price.return_value = 40
    mock_cart.user_type = 'regular'
    mock_cart.items = [{'category': 'books', 'price': 40}]
    discount_instance = discount(0.1, 50)
    result = discount_instance.apply_discount(mock_cart)
    assert result == 40

# edge_case - apply_discount - Test that no additional discount for premium user when no electronics are in cart.
def test_apply_discount_edge_case_no_electronics(mock_cart, discount):
    mock_cart.calculate_total_price.return_value = 200
    mock_cart.user_type = 'premium'
    mock_cart.items = [{'category': 'books', 'price': 200}]
    discount_instance = discount(0.1, 50)
    result = discount_instance.apply_discount(mock_cart)
    assert result == 220

# edge_case - apply_bulk_discount - Test that no bulk discount is applied when quantity is below bulk quantity.
def test_apply_bulk_discount_edge_case_below_quantity(mock_cart, discount):
    mock_cart.items = [{'category': 'books', 'quantity': 4, 'price': 15}, {'category': 'clothing', 'quantity': 5, 'price': 20}]
    discount_instance = discount(0.1)
    discount_instance.apply_bulk_discount(mock_cart, 5, 0.2)
    assert mock_cart.items[0]['price'] == 15
    assert mock_cart.items[1]['price'] == 20

# edge_case - apply_seasonal_discount - Test that no seasonal discount is applied for non-holiday season.
def test_apply_seasonal_discount_edge_case_non_holiday(mock_cart, discount):
    mock_cart.calculate_total_price.return_value = 300
    discount_instance = discount(0.1)
    result = discount_instance.apply_seasonal_discount(mock_cart, 'spring', 0.3)
    assert result == 300

# edge_case - apply_category_discount - Test that no category discount is applied when category does not match.
def test_apply_category_discount_edge_case_no_match(mock_cart, discount):
    mock_cart.items = [{'category': 'clothing', 'price': 100}, {'category': 'books', 'price': 50}]
    discount_instance = discount(0.1)
    discount_instance.apply_category_discount(mock_cart, 'electronics', 0.2)
    assert mock_cart.items[0]['price'] == 100
    assert mock_cart.items[1]['price'] == 50

# edge_case - apply_loyalty_discount - Test that no loyalty discount is applied for non-loyal users.
def test_apply_loyalty_discount_edge_case_non_loyal(mock_cart, discount):
    mock_cart.calculate_total_price.return_value = 400
    mock_cart.user_type = 'new'
    discount_instance = discount(0.1)
    result = discount_instance.apply_loyalty_discount(mock_cart, 3, 0.1)
    assert result == 400

# edge_case - apply_flash_sale_discount - Test that no flash sale discount is applied for items not on sale.
def test_apply_flash_sale_discount_edge_case_no_sale(mock_cart, discount):
    mock_cart.items = [{'item_id': 1, 'price': 50}, {'item_id': 2, 'price': 100}]
    discount_instance = discount(0.1)
    discount_instance.apply_flash_sale_discount(mock_cart, 0.3, [3])
    assert mock_cart.items[0]['price'] == 50
    assert mock_cart.items[1]['price'] == 100

