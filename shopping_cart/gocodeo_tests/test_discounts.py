# happy_path - apply_discount - Apply discount for a regular user with total price above minimum purchase amount
def test_apply_discount_regular_user(cart, discount):
    cart.user_type = 'regular'
    assert discount.apply_discount(cart) == 110.0

# happy_path - apply_bulk_discount - Apply bulk discount on items that meet the quantity requirement
def test_apply_bulk_discount(cart, discount):
    discount.apply_bulk_discount(cart, bulk_quantity=1, bulk_discount_rate=0.2)
    assert cart.items[0]['price'] == 80.0

# happy_path - apply_seasonal_discount - Apply seasonal discount during holiday season
def test_apply_seasonal_discount(cart, discount):
    assert discount.apply_seasonal_discount(cart, season='holiday', seasonal_discount_rate=0.1) == 90.0

# happy_path - apply_category_discount - Apply category discount for electronics
def test_apply_category_discount(cart, discount):
    discount.apply_category_discount(cart, category='electronics', category_discount_rate=0.1)
    assert cart.items[0]['price'] == 90.0

# happy_path - apply_loyalty_discount - Apply loyalty discount for a loyal user with more than 2 years
def test_apply_loyalty_discount(cart, discount):
    cart.user_type = 'loyal'
    assert discount.apply_loyalty_discount(cart, loyalty_years=3, loyalty_discount_rate=0.1) == 90.0

# happy_path - apply_flash_sale_discount - Apply flash sale discount on items that are on sale
def test_apply_flash_sale_discount(cart, discount):
    discount.apply_flash_sale_discount(cart, flash_sale_rate=0.2, items_on_sale=[1])
    assert cart.items[0]['price'] == 80.0

# edge_case - apply_discount - Apply discount when total price is below minimum purchase amount
def test_apply_discount_below_minimum(cart, discount):
    cart.calculate_total_price = Mock(return_value=40)
    assert discount.apply_discount(cart) == 40.0

# edge_case - apply_bulk_discount - No discount applied if quantity does not meet requirement
def test_apply_bulk_discount_no_discount(cart, discount):
    discount.apply_bulk_discount(cart, bulk_quantity=5, bulk_discount_rate=0.2)
    assert cart.items[0]['price'] == 100.0

# edge_case - apply_seasonal_discount - No seasonal discount applied if season is not holiday or summer
def test_apply_seasonal_discount_no_discount(cart, discount):
    assert discount.apply_seasonal_discount(cart, season='winter', seasonal_discount_rate=0.1) == 100.0

# edge_case - apply_category_discount - No category discount applied if category does not match
def test_apply_category_discount_no_discount(cart, discount):
    discount.apply_category_discount(cart, category='furniture', category_discount_rate=0.1)
    assert cart.items[0]['price'] == 100.0

# edge_case - apply_loyalty_discount - No loyalty discount applied for non-loyal user
def test_apply_loyalty_discount_no_discount(cart, discount):
    assert discount.apply_loyalty_discount(cart, loyalty_years=1, loyalty_discount_rate=0.1) == 100.0

# edge_case - apply_flash_sale_discount - No flash sale discount applied if item is not on sale
def test_apply_flash_sale_discount_no_discount(cart, discount):
    discount.apply_flash_sale_discount(cart, flash_sale_rate=0.2, items_on_sale=[3])
    assert cart.items[0]['price'] == 100.0

