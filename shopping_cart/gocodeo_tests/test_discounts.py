import pytest
from unittest.mock import Mock, patch

@pytest.fixture
def mock_cart():
    cart = Mock()
    cart.calculate_total_price = Mock()
    cart.items = []
    cart.user_type = ""
    cart.total_price = 0
    return cart

@pytest.fixture
def discount():
    with patch('path.to.Discount') as MockDiscount:
        instance = MockDiscount.return_value
        yield instance

@pytest.fixture
def setup_dependencies(mock_cart, discount):
    mock_cart.items = [
        {"item_id": 1, "price": 100, "quantity": 1, "category": "electronics"},
    ]
    mock_cart.user_type = "regular"
    mock_cart.calculate_total_price.return_value = 100
    discount.discount_rate = 0.1
    discount.min_purchase_amount = 50
    return mock_cart, discount# happy_path - apply_discount - Applying discount to a cart with total price above minimum purchase amount
def test_apply_discount_happy_path(discount, mock_cart):
    mock_cart.calculate_total_price.return_value = 110
    discount.apply_discount(mock_cart)
    assert mock_cart.total_price == 110


# happy_path - apply_discount - Applying discount to a premium user cart with electronics items
def test_apply_discount_premium_user(discount, mock_cart):
    mock_cart.user_type = 'premium'
    mock_cart.calculate_total_price.return_value = 200
    discount.discount_rate = 0.1
    discount.apply_discount(mock_cart)
    assert mock_cart.total_price == 300


# happy_path - apply_bulk_discount - Applying bulk discount to a cart with eligible items
def test_apply_bulk_discount_happy_path(discount, mock_cart):
    mock_cart.items = [{'item_id': 1, 'price': 100, 'quantity': 5}]
    discount.apply_bulk_discount(mock_cart, bulk_quantity=3, bulk_discount_rate=0.1)
    assert mock_cart.items[0]['price'] == 90


# happy_path - apply_seasonal_discount - Applying seasonal discount during holiday season
def test_apply_seasonal_discount_holiday(discount, mock_cart):
    mock_cart.calculate_total_price.return_value = 200
    discount.apply_seasonal_discount(mock_cart, season='holiday', seasonal_discount_rate=0.2)
    assert mock_cart.total_price == 160


# happy_path - apply_category_discount - Applying category discount to a cart with eligible categories
def test_apply_category_discount_happy_path(discount, mock_cart):
    mock_cart.items = [{'item_id': 1, 'price': 150, 'quantity': 1, 'category': 'clothing'}, {'item_id': 2, 'price': 100, 'quantity': 1, 'category': 'electronics'}]
    discount.apply_category_discount(mock_cart, category='clothing', category_discount_rate=0.15)
    assert mock_cart.items[0]['price'] == 127.5


# happy_path - apply_loyalty_discount - Applying loyalty discount for loyal customers with sufficient years
def test_apply_loyalty_discount_happy_path(discount, mock_cart):
    mock_cart.calculate_total_price.return_value = 300
    mock_cart.user_type = 'loyal'
    discount.apply_loyalty_discount(mock_cart, loyalty_years=3, loyalty_discount_rate=0.1)
    assert mock_cart.total_price == 270


# happy_path - apply_flash_sale_discount - Applying flash sale discount to items on sale
def test_apply_flash_sale_discount_happy_path(discount, mock_cart):
    mock_cart.items = [{'item_id': 1, 'price': 100, 'quantity': 1}]
    discount.apply_flash_sale_discount(mock_cart, flash_sale_rate=0.2, items_on_sale=[1])
    assert mock_cart.items[0]['price'] == 80


# edge_case - apply_discount - Applying discount to a cart with total price below minimum purchase amount
def test_apply_discount_edge_case(discount, mock_cart):
    mock_cart.calculate_total_price.return_value = 50
    discount.apply_discount(mock_cart)
    assert mock_cart.total_price == 50


# edge_case - apply_discount - Applying discount to a premium user cart without electronics items
def test_apply_discount_no_electronics(discount, mock_cart):
    mock_cart.user_type = 'premium'
    mock_cart.items = [{'item_id': 1, 'price': 200, 'quantity': 1, 'category': 'clothing'}]
    mock_cart.calculate_total_price.return_value = 220
    discount.apply_discount(mock_cart)
    assert mock_cart.total_price == 220


# edge_case - apply_bulk_discount - Applying bulk discount with no eligible items
def test_apply_bulk_discount_no_eligible_items(discount, mock_cart):
    mock_cart.items = [{'item_id': 1, 'price': 100, 'quantity': 1}]
    discount.apply_bulk_discount(mock_cart, bulk_quantity=5, bulk_discount_rate=0.1)
    assert mock_cart.items[0]['price'] == 100


# edge_case - apply_seasonal_discount - Applying seasonal discount outside of holiday season
def test_apply_seasonal_discount_non_holiday(discount, mock_cart):
    mock_cart.calculate_total_price.return_value = 200
    discount.apply_seasonal_discount(mock_cart, season='winter', seasonal_discount_rate=0.3)
    assert mock_cart.total_price == 200


# edge_case - apply_category_discount - Applying category discount to a cart with no eligible categories
def test_apply_category_discount_no_eligible_categories(discount, mock_cart):
    mock_cart.items = [{'item_id': 1, 'price': 150, 'quantity': 1, 'category': 'furniture'}]
    discount.apply_category_discount(mock_cart, category='clothing', category_discount_rate=0.15)
    assert mock_cart.items[0]['price'] == 150


# edge_case - apply_loyalty_discount - Applying loyalty discount for non-loyal customers
def test_apply_loyalty_discount_non_loyal(discount, mock_cart):
    mock_cart.calculate_total_price.return_value = 300
    mock_cart.user_type = 'regular'
    discount.apply_loyalty_discount(mock_cart, loyalty_years=1, loyalty_discount_rate=0.1)
    assert mock_cart.total_price == 300


# edge_case - apply_flash_sale_discount - Applying flash sale discount to items not on sale
def test_apply_flash_sale_discount_no_sale_items(discount, mock_cart):
    mock_cart.items = [{'item_id': 1, 'price': 100, 'quantity': 1}]
    discount.apply_flash_sale_discount(mock_cart, flash_sale_rate=0.2, items_on_sale=[2])
    assert mock_cart.items[0]['price'] == 100


