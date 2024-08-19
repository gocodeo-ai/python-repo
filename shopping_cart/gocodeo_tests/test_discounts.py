import pytest
from unittest.mock import MagicMock, patch

# Mocking the Cart class
class MockCart:
    def __init__(self, items, user_type):
        self.items = items
        self.user_type = user_type
        self.total_price = 0

    def calculate_total_price(self):
        return sum(item['price'] * item['quantity'] for item in self.items)

@pytest.fixture
def mock_cart():
    with patch('shopping_cart.discounts.Cart', new=MockCart):
        yield MockCart

@pytest.fixture
def discount():
    with patch('shopping_cart.discounts.Discount') as MockDiscount:
        yield MockDiscount

@pytest.fixture
def setup_dependencies(mock_cart, discount):
    mock_cart_instance = mock_cart(items=[], user_type='regular')
    discount_instance = discount(discount_rate=0.1, min_purchase_amount=100)
    return mock_cart_instance, discount_instance# happy_path - apply_discount - generate test cases on applying premium discount for electronics user
def test_apply_discount_premium_electronics(mock_cart):
    cart = mock_cart(items=[{'item_id': 2, 'price': 200, 'quantity': 1, 'category': 'electronics'}], user_type='premium')
    discount = Discount(discount_rate=0.05)
    total_price = discount.apply_discount(cart)
    assert total_price == 305.0

# happy_path - apply_bulk_discount - generate test cases on applying bulk discount when quantity meets requirement
def test_apply_bulk_discount_happy_path(mock_cart):
    cart = mock_cart(items=[{'item_id': 3, 'price': 50, 'quantity': 5, 'category': 'clothing'}], user_type='regular')
    discount = Discount(discount_rate=0.1)
    discount.apply_bulk_discount(cart, bulk_quantity=5, bulk_discount_rate=0.1)
    assert cart.items[0]['price'] == 45.0

# happy_path - apply_seasonal_discount - generate test cases on applying seasonal discount during holiday season
def test_apply_seasonal_discount_holiday(mock_cart):
    cart = mock_cart(items=[{'item_id': 4, 'price': 300, 'quantity': 1, 'category': 'toys'}], user_type='regular')
    discount = Discount(discount_rate=0.2)
    total_price = discount.apply_seasonal_discount(cart, season='holiday', seasonal_discount_rate=0.2)
    assert total_price == 240.0

# happy_path - apply_category_discount - generate test cases on applying category discount for clothing items
def test_apply_category_discount_happy_path(mock_cart):
    cart = mock_cart(items=[{'item_id': 5, 'price': 80, 'quantity': 1, 'category': 'clothing'}], user_type='regular')
    discount = Discount(discount_rate=0.15)
    discount.apply_category_discount(cart, category='clothing', category_discount_rate=0.15)
    assert cart.items[0]['price'] == 68.0

# happy_path - apply_loyalty_discount - generate test cases on applying loyalty discount for loyal user
def test_apply_loyalty_discount_happy_path(mock_cart):
    cart = mock_cart(items=[{'item_id': 6, 'price': 400, 'quantity': 1, 'category': 'furniture'}], user_type='loyal')
    discount = Discount(discount_rate=0.1)
    total_price = discount.apply_loyalty_discount(cart, loyalty_years=3, loyalty_discount_rate=0.1)
    assert total_price == 360.0

# happy_path - apply_flash_sale_discount - generate test cases on applying flash sale discount for sale items
def test_apply_flash_sale_discount_happy_path(mock_cart):
    cart = mock_cart(items=[{'item_id': 7, 'price': 150, 'quantity': 1, 'category': 'electronics'}], user_type='regular')
    discount = Discount(discount_rate=0.2)
    discount.apply_flash_sale_discount(cart, flash_sale_rate=0.2, items_on_sale=[7])
    assert cart.items[0]['price'] == 120.0

# edge_case - apply_discount - generate test cases on applying discount when total price is below minimum purchase amount
def test_apply_discount_edge_case_below_minimum(mock_cart):
    cart = mock_cart(items=[{'item_id': 8, 'price': 50, 'quantity': 1, 'category': 'clothing'}], user_type='regular')
    discount = Discount(discount_rate=0.1, min_purchase_amount=100)
    total_price = discount.apply_discount(cart)
    assert total_price == 50.0

# edge_case - apply_discount - generate test cases on applying discount with negative discount rate
def test_apply_discount_edge_case_negative_rate(mock_cart):
    cart = mock_cart(items=[{'item_id': 9, 'price': 100, 'quantity': 1, 'category': 'clothing'}], user_type='regular')
    discount = Discount(discount_rate=-0.05)
    total_price = discount.apply_discount(cart)
    assert total_price == 95.0

# edge_case - apply_bulk_discount - generate test cases on applying bulk discount with zero quantity
def test_apply_bulk_discount_edge_case_zero_quantity(mock_cart):
    cart = mock_cart(items=[{'item_id': 10, 'price': 70, 'quantity': 0, 'category': 'clothing'}], user_type='regular')
    discount = Discount(discount_rate=0.1)
    discount.apply_bulk_discount(cart, bulk_quantity=5, bulk_discount_rate=0.1)
    assert cart.items[0]['quantity'] == 0

# edge_case - apply_seasonal_discount - generate test cases on applying seasonal discount with invalid season
def test_apply_seasonal_discount_edge_case_invalid_season(mock_cart):
    cart = mock_cart(items=[{'item_id': 11, 'price': 200, 'quantity': 1, 'category': 'toys'}], user_type='regular')
    discount = Discount(discount_rate=0.2)
    total_price = discount.apply_seasonal_discount(cart, season='winter', seasonal_discount_rate=0.3)
    assert total_price == 200.0

# edge_case - apply_category_discount - generate test cases on applying category discount for non-existent category
def test_apply_category_discount_edge_case_no_category(mock_cart):
    cart = mock_cart(items=[{'item_id': 12, 'price': 90, 'quantity': 1, 'category': 'home'}], user_type='regular')
    discount = Discount(discount_rate=0.2)
    discount.apply_category_discount(cart, category='electronics', category_discount_rate=0.2)
    assert cart.items[0]['price'] == 90.0

# edge_case - apply_loyalty_discount - generate test cases on applying loyalty discount for user with insufficient loyalty years
def test_apply_loyalty_discount_edge_case_insufficient_years(mock_cart):
    cart = mock_cart(items=[{'item_id': 13, 'price': 500, 'quantity': 1, 'category': 'furniture'}], user_type='loyal')
    discount = Discount(discount_rate=0.1)
    total_price = discount.apply_loyalty_discount(cart, loyalty_years=1, loyalty_discount_rate=0.1)
    assert total_price == 500.0

# edge_case - apply_flash_sale_discount - generate test cases on applying flash sale discount for items not on sale
def test_apply_flash_sale_discount_edge_case_not_on_sale(mock_cart):
    cart = mock_cart(items=[{'item_id': 12, 'price': 300, 'quantity': 1, 'category': 'electronics'}], user_type='regular')
    discount = Discount(discount_rate=0.25)
    discount.apply_flash_sale_discount(cart, flash_sale_rate=0.25, items_on_sale=[])  
    assert cart.items[0]['price'] == 300.0

