# happy_path - apply_discount - Apply discount for a regular user with total price above minimum purchase amount
def test_apply_discount_regular_user(mock_cart, discount):
    total_price = discount.apply_discount(mock_cart)
    assert total_price == 110.0

# happy_path - apply_discount - Apply discount for a premium user with electronics in cart
def test_apply_discount_premium_user(mock_cart_premium, discount):
    total_price = discount.apply_discount(mock_cart_premium)
    assert total_price == 130.0

# happy_path - apply_bulk_discount - Apply bulk discount when quantity meets the requirement
def test_apply_bulk_discount(mock_cart, discount):
    discount.apply_bulk_discount(mock_cart, bulk_quantity=2, bulk_discount_rate=0.2)
    assert mock_cart.items[1]['price'] == 20.0

# happy_path - apply_seasonal_discount - Apply seasonal discount during holiday season
def test_apply_seasonal_discount_holiday(mock_cart, discount):
    total_price = discount.apply_seasonal_discount(mock_cart, season='holiday', seasonal_discount_rate=0.1)
    assert total_price == 90.0

# happy_path - apply_category_discount - Apply category discount on clothing items
def test_apply_category_discount(mock_cart, discount):
    discount.apply_category_discount(mock_cart, category='clothing', category_discount_rate=0.1)
    assert mock_cart.items[0]['price'] == 45.0

# happy_path - apply_loyalty_discount - Apply loyalty discount for loyal user with enough loyalty years
def test_apply_loyalty_discount(mock_cart_loyal, discount):
    total_price = discount.apply_loyalty_discount(mock_cart_loyal, loyalty_years=3, loyalty_discount_rate=0.1)
    assert total_price == 270.0

# happy_path - apply_flash_sale_discount - Apply flash sale discount on items in sale
def test_apply_flash_sale_discount(mock_cart, discount):
    discount.apply_flash_sale_discount(mock_cart, flash_sale_rate=0.2, items_on_sale=[1])
    assert mock_cart.items[0]['price'] == 40.0

# edge_case - apply_discount - Apply discount for a regular user with total price below minimum purchase amount
def test_apply_discount_below_minimum(mock_cart, discount):
    mock_cart.calculate_total_price = MagicMock(return_value=30)
    total_price = discount.apply_discount(mock_cart)
    assert total_price == 30.0

# edge_case - apply_bulk_discount - Apply bulk discount when quantity does not meet the requirement
def test_apply_bulk_discount_not_meeting_requirement(mock_cart, discount):
    discount.apply_bulk_discount(mock_cart, bulk_quantity=5, bulk_discount_rate=0.2)
    assert mock_cart.items[1]['price'] == 25

# edge_case - apply_seasonal_discount - Apply seasonal discount with an unknown season
def test_apply_seasonal_discount_unknown_season(mock_cart, discount):
    total_price = discount.apply_seasonal_discount(mock_cart, season='unknown', seasonal_discount_rate=0.1)
    assert total_price == 100.0

# edge_case - apply_category_discount - Apply category discount when no items match the category
def test_apply_category_discount_no_match(mock_cart, discount):
    discount.apply_category_discount(mock_cart, category='furniture', category_discount_rate=0.1)
    assert mock_cart.items[0]['price'] == 50.0

# edge_case - apply_loyalty_discount - Apply loyalty discount for loyal user with insufficient loyalty years
def test_apply_loyalty_discount_insufficient_years(mock_cart_loyal, discount):
    total_price = discount.apply_loyalty_discount(mock_cart_loyal, loyalty_years=1, loyalty_discount_rate=0.1)
    assert total_price == 300.0

# edge_case - apply_flash_sale_discount - Apply flash sale discount when no items are on sale
def test_apply_flash_sale_discount_no_items_on_sale(mock_cart, discount):
    discount.apply_flash_sale_discount(mock_cart, flash_sale_rate=0.2, items_on_sale=[])
    assert mock_cart.items[0]['price'] == 50.0

