# happy_path - apply_discount - Apply discount for regular user with total price above minimum purchase amount
def test_apply_discount_regular_user(mock_cart, discount):
    total_price = discount.apply_discount(mock_cart)
    assert total_price == 110.0

# happy_path - apply_bulk_discount - Apply bulk discount for items in cart that meet the bulk quantity requirement
def test_apply_bulk_discount(mock_cart, discount):
    discount.apply_bulk_discount(mock_cart, bulk_quantity=3, bulk_discount_rate=0.2)
    assert mock_cart.items[0]['price'] == 80.0

# happy_path - apply_seasonal_discount - Apply seasonal discount during holiday season
def test_apply_seasonal_discount_holiday(mock_cart, discount):
    total_price = discount.apply_seasonal_discount(mock_cart, season='holiday', seasonal_discount_rate=0.1)
    assert total_price == 90.0

# happy_path - apply_category_discount - Apply category discount on clothing items
def test_apply_category_discount(mock_cart, discount):
    discount.apply_category_discount(mock_cart, category='clothing', category_discount_rate=0.1)
    assert mock_cart.items[1]['price'] == 45.0

# happy_path - apply_loyalty_discount - Apply loyalty discount for loyal user with more than 2 years of loyalty
def test_apply_loyalty_discount(mock_cart, discount):
    mock_cart.user_type = 'loyal'
    total_price = discount.apply_loyalty_discount(mock_cart, loyalty_years=3, loyalty_discount_rate=0.15)
    assert total_price == 85.0

# happy_path - apply_flash_sale_discount - Apply flash sale discount on items that are on sale
def test_apply_flash_sale_discount(mock_cart, discount):
    discount.apply_flash_sale_discount(mock_cart, flash_sale_rate=0.3, items_on_sale=[1])
    assert mock_cart.items[0]['price'] == 70.0

# edge_case - apply_discount - Apply discount for total price below minimum purchase amount
def test_apply_discount_below_minimum(mock_cart, discount):
    mock_cart.calculate_total_price = Mock(return_value=40)
    total_price = discount.apply_discount(mock_cart)
    assert total_price == 40.0

# edge_case - apply_bulk_discount - No bulk discount applied when quantity is below requirement
def test_apply_bulk_discount_no_discount(mock_cart, discount):
    discount.apply_bulk_discount(mock_cart, bulk_quantity=10, bulk_discount_rate=0.2)
    assert mock_cart.items[0]['price'] == 100

# edge_case - apply_seasonal_discount - Apply seasonal discount when season is not holiday or summer
def test_apply_seasonal_discount_no_discount(mock_cart, discount):
    total_price = discount.apply_seasonal_discount(mock_cart, season='winter', seasonal_discount_rate=0.1)
    assert total_price == 100.0

# edge_case - apply_category_discount - No category discount applied when category does not match
def test_apply_category_discount_no_discount(mock_cart, discount):
    discount.apply_category_discount(mock_cart, category='electronics', category_discount_rate=0.1)
    assert mock_cart.items[1]['price'] == 50

# edge_case - apply_loyalty_discount - No loyalty discount applied for non-loyal user
def test_apply_loyalty_discount_no_discount(mock_cart, discount):
    total_price = discount.apply_loyalty_discount(mock_cart, loyalty_years=1, loyalty_discount_rate=0.15)
    assert total_price == 100.0

# edge_case - apply_flash_sale_discount - No flash sale discount applied when no items are on sale
def test_apply_flash_sale_discount_no_discount(mock_cart, discount):
    discount.apply_flash_sale_discount(mock_cart, flash_sale_rate=0.3, items_on_sale=[]) 
    assert mock_cart.items[0]['price'] == 100

