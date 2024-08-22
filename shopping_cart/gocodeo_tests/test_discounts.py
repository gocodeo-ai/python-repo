import pytest
from unittest.mock import Mock, patch

@pytest.fixture
def mock_cart():
    mock_cart = Mock()
    mock_cart.calculate_total_price = Mock(return_value=100)
    mock_cart.user_type = 'regular'
    mock_cart.items = []
    mock_cart.total_price = 100
    return mock_cart

@pytest.fixture
def mock_cart_with_items():
    mock_cart = Mock()
    mock_cart.calculate_total_price = Mock(return_value=200)
    mock_cart.user_type = 'regular'
    mock_cart.items = [{'item_id': 1, 'price': 100, 'quantity': 10, 'category': 'electronics'}]
    mock_cart.total_price = 200
    return mock_cart

@pytest.fixture
def mock_cart_premium():
    mock_cart = Mock()
    mock_cart.calculate_total_price = Mock(return_value=200)
    mock_cart.user_type = 'premium'
    mock_cart.items = [{'item_id': 1, 'price': 100, 'quantity': 1, 'category': 'electronics'}]
    mock_cart.total_price = 200
    return mock_cart

@pytest.fixture
def discount():
    return Discount(discount_rate=0.1, min_purchase_amount=50)

@pytest.fixture
def bulk_discount_params():
    return {'bulk_quantity': 5, 'bulk_discount_rate': 0.1}

@pytest.fixture
def seasonal_discount_params():
    return {'season': 'holiday', 'seasonal_discount_rate': 0.2}

@pytest.fixture
def category_discount_params():
    return {'category': 'electronics', 'category_discount_rate': 0.15}

@pytest.fixture
def loyalty_discount_params():
    return {'loyalty_years': 3, 'loyalty_discount_rate': 0.1}

@pytest.fixture
def flash_sale_discount_params():
    return {'flash_sale_rate': 0.25, 'items_on_sale': [1]}

# happy_path - apply_discount - Test that applying discount with adequate total price applies the discount rate.
def test_apply_discount_happy_path(discount, mock_cart):
    mock_cart.total_price = 100
    result = discount.apply_discount(mock_cart)
    assert result == 110

# happy_path - apply_bulk_discount - Test that applying bulk discount reduces the price for eligible items.
def test_apply_bulk_discount_happy_path(discount, mock_cart_with_items, bulk_discount_params):
    discount.apply_bulk_discount(mock_cart_with_items, **bulk_discount_params)
    assert mock_cart_with_items.items[0]['price'] == 90

# happy_path - apply_seasonal_discount - Test that applying seasonal discount during holiday reduces total price correctly.
def test_apply_seasonal_discount_happy_path(discount, mock_cart):
    mock_cart.total_price = 200
    result = discount.apply_seasonal_discount(mock_cart, 'holiday', 0.2)
    assert result == 160

# happy_path - apply_category_discount - Test that applying category discount reduces price for items in the specified category.
def test_apply_category_discount_happy_path(discount, mock_cart_with_items, category_discount_params):
    discount.apply_category_discount(mock_cart_with_items, **category_discount_params)
    assert mock_cart_with_items.items[0]['price'] == 85

# happy_path - apply_loyalty_discount - Test that applying loyalty discount for loyal users with sufficient years reduces total price.
def test_apply_loyalty_discount_happy_path(discount, mock_cart, loyalty_discount_params):
    mock_cart.total_price = 300
    mock_cart.user_type = 'loyal'
    result = discount.apply_loyalty_discount(mock_cart, **loyalty_discount_params)
    assert result == 270

# happy_path - apply_flash_sale_discount - Test that applying flash sale discount reduces price for items on sale.
def test_apply_flash_sale_discount_happy_path(discount, mock_cart_with_items, flash_sale_discount_params):
    discount.apply_flash_sale_discount(mock_cart_with_items, **flash_sale_discount_params)
    assert mock_cart_with_items.items[0]['price'] == 150

# edge_case - apply_discount - Test that applying discount with total price below min purchase amount does not apply discount.
def test_apply_discount_edge_case(discount, mock_cart):
    mock_cart.total_price = 50
    result = discount.apply_discount(mock_cart)
    assert result == 50

# edge_case - apply_bulk_discount - Test that applying bulk discount does not affect items below bulk quantity.
def test_apply_bulk_discount_edge_case(discount, mock_cart, bulk_discount_params):
    mock_cart.items = [{'item_id': 1, 'price': 100, 'quantity': 3}]
    discount.apply_bulk_discount(mock_cart, **bulk_discount_params)
    assert mock_cart.items[0]['price'] == 100

# edge_case - apply_seasonal_discount - Test that applying seasonal discount with no items does not change total price.
def test_apply_seasonal_discount_edge_case(discount, mock_cart):
    mock_cart.total_price = 0
    result = discount.apply_seasonal_discount(mock_cart, 'holiday', 0.2)
    assert result == 0

# edge_case - apply_category_discount - Test that applying category discount does not affect items not in the category.
def test_apply_category_discount_edge_case(discount, mock_cart, category_discount_params):
    mock_cart.items = [{'item_id': 1, 'price': 100, 'category': 'clothing'}]
    discount.apply_category_discount(mock_cart, **category_discount_params)
    assert mock_cart.items[0]['price'] == 100

# edge_case - apply_loyalty_discount - Test that applying loyalty discount for non-loyal users does not change total price.
def test_apply_loyalty_discount_edge_case(discount, mock_cart, loyalty_discount_params):
    mock_cart.total_price = 100
    mock_cart.user_type = 'regular'
    result = discount.apply_loyalty_discount(mock_cart, **loyalty_discount_params)
    assert result == 100

# edge_case - apply_flash_sale_discount - Test that applying flash sale discount to items not on sale does not change their price.
def test_apply_flash_sale_discount_edge_case(discount, mock_cart, flash_sale_discount_params):
    mock_cart.items = [{'item_id': 1, 'price': 200}]
    discount.apply_flash_sale_discount(mock_cart, **flash_sale_discount_params)
    assert mock_cart.items[0]['price'] == 200

