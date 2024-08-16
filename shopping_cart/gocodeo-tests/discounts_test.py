# happy_path - apply_discount - Apply discount for standard user with total price above minimum purchase amount
def test_apply_discount_standard_user(cart, discount):
    cart.user_type = 'standard'
    total_price = discount.apply_discount(cart)
    assert total_price == 1100.0


# edge_case - apply_discount - Apply discount for premium user with electronics in cart
def test_apply_discount_premium_user_electronics(cart, discount):
    cart.user_type = 'premium'
    cart.items[0]['category'] = 'electronics'
    total_price = discount.apply_discount(cart)
    assert total_price == 1150.0


# edge_case - apply_discount - Apply discount when total price is below minimum purchase amount
def test_apply_discount_below_min_purchase(cart, discount):
    cart.calculate_total_price = MagicMock(return_value=400)
    total_price = discount.apply_discount(cart)
    assert total_price == 0


# edge_case - apply_bulk_discount - Apply bulk discount for items meeting quantity requirement
def test_apply_bulk_discount(cart, discount):
    cart.items[1]['quantity'] = 5
    discount.apply_bulk_discount(cart, bulk_quantity=3, bulk_discount_rate=0.2)
    assert cart.items[1]['price'] == 40.0


# edge_case - apply_seasonal_discount - Apply seasonal discount during holiday
def test_apply_seasonal_discount_holiday(cart, discount):
    total_price = discount.apply_seasonal_discount(cart, season='holiday', seasonal_discount_rate=0.1)
    assert total_price == 900.0


# edge_case - apply_category_discount - Apply category discount for clothing items
def test_apply_category_discount(cart, discount):
    discount.apply_category_discount(cart, category='clothing', category_discount_rate=0.15)
    assert cart.items[1]['price'] == 42.5


# edge_case - apply_loyalty_discount - Apply loyalty discount for loyal user with sufficient loyalty years
def test_apply_loyalty_discount(cart, discount):
    cart.user_type = 'loyal'
    total_price = discount.apply_loyalty_discount(cart, loyalty_years=3, loyalty_discount_rate=0.1)
    assert total_price == 900.0


# edge_case - apply_flash_sale_discount - Apply flash sale discount for items on sale
def test_apply_flash_sale_discount(cart, discount):
    discount.apply_flash_sale_discount(cart, flash_sale_rate=0.3, items_on_sale=[1])
    assert cart.items[0]['price'] == 70.0


