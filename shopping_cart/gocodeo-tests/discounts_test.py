# happy_path - method_name
apply_discount

# happy_path - test_function
def test_apply_discount(cart_mock, discount):
    cart_mock.user_type = 'regular'
    assert discount.apply_discount(cart_mock) == 1100.0

# happy_path - method_name
apply_bulk_discount

# happy_path - test_function
def test_apply_bulk_discount(cart_mock, discount):
    cart_mock.items[0]['quantity'] = 10
    discount.apply_bulk_discount(cart_mock, 5, 0.2)
    assert cart_mock.items[0]['price'] == 80.0

# happy_path - method_name
apply_seasonal_discount

# happy_path - test_function
def test_apply_seasonal_discount(cart_mock, discount):
    assert discount.apply_seasonal_discount(cart_mock, 'holiday', 0.2) == 800.0

# happy_path - method_name
apply_category_discount

# happy_path - test_function
def test_apply_category_discount(cart_mock, discount):
    discount.apply_category_discount(cart_mock, 'books', 0.1)
    assert cart_mock.items[0]['price'] == 90.0

# happy_path - method_name
apply_loyalty_discount

# happy_path - test_function
def test_apply_loyalty_discount(cart_mock, discount):
    cart_mock.user_type = 'loyal'
    assert discount.apply_loyalty_discount(cart_mock, 3, 0.15) == 850.0

# happy_path - method_name
apply_flash_sale_discount

# happy_path - test_function
def test_apply_flash_sale_discount(cart_mock, discount):
    discount.apply_flash_sale_discount(cart_mock, 0.3, [1])
    assert cart_mock.items[0]['price'] == 70.0

# edge_case - method_name
apply_discount

# edge_case - test_function
def test_apply_discount_below_minimum(cart_mock, discount):
    cart_mock.calculate_total_price.return_value = 400
    assert discount.apply_discount(cart_mock) == 400.0

# edge_case - method_name
apply_bulk_discount

# edge_case - test_function
def test_apply_bulk_discount_no_items(cart_mock, discount):
    cart_mock.items = []
    discount.apply_bulk_discount(cart_mock, 5, 0.2)
    assert cart_mock.items == []

# edge_case - method_name
apply_seasonal_discount

# edge_case - test_function
def test_apply_seasonal_discount_invalid_season(cart_mock, discount):
    assert discount.apply_seasonal_discount(cart_mock, 'winter', 0.2) == 1000.0

# edge_case - method_name
apply_category_discount

# edge_case - test_function
def test_apply_category_discount_no_matching_category(cart_mock, discount):
    discount.apply_category_discount(cart_mock, 'clothing', 0.1)
    assert cart_mock.items[0]['price'] == 100

# edge_case - method_name
apply_loyalty_discount

# edge_case - test_function
def test_apply_loyalty_discount_not_loyal(cart_mock, discount):
    cart_mock.user_type = 'regular'
    assert discount.apply_loyalty_discount(cart_mock, 3, 0.15) == 1000.0

# edge_case - method_name
apply_flash_sale_discount

# edge_case - test_function
def test_apply_flash_sale_discount_no_items_on_sale(cart_mock, discount):
    discount.apply_flash_sale_discount(cart_mock, 0.3, [])
    assert cart_mock.items[0]['price'] == 100

