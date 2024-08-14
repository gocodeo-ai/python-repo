# happy path - apply_discount
def test_apply_discount_premium_electronics():
    cart = MockCart(user_type='premium', items=[{'category': 'electronics', 'price': 100}])
    cart.calculate_total_price = lambda: 100
    discount = Discount(discount_rate=0.1, min_purchase_amount=50)
    result = discount.apply_discount(cart)
    assert result == 115.0
    assert cart.total_price == 115.0

# happy path - apply_bulk_discount
def test_apply_bulk_discount_sufficient_quantity():
    cart = MockCart(items=[{'quantity': 10, 'price': 10}])
    discount = Discount(discount_rate=0.1)
    discount.apply_bulk_discount(cart, bulk_quantity=5, bulk_discount_rate=0.2)
    assert cart.items[0]['price'] == 8.0

# happy path - apply_seasonal_discount
def test_apply_seasonal_discount_holiday():
    cart = MockCart(items=[{'price': 100}])
    cart.calculate_total_price = lambda: 100
    discount = Discount(discount_rate=0.1)
    result = discount.apply_seasonal_discount(cart, season='holiday', seasonal_discount_rate=0.2)
    assert result == 80.0
    assert cart.total_price == 80.0

# happy path - apply_category_discount
def test_apply_category_discount_electronics():
    cart = MockCart(items=[{'category': 'electronics', 'price': 100}])
    discount = Discount(discount_rate=0.1)
    discount.apply_category_discount(cart, category='electronics', category_discount_rate=0.2)
    assert cart.items[0]['price'] == 80.0

# happy path - apply_loyalty_discount
def test_apply_loyalty_discount_loyal_user():
    cart = MockCart(user_type='loyal', items=[{'price': 100}])
    cart.calculate_total_price = lambda: 100
    discount = Discount(discount_rate=0.1)
    result = discount.apply_loyalty_discount(cart, loyalty_years=3, loyalty_discount_rate=0.15)
    assert result == 85.0
    assert cart.total_price == 85.0

# happy path - apply_flash_sale_discount
def test_apply_flash_sale_discount_items_on_sale():
    cart = MockCart(items=[{'item_id': 1, 'price': 100}, {'item_id': 2, 'price': 200}])
    discount = Discount(discount_rate=0.1)
    discount.apply_flash_sale_discount(cart, flash_sale_rate=0.3, items_on_sale=[1])
    assert cart.items[0]['price'] == 70.0
    assert cart.items[1]['price'] == 200.0

# edge case - apply_discount
def test_apply_discount_below_min_purchase():
    cart = MockCart(user_type='regular', items=[{'price': 40}])
    cart.calculate_total_price = lambda: 40
    discount = Discount(discount_rate=0.1, min_purchase_amount=50)
    result = discount.apply_discount(cart)
    assert result == 40.0
    assert cart.total_price == 40.0

# edge case - apply_bulk_discount
def test_apply_bulk_discount_insufficient_quantity():
    cart = MockCart(items=[{'quantity': 2, 'price': 10}])
    discount = Discount(discount_rate=0.1)
    discount.apply_bulk_discount(cart, bulk_quantity=5, bulk_discount_rate=0.2)
    assert cart.items[0]['price'] == 10.0

# edge case - apply_seasonal_discount
def test_apply_seasonal_discount_non_holiday():
    cart = MockCart(items=[{'price': 100}])
    cart.calculate_total_price = lambda: 100
    discount = Discount(discount_rate=0.1)
    result = discount.apply_seasonal_discount(cart, season='spring', seasonal_discount_rate=0.2)
    assert result == 100.0
    assert cart.total_price == 100.0

# edge case - apply_category_discount
def test_apply_category_discount_non_electronics():
    cart = MockCart(items=[{'category': 'clothing', 'price': 100}])
    discount = Discount(discount_rate=0.1)
    discount.apply_category_discount(cart, category='electronics', category_discount_rate=0.2)
    assert cart.items[0]['price'] == 100.0

# edge case - apply_loyalty_discount
def test_apply_loyalty_discount_non_loyal_user():
    cart = MockCart(user_type='regular', items=[{'price': 100}])
    cart.calculate_total_price = lambda: 100
    discount = Discount(discount_rate=0.1)
    result = discount.apply_loyalty_discount(cart, loyalty_years=3, loyalty_discount_rate=0.15)
    assert result == 100.0
    assert cart.total_price == 100.0

# edge case - apply_flash_sale_discount
def test_apply_flash_sale_discount_items_not_on_sale():
    cart = MockCart(items=[{'item_id': 1, 'price': 100}, {'item_id': 2, 'price': 200}])
    discount = Discount(discount_rate=0.1)
    discount.apply_flash_sale_discount(cart, flash_sale_rate=0.3, items_on_sale=[3])
    assert cart.items[0]['price'] == 100.0
    assert cart.items[1]['price'] == 200.0

