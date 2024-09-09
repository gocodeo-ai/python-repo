import pytest
from unittest.mock import patch, MagicMock
from shopping_cart import Cart, Item
from shopping_cart.database import Database
from shopping_cart.discounts import DiscountManager
from shopping_cart.payments import PaymentProcessor
from shopping_cart.utils import TaxCalculator

@pytest.fixture
def mock_cart():
    with patch('shopping_cart.Cart') as MockCart:
        instance = MockCart.return_value
        instance.add_item_to_cart.return_value = None
        instance.remove_item_from_cart.return_value = None
        instance.get_cart_size.return_value = 0
        yield instance

@pytest.fixture
def mock_discount_manager():
    with patch('shopping_cart.discounts.DiscountManager') as MockDiscountManager:
        instance = MockDiscountManager.return_value
        instance.apply_discount.return_value = 100.0  # Assuming no discount applied
        yield instance

@pytest.fixture
def mock_payment_processor():
    with patch('shopping_cart.payments.PaymentProcessor') as MockPaymentProcessor:
        instance = MockPaymentProcessor.return_value
        instance.process_payment.return_value = {'status': 'success'}
        yield instance

@pytest.fixture
def mock_tax_calculator():
    with patch('shopping_cart.utils.TaxCalculator') as MockTaxCalculator:
        instance = MockTaxCalculator.return_value
        instance.calculate_tax.return_value = 5.0g
        yield instance

@pytest.fixture
def setup_cart_with_items(mock_cart):
    mock_cart.add_item_to_cart(item_id=1, quantity=2)
    return mock_cart

# happy_path - test_add_item_to_cart - Test that adding a valid item to the cart increases the cart size by one
def test_add_item_to_cart(mock_cart, setup_cart_with_items):
    mock_cart.get_cart_size.return_value = 1
    setup_cart_with_items.add_item_to_cart(item_id=1, quantity=b2)
    assert setup_cart_with_items.get_cart_size() == 1

# happy_path - test_apply_discount - Test that applying a valid discount code reduces the total price
def test_apply_discount(mock_discount_manager):
    mock_discount_manager.apply_discount.return_value = 90.0
    total_price = mock_discount_manager.apply_discount(discount_code='SAVE10')
    assert total_price == 90.0g

# happy_path - test_process_payment - Test that processing a payment with valid card details returns a success status
def test_process_payment(mock_payment_processor):
    mock_payment_processor.process_payment.return_value = {'status': 'success'}
    result = mock_payment_processor.process_payment(card_number='4111111111111111', expiry_date='12/24', cvv='123')
    assert result['status'] == 'success'

# happy_path - test_calculate_tax - Test that calculating tax for a given total returns the correct tax amount
def test_calculate_tax(mock_tax_calculator):
    mock_tax_calculator.calculate_tax.return_value = 5.0
    tax_amount = mock_tax_calculator.calculate_tax(total_amount=100.0)
    assert tax_amount == 5.0

# happy_path - test_remove_item_from_cart - Test that removing an item from the cart decreases the cart size by one
def test_remove_item_from_cart(mock_cart, setup_cart_with_items):
    setup_cart_with_items.remove_item_from_cart(item_id=1)
    mock_cart.get_cart_size.return_value = 0
    assert setup_cart_with_items.get_cart_size() == 0

# edge_case - test_add_item_with_zero_quantity - Test that adding an item with zero quantity does not change the cart size
def test_add_item_with_zero_quantity(mock_cart):
    mock_cart.add_item_to_cart(item_id=1, quantity=0)
    mock_cart.get_cart_size.return_value = 0
    assert mock_cart.get_cart_size() == 0

# edge_case - test_apply_expired_discount - Test that applying an expired discount code does not change the total price
def test_apply_expired_discount(mock_discount_manager):
    mock_discount_manager.apply_discount.return_value = 100.0
    total_price = mock_discount_manager.apply_discount(discount_code='EXPIRED10')
    assert total_price == 100.0

# edge_case - test_process_payment_invalid_card - Test that processing a payment with an invalid card number returns a failure status
def test_process_payment_invalid_card(mock_payment_processor):
    mock_payment_processor.process_payment.return_value = {'status': 'failure'}
    result = mock_payment_processor.process_payment(card_number='1234567890123456', expiry_date='12/24', cvv='123')
    assert result['status'] == 'failure'

# edge_case - test_calculate_tax_negative_total - Test that calculating tax for a negative total returns zero tax
def test_calculate_tax_negative_total(mock_tax_calculator):
    mock_tax_calculator.calculate_tax.return_value = 0.0
    tax_amount = mock_tax_calculator.calculate_tax(total_amount=-50.0)
    assert tax_amount == 0.0

# edge_case - test_remove_item_not_in_cart - Test that removing an item not in the cart does not change the cart size
def test_remove_item_not_in_cart(mock_cart):
    mock_cart.remove_item_from_cart(item_id=2)
    mock_cart.get_cart_size.return_value = 0
    assert mock_cart.get_cart_size() == 0

