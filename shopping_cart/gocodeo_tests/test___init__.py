import pytest
from unittest.mock import patch, MagicMock
from .cart import Cart, Item
from .database import Database
from .discounts import DiscountManager
from .payments import PaymentProcessor
from .utils import Utils



    patcher_db.stop()
    patcher_discount.stop()
    patcher_payment.stop()
    patcher_utils.stop()

# happy_path - test_add_item_to_cart - Test that a cart can successfully add an item
def test_add_item_to_cart(setup_mocks):
    cart = Cart(cart_id=1)
    item = Item(item_id=101, quantity=2)
    setup_mocks['db'].get_cart.return_value = cart
    setup_mocks['db'].get_item.return_value = item
    cart.add_item(item)
    assert cart.items == [{'item_id': 101, 'quantity': 2}]

# happy_path - test_remove_item_from_cart - Test that an item can be removed from the cart
def test_remove_item_from_cart(setup_mocks):
    cart = Cart(cart_id=1)
    item = Item(item_id=101, quantity=1)
    cart.items = [{'item_id': 101, 'quantity': 1}]
    cart.remove_item(item)
    assert cart.items == []

# happy_path - test_apply_discount_to_cart - Test that a discount can be applied to the cart
def test_apply_discount_to_cart(setup_mocks):
    cart = Cart(cart_id=1)
    setup_mocks['discount_manager'].apply_discount.return_value = True
    result = cart.apply_discount('SUMMER21')
    assert result is True

# happy_path - test_process_payment - Test that payment can be processed for a cart
def test_process_payment(setup_mocks):
    cart = Cart(cart_id=1)
    setup_mocks['payment_processor'].process_payment.return_value = 'completed'
    status = cart.process_payment('credit_card')
    assert status == 'completed'

# happy_path - test_calculate_cart_total - Test that the cart total is calculated correctly
def test_calculate_cart_total(setup_mocks):
    cart = Cart(cart_id=1)
    setup_mocks['utils'].calculate_total.return_value = 150.0
    total = cart.calculate_total()
    assert total == 150.0

# happy_path - test_apply_discount_to_cart - Test that a discount can be applied to a cart with multiple items.
def test_apply_discount_to_cart_with_multiple_items(setup_mocks):
    cart = Cart(cart_id=1)
    setup_mocks['discount_manager'].apply_discount.return_value = True
    setup_mocks['utils'].calculate_total.return_value = 80
    result = cart.apply_discount('SUMMER20')
    total = cart.calculate_total()
    assert result is True
    assert total == 80

# happy_path - test_process_payment_for_cart - Test that payment can be processed for a cart with valid payment details.
def test_process_payment_for_cart(setup_mocks):
    cart = Cart(cart_id=1)
    setup_mocks['payment_processor'].process_payment.return_value = {'status': 'completed', 'transaction_id': 'abc123'}
    result = cart.process_payment('credit_card', {'number': '1234567890123456', 'expiry': '12/23'})
    assert result['status'] == 'completed'
    assert result['transaction_id'] == 'abc123'

# happy_path - test_remove_item_from_cart - Test that an item can be removed from the cart.
def test_remove_item_from_cart_by_name(setup_mocks):
    cart = Cart(cart_id=1)
    cart.items = [{'item_id': 101, 'quantity': 1, 'name': 'banana'}]
    cart.remove_item_by_name('banana')
    assert cart.items == []

# happy_path - test_clear_cart - Test that the cart can be cleared of all items.
def test_clear_cart(setup_mocks):
    cart = Cart(cart_id=1)
    cart.items = [{'item_id': 101, 'quantity': 1}, {'item_id': 102, 'quantity': 1}]
    cart.clear()
    assert cart.items == []

# edge_case - test_add_zero_quantity_item - Test that adding an item with zero quantity does not alter the cart
def test_add_zero_quantity_item(setup_mocks):
    cart = Cart(cart_id=1)
    item = Item(item_id=101, quantity=0)
    cart.add_item(item)
    assert cart.items == []

# edge_case - test_remove_nonexistent_item - Test that removing an item not in the cart does not cause errors
def test_remove_nonexistent_item(setup_mocks):
    cart = Cart(cart_id=1)
    item = Item(item_id=999)
    cart.remove_item(item)
    assert cart.items == []

# edge_case - test_apply_invalid_discount - Test that applying an invalid discount code does not alter the cart
def test_apply_invalid_discount(setup_mocks):
    cart = Cart(cart_id=1)
    setup_mocks['discount_manager'].apply_discount.return_value = False
    result = cart.apply_discount('INVALID')
    assert result is False

# edge_case - test_process_payment_invalid_method - Test that processing payment with an invalid method fails
def test_process_payment_invalid_method(setup_mocks):
    cart = Cart(cart_id=1)
    setup_mocks['payment_processor'].process_payment.return_value = 'failed'
    status = cart.process_payment('invalid_method')
    assert status == 'failed'

# edge_case - test_calculate_total_empty_cart - Test that calculating the total for an empty cart returns zero
def test_calculate_total_empty_cart(setup_mocks):
    cart = Cart(cart_id=2)
    setup_mocks['utils'].calculate_total.return_value = 0.0
    total = cart.calculate_total()
    assert total == 0.0

# edge_case - test_add_zero_quantity_item - Test that adding an item with zero quantity does not affect the cart.
def test_add_zero_quantity_item_with_name(setup_mocks):
    cart = Cart(cart_id=1)
    cart.items = [{'item_id': 201, 'name': 'orange', 'quantity': 5}]
    item = Item(item_id=202, name='orange', quantity=0)
    cart.add_item(item)
    assert cart.items == [{'item_id': 201, 'name': 'orange', 'quantity': 5}]

# edge_case - test_apply_invalid_discount - Test that applying an invalid discount code does not alter the cart total price.
def test_apply_invalid_discount_with_total(setup_mocks):
    cart = Cart(cart_id=1)
    setup_mocks['discount_manager'].apply_discount.return_value = False
    setup_mocks['utils'].calculate_total.return_value = 100
    result = cart.apply_discount('INVALID')
    total = cart.calculate_total()
    assert result is False
    assert total == 100

# edge_case - test_process_payment_with_expired_card - Test that processing payment with expired card details fails.
def test_process_payment_with_expired_card(setup_mocks):
    cart = Cart(cart_id=1)
    setup_mocks['payment_processor'].process_payment.return_value = {'status': 'failed', 'error_message': 'Card expired'}
    result = cart.process_payment('credit_card', {'number': '1234567890123456', 'expiry': '01/20'})
    assert result['status'] == 'failed'
    assert result['error_message'] == 'Card expired'

# edge_case - test_remove_non_existent_item - Test that removing an item not in the cart does not change the cart.
def test_remove_non_existent_item(setup_mocks):
    cart = Cart(cart_id=1)
    cart.items = [{'item_id': 201, 'quantity': 5, 'name': 'apple'}]
    cart.remove_item_by_name('grape')
    assert cart.items == [{'item_id': 201, 'quantity': 5, 'name': 'apple'}]

# edge_case - test_clear_empty_cart - Test that clearing an already empty cart remains unchanged.
def test_clear_empty_cart(setup_mocks):
    cart = Cart(cart_id=2)
    cart.items = []
    cart.clear()
    assert cart.items == []

