import pytest
from unittest.mock import patch, MagicMock
from shopping_cart.payments import PaymentProcessor, PaymentMethod, process_payments, make_payments, add_payment_to_cart, run_multiple_payments

@pytest.fixture
def cart():
    return MagicMock(payment_status='')

@pytest.fixture
def payment_methods():
    return [
        PaymentMethod(name='Credit Card', processing_time=0.2),
        PaymentMethod(name='PayPal', processing_time=0.3)
    ]

@pytest.fixture
def mock_payment_method():
    with patch('shopping_cart.payments.PaymentMethod') as mock:
        yield mock

@pytest.fixture
def mock_payment_processor():
    with patch('shopping_cart.payments.PaymentProcessor') as mock:
        yield mock

@pytest.fixture
def mock_time_sleep():
    with patch('time.sleep') as mock:
        yield mock

@pytest.fixture
def mock_process_payment():
    with patch.object(PaymentMethod, 'process_payment') as mock:
        yield mock

@pytest.fixture
def mock_thread_start():
    with patch.object(PaymentProcessor, 'start') as mock:
        yield mock

@pytest.fixture
def mock_thread_join():
    with patch.object(PaymentProcessor, 'join') as mock:
        yield mock

# happy path - process_payments - Test that process_payments starts a thread for each payment method and processes payments
def test_process_payments_starts_threads(cart, payment_methods, mock_thread_start, mock_thread_join):
    process_payments(cart, payment_methods)
    assert mock_thread_start.call_count == len(payment_methods)
    assert mock_thread_join.call_count == len(payment_methods)
    assert cart.payment_status == 'PayPal Payment Processed'


# happy path - make_payments - Test that make_payments processes all payments in the list
def test_make_payments_processes_all(cart, payment_methods, mock_thread_start, mock_thread_join):
    make_payments(cart, payment_methods)
    assert cart.payment_status == 'PayPal Payment Processed'


# happy path - add_payment_to_cart - Test that add_payment_to_cart processes a single payment
def test_add_payment_to_cart_single_payment(cart, mock_payment_method, mock_thread_start, mock_thread_join):
    payment_method = PaymentMethod(name='Credit Card', processing_time=0.2)
    add_payment_to_cart(cart, payment_method)
    assert cart.payment_status == 'Credit Card Payment Processed'


# happy path - run_multiple_payments - Test that run_multiple_payments processes multiple payments
def test_run_multiple_payments_processes_multiple(cart, mock_thread_start, mock_thread_join):
    run_multiple_payments(cart)
    assert cart.payment_status == 'Method 4 Payment Processed'


# happy path - run - Test that PaymentProcessor run method processes payment
def test_payment_processor_run_processes_payment(cart, mock_payment_method, mock_time_sleep):
    payment_method = PaymentMethod(name='Credit Card', processing_time=0.2)
    processor = PaymentProcessor(cart, payment_method)
    processor.run()
    assert cart.payment_status == 'Credit Card Payment Processed'


# edge case - process_payments - Test process_payments with an empty payment_methods list
def test_process_payments_empty_methods(cart, mock_thread_start, mock_thread_join):
    process_payments(cart, [])
    assert cart.payment_status == ''
    assert mock_thread_start.call_count == 0
    assert mock_thread_join.call_count == 0


# edge case - make_payments - Test make_payments with a cart already having a payment status
def test_make_payments_with_existing_status(cart, mock_thread_start, mock_thread_join):
    cart.payment_status = 'Existing Payment'
    payment_methods = [PaymentMethod(name='Credit Card', processing_time=0.2)]
    make_payments(cart, payment_methods)
    assert cart.payment_status == 'Credit Card Payment Processed'


# edge case - add_payment_to_cart - Test add_payment_to_cart with a slow processing payment method
def test_add_payment_to_cart_slow_method(cart, mock_payment_method, mock_time_sleep):
    payment_method = PaymentMethod(name='Slow Method', processing_time=5)
    add_payment_to_cart(cart, payment_method)
    assert cart.payment_status == 'Slow Method Payment Processed'


# edge case - run_multiple_payments - Test run_multiple_payments with no payment methods
def test_run_multiple_payments_no_methods(cart, mock_thread_start, mock_thread_join):
    run_multiple_payments(cart)
    assert cart.payment_status == 'Method 4 Payment Processed'


# edge case - run - Test PaymentProcessor run with a None cart
def test_payment_processor_run_none_cart(mock_payment_method, mock_time_sleep):
    payment_method = PaymentMethod(name='Credit Card', processing_time=0.2)
    processor = PaymentProcessor(None, payment_method)
    processor.run()
    assert processor.cart is None


# happy path - process_payments - Test that process_payments successfully processes payments for multiple methods
def test_process_payments_multiple_methods(cart, mock_thread_start, mock_thread_join):
    payment_methods = [
        PaymentMethod(name='Credit Card', processing_time=0.2),
        PaymentMethod(name='Debit Card', processing_time=0.3),
        PaymentMethod(name='PayPal', processing_time=0.4)
    ]
    process_payments(cart, payment_methods)
    assert cart.payment_status == 'PayPal Payment Processed'


# happy path - make_payments - Test that make_payments handles a single payment method correctly
def test_make_payments_single_method(cart, mock_thread_start, mock_thread_join):
    payment_methods = [PaymentMethod(name='Credit Card', processing_time=0.2)]
    make_payments(cart, payment_methods)
    assert cart.payment_status == 'Credit Card Payment Processed'


# happy path - add_payment_to_cart - Test that add_payment_to_cart can handle multiple sequential additions
def test_add_payment_to_cart_multiple_sequential(cart, mock_payment_method, mock_thread_start, mock_thread_join):
    payment_method = PaymentMethod(name='Credit Card', processing_time=0.2)
    add_payment_to_cart(cart, payment_method)
    assert cart.payment_status == 'Credit Card Payment Processed'
    add_payment_to_cart(cart, payment_method)
    assert cart.payment_status == 'Credit Card Payment Processed'


# happy path - run_multiple_payments - Test that run_multiple_payments processes all payment methods in sequence
def test_run_multiple_payments_sequence(cart, mock_thread_start, mock_thread_join):
    run_multiple_payments(cart)
    assert cart.payment_status == 'Method 4 Payment Processed'


# happy path - run - Test that PaymentProcessor's run method completes without error
def test_payment_processor_run_no_error(cart, mock_payment_method, mock_time_sleep):
    payment_method = PaymentMethod(name='Credit Card', processing_time=0.2)
    processor = PaymentProcessor(cart, payment_method)
    processor.run()
    assert cart.payment_status == 'Credit Card Payment Processed'


