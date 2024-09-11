import pytest
from unittest.mock import patch, Mock
from shopping_cart.discounts import Discount

@pytest.fixture
def mock_cart():
    with patch('shopping_cart.discounts.Cart') as MockCart:
        mock_cart_instance = MockCart.return_value
        mock_cart_instance.calculate_total_price.return_value = 150
        mock_cart_instance.user_type = 'regular'
        mock_cart_instance.items = [{'category': 'clothing', 'price': 50}, {'category': 'clothing', 'price': 100}]
        yield mock_cart_instance

@pytest.fixture
def mock_discount():
    with patch('shopping_cart.discounts.Discount') as MockDiscount:
        mock_discount_instance = MockDiscount.return_value
        mock_discount_instance.apply_discount.return_value = 165.0
        mock_discount_instance.apply_bulk_discount.return_value = None
        mock_discount_instance.apply_seasonal_discount.return_value = 210.0
        mock_discount_instance.apply_category_discount.return_value = None
        mock_discount_instance.apply_loyalty_discount.return_value = 400
        mock_discount_instance.apply_flash_sale_discount.return_value = None
        yield mock_discount_instance

@pytest.fixture
def mock_cart_for_bulk_discount():
    with patch('shopping_cart.discounts.Cart') as MockCart:
        mock_cart_instance = MockCart.return_value
        mock_cart_instance.items = [{'quantity': 10, 'price': 100}, {'quantity': 5, 'price': 50}]
        yield mock_cart_instance

@pytest.fixture
def mock_cart_for_seasonal_discount():
    with patch('shopping_cart.discounts.Cart') as MockCart:
        mock_cart_instance = MockCart.return_value
        mock_cart_instance.calculate_total_price.return_value = 300
        yield mock_cart_instance

@pytest.fixture
def mock_cart_for_category_discount():
    with patch('shopping_cart.discounts.Cart') as MockCart:
        mock_cart_instance = MockCart.return_value
        mock_cart_instance.items = [{'category': 'electronics', 'price': 200}, {'category': 'clothing', 'price': 100}]
        yield mock_cart_instance

@pytest.fixture
def mock_cart_for_loyalty_discount():
    with patch('shopping_cart.discounts.Cart') as MockCart:
        mock_cart_instance = MockCart.return_value
        mock_cart_instance.calculate_total_price.return_value = 400
        mock_cart_instance.user_type = 'loyal'
        yield mock_cart_instance

@pytest.fixture
def mock_cart_for_flash_sale_discount():
    with patch('shopping_cart.discounts.Cart') as MockCart:
        mock_cart_instance = MockCart.return_value
        mock_cart_instance.items = [{'item_id': 1, 'price': 100}, {'item_id': 2, 'price': 200}]
        yield mock_cart_instance

# happy_path - test_apply_discount_regular_user - Test that discount is applied correctly when total price exceeds minimum purchase amount for regular users.
def test_apply_discount_regular_user(mock_cart, mock_discount):
    discount = Discount(discount_rate=0.1, min_purchase_amount=100)
    result = discount.apply_discount(mock_cart)
    assert result == 165.0

# happy_path - test_apply_discount_premium_user_with_electronics - Test that discount is applied correctly when total price exceeds minimum purchase amount for premium users with electronics.
def test_apply_discount_premium_user_with_electronics():
    with patch('shopping_cart.discounts.Cart') as MockCart:
        mock_cart = MockCart()
        mock_cart.calculate_total_price.return_value = 200
        mock_cart.user_type = 'premium'
        mock_cart.items = [{'category': 'electronics', 'price': 200}]
        discount = Discount(discount_rate=0.1, min_purchase_amount=100)
        result = discount.apply_discount(mock_cart)
        assert result == 230.0

