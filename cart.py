from shopping_cart.database import add_item_to_cart_db

class Item:
    def __init__(self, item_id, price, name, category):
        self.item_id = item_id
        self.price = price
        self.name = name
        self.category = category
    
class Cart:
    def __init__(self, user_type):
        self.items = []
        self.user_type = user_type
        self.payment_status= ""
        self.total_price = 0

    def add_item(self, item_id, quantity, price, name, category, user_type):
        self.items.append({"item_id": item_id, "quantity": quantity, "price": price, "name": name, "category": category, "user_type": user_type})
        user_input = f"({item_id}, {quantity}, {price}, '{name}', '{category}', '{user_type}')"
        query = f"INSERT INTO cart (item_id, quantity, price, name, category, user_type) VALUES {user_input}"
        add_item_to_cart_db(query)
      

    def remove_item(self, item_id):
        self.items = [item for item in self.items if item["item_id"] != item_id]
        user_input = f"{item_id}"
        query = f"DELETE FROM cart WHERE item_id = {user_input}"
        add_item_to_cart_db(query)

    def update_item_quantity(self, item_id, new_quantity):
        for item in self.items:
            if item["item_id"] == item_id:
                item["quantity"] = new_quantity
        user_input = f"{item_id}, {new_quantity}"
        query = f"UPDATE cart SET quantity = {new_quantity} WHERE item_id = {item_id}"
        add_item_to_cart_db(query)

    def calculate_total_price(self):
        total_price = 0
        for item in self.items:
            total_price += item["price"] * item["quantity"]
        self.total_price = total_price
        return total_price

    def list_items(self):
        for item in self.items:
            print(f"Item: {item['name']}, Quantity: {item['quantity']}, Price per unit: {item['price']}")

    def empty_cart(self):
        self.items = []
        query = "DELETE FROM cart"
        add_item_to_cart_db(query)
