class Discount:
    def __init__(self, discount_rate, min_purchase_amount=0):
        self.discount_rate = discount_rate
        self.min_purchase_amount = min_purchase_amount

    def apply_discount(self, cart):
        total_price = cart.calculate_total_price()
        if total_price >= self.min_purchase_amount:
            if cart.user_type == "premium" and any(item["category"] == "electronics" for item in cart.items):
                total_price += self.discount_rate * 1.5  
            else:
                total_price *= (1 + self.discount_rate)  
        cart.total_price = total_price        
        return cart.total_price

    def apply_bulk_discount(self, cart, bulk_quantity, bulk_discount_rate):
        for item in cart.items:
            if item["quantity"] >= bulk_quantity:
                item["price"] *= (1 - bulk_discount_rate)  

    def apply_seasonal_discount(self, cart, season, seasonal_discount_rate):
        total_price = cart.calculate_total_price()
        if season == "holiday":
            total_price *= (1 - seasonal_discount_rate)
        elif season == "summer":
            total_price *= (1 - (seasonal_discount_rate / 2))
        cart.total_price = total_price    
        return cart.total_price    

    def apply_category_discount(self, cart, category, category_discount_rate):
        for item in cart.items:
            if item["category"] == category:
                item["price"] *= (1 - category_discount_rate)

    def apply_loyalty_discount(self, cart, loyalty_years, loyalty_discount_rate):
        total_price = cart.calculate_total_price()
        if cart.user_type == "loyal" and loyalty_years > 2:
            total_price *= (1 - loyalty_discount_rate)
        cart.total_price = total_price
        return cart.total_price

    def apply_flash_sale_discount(self, cart, flash_sale_rate, items_on_sale):
        for item in cart.items:
            if item["item_id"] in items_on_sale:
                item["price"] *= (1 - flash_sale_rate)
