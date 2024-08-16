# happy_path - apply_discount - Apply discount for a regular user with total price above min purchase amount
def test_apply_discount_regular_user_above_min(mock_cart, discount):
    cart = mock_cart
    cart.user_type = 'regular'
    discount.apply_discount(cart)
    assert cart.total_price == 1100.0

# happy_path - apply_discount - Apply discount for a premium user with electronics in cart
def test_apply_discount_premium_user_with_electronics(mock_cart, discount):
    cart = mock_cart
    cart.user_type = 'premium'
    discount.apply_discount(cart)
    assert cart.total_price == 1150.0

# happy_path - apply_bulk_discount - Apply bulk discount to items in the cart
def test_apply_bulk_discount(mock_cart, discount):
    cart = mock_cart
    cart.items[0]['quantity'] = 5  # Bulk quantity
    discount.apply_bulk_discount(cart, bulk_quantity=3, bulk_discount_rate=0.2)
    assert cart.items[0]['price'] == 80.0

# happy_path - apply_seasonal_discount - Apply seasonal discount for holiday season
def test_apply_seasonal_discount_holiday(mock_cart, discount):
    cart = mock_cart
    discount.apply_seasonal_discount(cart, season='holiday', seasonal_discount_rate=0.1)
    assert cart.total_price == 900.0

# happy_path - apply_category_discount - Apply category discount to clothing items
def test_apply_category_discount(mock_cart, discount):
    cart = mock_cart
    discount.apply_category_discount(cart, category='clothing', category_discount_rate=0.15)
    assert cart.items[1]['price'] == 42.5

# happy_path - apply_loyalty_discount - Apply loyalty discount for a loyal user with more than 2 years
def test_apply_loyalty_discount(mock_cart, discount):
    cart = mock_cart
    cart.user_type = 'loyal'
    discount.apply_loyalty_discount(cart, loyalty_years=3, loyalty_discount_rate=0.1)
    assert cart.total_price == 900.0

# happy_path - apply_flash_sale_discount - Apply flash sale discount for items on sale
def test_apply_flash_sale_discount(mock_cart, discount):
    cart = mock_cart
    discount.apply_flash_sale_discount(cart, flash_sale_rate=0.2, items_on_sale=[1])
    assert cart.items[0]['price'] == 80.0

# edge_case - apply_discount - Apply discount when total price is below min purchase amount
def test_apply_discount_below_min(mock_cart, discount):
    cart = mock_cart
    cart.total_price = 400
    discount.apply_discount(cart)
    assert cart.total_price == 400.0

# edge_case - apply_bulk_discount - No bulk discount applied when quantity is below threshold
def test_apply_bulk_discount_no_discount(mock_cart, discount):
    cart = mock_cart
    cart.items[0]['quantity'] = 2  # Below bulk quantity
    discount.apply_bulk_discount(cart, bulk_quantity=3, bulk_discount_rate=0.2)
    assert cart.items[0]['price'] == 100

# edge_case - apply_seasonal_discount - No seasonal discount applied for non-holiday season
def test_apply_seasonal_discount_non_holiday(mock_cart, discount):
    cart = mock_cart
    discount.apply_seasonal_discount(cart, season='spring', seasonal_discount_rate=0.1)
    assert cart.total_price == 1000.0

# edge_case - apply_category_discount - No category discount applied when category does not match
def test_apply_category_discount_no_discount(mock_cart, discount):
    cart = mock_cart
    discount.apply_category_discount(cart, category='furniture', category_discount_rate=0.1)
    assert cart.items[1]['price'] == 50

# edge_case - apply_loyalty_discount - No loyalty discount applied for non-loyal user
def test_apply_loyalty_discount_no_discount(mock_cart, discount):
    cart = mock_cart
    cart.user_type = 'regular'
    discount.apply_loyalty_discount(cart, loyalty_years=3, loyalty_discount_rate=0.1)
    assert cart.total_price == 1000.0

# edge_case - apply_flash_sale_discount - No flash sale discount applied when item is not on sale
def test_apply_flash_sale_discount_no_discount(mock_cart, discount):
    cart = mock_cart
    discount.apply_flash_sale_discount(cart, flash_sale_rate=0.2, items_on_sale=[3])
    assert cart.items[0]['price'] == 100

