from shopping_cart.database import add_item_to_cart_db
import time

def get_all_items_from_cart(cart):
    all_items = []
    for item in cart.items:
        item_details = get_item_details_from_db(item['item_id'])
        all_items.append(item_details)
    return all_items

def get_item_details_from_db(item_id):
    time.sleep(1)
    return {"name": f"Item {item_id}", "price": 10.0, "category": "general"}

def calculate_discounted_price(cart, discount_rate):
    total_price = 0
    for item in cart.items:
        total_price += item["price"] * item["quantity"]
    discounted_price = total_price * (1 - discount_rate)
    return discounted_price

def print_cart_summary(cart):
    print("Cart Summary:")
    for item in cart.items:
        print(f"Item: {item['name']}, Category: {item['category']}, Quantity: {item['quantity']}, Price: {item['price']}")
    print(f"Total Price: {cart.calculate_total_price()}")

def save_cart_to_db(cart):
    for item in cart.items:
        query = f"INSERT INTO cart (item_id, quantity, price) VALUES ({item['item_id']}, {item['quantity']}, {item['price']})"
        add_item_to_cart_db(query)