# happy_path - test_apply_bulk_discount - Test that bulk discount is applied to items with quantity exceeding bulk quantity.
def test_apply_bulk_discount(mock_cart_for_bulk_discount, mock_discount):
    discount = Discount(discount_rate=0.1)
    discount.apply_bulk_discount(mock_cart_for_bulk_discount, bulk_quantity=8, bulk_discount_rate=0.2)
    assert mock_cart_for_bulk_discount.items[0]['price'] == 80.0
    assert mock_cart_for_bulk_discount.items[1]['price'] == 50

# happy_path - test_apply_seasonal_discount_holiday - Test that seasonal discount is applied during holiday season.
def test_apply_seasonal_discount_holiday(mock_cart_for_seasonal_discount, mock_discount):
    discount = Discount(discount_rate=0.1)
    result = discount.apply_seasonal_discount(mock_cart_for_seasonal_discount, season='holiday', seasonal_discount_rate=0.3)
    assert result == 210.0

# happy_path - test_apply_category_discount_electronics - Test that category discount is applied to electronics.
def test_apply_category_discount_electronics(mock_cart_for_category_discount, mock_discount):
    discount = Discount(discount_rate=0.1)
    discount.apply_category_discount(mock_cart_for_category_discount, category='electronics', category_discount_rate=0.15)
    assert mock_cart_for_category_discount.items[0]['price'] == 170.0
    assert mock_cart_for_category_discount.items[1]['price'] == 100

# edge_case - test_apply_discount_below_min_purchase - Test that no discount is applied when total price is below minimum purchase amount.
def test_apply_discount_below_min_purchase():
    with patch('shopping_cart.discounts.Cart') as MockCart:
        mock_cart = MockCart()
        mock_cart.calculate_total_price.return_value = 50
        mock_cart.user_type = 'regular'
        mock_cart.items = [{'category': 'clothing', 'price': 50}]
        discount = Discount(discount_rate=0.1, min_purchase_amount=100)
        result = discount.apply_discount(mock_cart)
        assert result == 50

# edge_case - test_apply_bulk_discount_below_quantity - Test that no bulk discount is applied to items with quantity below bulk quantity.
def test_apply_bulk_discount_below_quantity():
    with patch('shopping_cart.discounts.Cart') as MockCart:
        mock_cart = MockCart()
        mock_cart.items = [{'quantity': 5, 'price': 100}]
        discount = Discount(discount_rate=0.1)
        discount.apply_bulk_discount(mock_cart, bulk_quantity=8, bulk_discount_rate=0.2)
        assert mock_cart.items[0]['price'] == 100

# edge_case - test_apply_seasonal_discount_non_holiday - Test that seasonal discount is not applied during non-holiday season.
def test_apply_seasonal_discount_non_holiday(mock_cart_for_seasonal_discount, mock_discount):
    discount = Discount(discount_rate=0.1)
    result = discount.apply_seasonal_discount(mock_cart_for_seasonal_discount, season='spring', seasonal_discount_rate=0.3)
    assert result == 300

# edge_case - test_apply_loyalty_discount_below_years - Test that loyalty discount is not applied for users with less than 3 years of loyalty.
def test_apply_loyalty_discount_below_years(mock_cart_for_loyalty_discount, mock_discount):
    discount = Discount(discount_rate=0.1)
    result = discount.apply_loyalty_discount(mock_cart_for_loyalty_discount, loyalty_years=2, loyalty_discount_rate=0.1)
    assert result == 400

# edge_case - test_apply_flash_sale_discount_no_items_on_sale - Test that flash sale discount is not applied to items not on sale.
def test_apply_flash_sale_discount_no_items_on_sale(mock_cart_for_flash_sale_discount, mock_discount):
    discount = Discount(discount_rate=0.1)
    discount.apply_flash_sale_discount(mock_cart_for_flash_sale_discount, flash_sale_rate=0.2, items_on_sale=[3, 4])
    assert mock_cart_for_flash_sale_discount.items[0]['price'] == 100
    assert mock_cart_for_flash_sale_discount.items[1]['price'] == 200

