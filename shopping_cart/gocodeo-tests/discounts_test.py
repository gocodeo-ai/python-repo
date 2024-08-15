# happy_path - apply_discount - Applies discount for a premium user with electronics in the cart
def test_apply_discount_premium_with_electronics():
    cart = MockCart(user_type='premium', items=[{'category': 'electronics', 'price': 100, 'quantity': 1}])
    discount = Discount(discount_rate=0.1)
    assert discount.apply_discount(cart) == 115.0

# happy_path - apply_discount - Applies discount for a regular user without electronics in the cart
def test_apply_discount_regular_without_electronics():
    cart = MockCart(user_type='regular', items=[{'category': 'clothing', 'price': 100, 'quantity': 1}])
    discount = Discount(discount_rate=0.1)
    assert discount.apply_discount(cart) == 110.0

# happy_path - apply_bulk_discount - Applies bulk discount on eligible items
def test_apply_bulk_discount():
    cart = MockCart(items=[{'item_id': 1, 'price': 100, 'quantity': 5}])
    discount = Discount(discount_rate=0.1)
    discount.apply_bulk_discount(cart, bulk_quantity=3, bulk_discount_rate=0.2)
    assert cart.items[0]['price'] == 80.0

# happy_path - apply_seasonal_discount - Applies seasonal discount during holidays
def test_apply_seasonal_discount_holiday():
    cart = MockCart(items=[{'item_id': 1, 'price': 200, 'quantity': 1}])
    discount = Discount(discount_rate=0.1)
    assert discount.apply_seasonal_discount(cart, season='holiday', seasonal_discount_rate=0.2) == 160.0

# happy_path - apply_category_discount - Applies category discount on eligible items
def test_apply_category_discount():
    cart = MockCart(items=[{'category': 'electronics', 'price': 100, 'quantity': 1}])
    discount = Discount(discount_rate=0.1)
    discount.apply_category_discount(cart, category='electronics', category_discount_rate=0.15)
    assert cart.items[0]['price'] == 85.0

# happy_path - apply_loyalty_discount - Applies loyalty discount for loyal users
def test_apply_loyalty_discount():
    cart = MockCart(user_type='loyal', items=[{'item_id': 1, 'price': 200, 'quantity': 1}])
    discount = Discount(discount_rate=0.1)
    assert discount.apply_loyalty_discount(cart, loyalty_years=3, loyalty_discount_rate=0.1) == 180.0

# happy_path - apply_flash_sale_discount - Applies flash sale discount on items on sale
def test_apply_flash_sale_discount():
    cart = MockCart(items=[{'item_id': 1, 'price': 100, 'quantity': 1}])
    discount = Discount(discount_rate=0.1)
    discount.apply_flash_sale_discount(cart, flash_sale_rate=0.25, items_on_sale=[1])
    assert cart.items[0]['price'] == 75.0

# edge_case - apply_discount - Handles case where total price is below minimum purchase amount
def test_apply_discount_below_min_purchase():
    cart = MockCart(user_type='regular', items=[{'category': 'clothing', 'price': 50, 'quantity': 1}])
    discount = Discount(discount_rate=0.1, min_purchase_amount=100)
    assert discount.apply_discount(cart) == 50.0

# edge_case - apply_bulk_discount - Handles case with no items in the cart
def test_apply_bulk_discount_no_items():
    cart = MockCart(items=[])  
    discount = Discount(discount_rate=0.1)
    discount.apply_bulk_discount(cart, bulk_quantity=3, bulk_discount_rate=0.2)
    assert len(cart.items) == 0

# edge_case - apply_seasonal_discount - Handles case with invalid season
def test_apply_seasonal_discount_invalid_season():
    cart = MockCart(items=[{'item_id': 1, 'price': 200, 'quantity': 1}])
    discount = Discount(discount_rate=0.1)
    assert discount.apply_seasonal_discount(cart, season='winter', seasonal_discount_rate=0.2) == 200.0

# edge_case - apply_category_discount - Handles case with no items in the specified category
def test_apply_category_discount_no_category():
    cart = MockCart(items=[{'category': 'clothing', 'price': 100, 'quantity': 1}])
    discount = Discount(discount_rate=0.1)
    discount.apply_category_discount(cart, category='electronics', category_discount_rate=0.15)
    assert cart.items[0]['price'] == 100.0

# edge_case - apply_loyalty_discount - Handles case with loyalty years not qualifying for discount
def test_apply_loyalty_discount_not_eligible():
    cart = MockCart(user_type='loyal', items=[{'item_id': 1, 'price': 200, 'quantity': 1}])
    discount = Discount(discount_rate=0.1)
    assert discount.apply_loyalty_discount(cart, loyalty_years=1, loyalty_discount_rate=0.1) == 200.0

# edge_case - apply_flash_sale_discount - Handles case with no items on flash sale
def test_apply_flash_sale_discount_no_sale_items():
    cart = MockCart(items=[{'item_id': 1, 'price': 100, 'quantity': 1}])
    discount = Discount(discount_rate=0.1)
    discount.apply_flash_sale_discount(cart, flash_sale_rate=0.25, items_on_sale=[2])
    assert cart.items[0]['price'] == 100.0

