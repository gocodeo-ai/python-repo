import pytest
from unittest.mock import patch, Mock
from .cart import Cart, Item
from .database import Database
from .discounts import DiscountManager
from .payments import PaymentProcessor
from .utils import Utils


@pytest.fixture
def cart_fixture():
    with patch('path.to.cart.Database') as MockDatabase, \
         patch('path.to.cart.DiscountManager') as MockDiscountManager, \
         patch('path.to.cart.PaymentProcessor') as MockPaymentProcessor, \
         patch('path.to.cart.Utils') as MockUtils:

        # Mocking the database
        mock_db_instance = MockDatabase.return_value
        mock_db_instance.get_item_price.return_value = 10.0

        # Mocking the discount manager
        mock_discount_instance = MockDiscountManager.return_value
        mock_discount_instance.apply_discount.return_value = 2.0

        # Mocking the payment processor
        mock_payment_instance = MockPaymentProcessor.return_value
        mock_payment_instance.process_payment.return_value = {'status': 'success', 'order_id': 12345}

        # Mocking the utils
        mock_utils_instance = MockUtils.return_value
        mock_utils_instance.calculate_total_price.return_value = 20.0

        cart = Cart()
        yield cart, mock_db_instance, mock_discount_instance, mock_payment_instance, mock_utils_instance

# happy_path - add_item_to_cart - Generate test cases on adding an item to the cart successfully
def test_add_item_to_cart(cart_fixture):
    cart, mock_db, mock_discount, mock_payment, mock_utils = cart_fixture
    cart.add_item_to_cart(item_id=1, quantity=2)
    assert cart.cart_items == [{'item_id': 1, 'quantity': 2}]
    assert cart.total_price == 20.0

# happy_path - remove_item_from_cart - Generate test cases on removing an item from the cart successfully
def test_remove_item_from_cart(cart_fixture):
    cart, mock_db, mock_discount, mock_payment, mock_utils = cart_fixture
    cart.add_item_to_cart(item_id=1, quantity=2)
    cart.remove_item_from_cart(item_id=1)
    assert cart.cart_items == []
    assert cart.total_price == 0.0

# happy_path - apply_discount_code - Generate test cases on applying a discount code successfully
def test_apply_discount_code(cart_fixture):
    cart, mock_db, mock_discount, mock_payment, mock_utils = cart_fixture
    cart.add_item_to_cart(item_id=1, quantity=2)
    cart.apply_discount_code(code='SAVE10')
    assert cart.discount_applied == True
    assert cart.total_price == 18.0

# happy_path - checkout - Generate test cases on successful checkout process
def test_checkout(cart_fixture):
    cart, mock_db, mock_discount, mock_payment, mock_utils = cart_fixture
    cart.add_item_to_cart(item_id=1, quantity=2)
    order_status = cart.checkout(payment_method='credit_card')
    assert order_status['order_status'] == 'success'
    assert order_status['order_id'] == 12345

# happy_path - view_cart - Generate test cases on viewing cart contents
def test_view_cart(cart_fixture):
    cart, mock_db, mock_discount, mock_payment, mock_utils = cart_fixture
    cart.add_item_to_cart(item_id=1, quantity=2)
    contents = cart.view_cart()
    assert contents == {'cart_items': [{'item_id': 1, 'quantity': 2}], 'total_price': 20.0}

# edge_case - add_item_to_cart - Generate test cases on adding an item with zero quantity
def test_add_item_zero_quantity(cart_fixture):
    cart, mock_db, mock_discount, mock_payment, mock_utils = cart_fixture
    with pytest.raises(ValueError, match='Quantity must be greater than zero'):
        cart.add_item_to_cart(item_id=1, quantity=0)

# edge_case - remove_item_from_cart - Generate test cases on removing an item not in the cart
def test_remove_item_not_in_cart(cart_fixture):
    cart, mock_db, mock_discount, mock_payment, mock_utils = cart_fixture
    with pytest.raises(ValueError, match='Item not found in cart'):
        cart.remove_item_from_cart(item_id=99)

# edge_case - apply_discount_code - Generate test cases on applying an invalid discount code
def test_apply_invalid_discount_code(cart_fixture):
    cart, mock_db, mock_discount, mock_payment, mock_utils = cart_fixture
    cart.add_item_to_cart(item_id=1, quantity=2)
    result = cart.apply_discount_code(code='INVALIDCODE')
    assert result['discount_applied'] == False
    assert result['error'] == 'Invalid discount code'

# edge_case - checkout - Generate test cases on checkout with empty cart
def test_checkout_empty_cart(cart_fixture):
    cart, mock_db, mock_discount, mock_payment, mock_utils = cart_fixture
    with pytest.raises(ValueError, match='Cart is empty'):
        cart.checkout(payment_method='credit_card')

# edge_case - view_cart - Generate test cases on viewing cart when cart is empty
def test_view_empty_cart(cart_fixture):
    cart, mock_db, mock_discount, mock_payment, mock_utils = cart_fixture
    contents = cart.view_cart()
    assert contents == {'cart_items': [], 'total_price': 0.0}

