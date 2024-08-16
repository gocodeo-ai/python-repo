# happy_path - process_payments - Test processing of payments using multiple payment methods
def test_process_payments(process_payments_fixture):
    process_payments_fixture(cart, payment_methods)
    for method in payment_methods:
        method.process_payment.assert_called_once_with(cart)

# happy_path - add_payment_to_cart - Test adding a payment to cart and processing it
def test_add_payment_to_cart(cart, payment_method):
    add_payment_to_cart(cart, payment_method)
    payment_method.process_payment.assert_called_once_with(cart)

# happy_path - apply_promotions - Test applying Spring Sale promotion to cart items
def test_apply_promotions_spring(cart, promotions):
    apply_promotions(cart, promotions)
    for item in cart.items:
        assert item.price == 90.0

# edge_case - process_payments - Test processing payments with an empty cart
def test_process_payments_empty_cart():
    empty_cart = Mock()
    empty_cart.items = []
    payment_methods = [Mock(process_payment=Mock())]
    process_payments(empty_cart, payment_methods)
    for method in payment_methods:
        method.process_payment.assert_called_once_with(empty_cart)

# edge_case - apply_promotions - Test applying promotions when no items in cart
def test_apply_promotions_no_items(cart, promotions):
    cart.items = []
    apply_promotions(cart, promotions)
    assert all(item.price == 100 for item in cart.items)

