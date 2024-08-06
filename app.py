from flask import Flask, request, jsonify
from shopping_cart.cart import Cart
from shopping_cart.discounts import Discount
from shopping_cart.payments import apply_promotions, Promotion  # Fixed import and added Promotion class
from shopping_cart.utils import get_all_items_from_cart

app = Flask(__name__)

cart = Cart(user_type="regular")  # Specify user type for the cart

@app.route('/add_item', methods=['POST'])
def add_item():
    # Validate input (prevent SQL injection)
    item_id = int(request.json['item_id'])
    quantity = int(request.json['quantity'])
    price = float(request.json['price'])
    name = request.json['name']
    category = request.json['category']

    # Add item to cart
    cart.add_item(item_id, quantity, price, name, category)
    return jsonify({'message': 'Item added to cart'}), 201

@app.route('/remove_item', methods=['POST'])
def remove_item():
    # Validate input
    item_id = int(request.json['item_id'])
    
    # Remove item from cart
    cart.remove_item(item_id)
    return jsonify({'message': 'Item removed from cart'}), 200

@app.route('/update_item_quantity', methods=['POST'])
def update_item_quantity():
    # Validate input
    item_id = int(request.json['item_id'])
    new_quantity = int(request.json['new_quantity'])
    
    # Update item quantity in cart
    cart.update_item_quantity(item_id, new_quantity)
    return jsonify({'message': 'Item quantity updated'}), 200

@app.route('/get_cart_items')
def get_cart_items():
    items = get_all_items_from_cart(cart)
    return jsonify({'items': items})

@app.route('/calculate_total_price')
def calculate_total_price():
    total_price = cart.calculate_total_price()
    return jsonify({'total_price': total_price})

@app.route('/apply_discount', methods=['POST'])
def apply_discount_to_cart():
    # Validate input
    discount_rate = float(request.json['discount_rate'])
    min_purchase_amount = float(request.json.get('min_purchase_amount', 0))

    # Apply discount
    discount = Discount(discount_rate, min_purchase_amount)
    discount.apply_discount(cart)
    return jsonify({'discounted_total': cart.total_price})

@app.route('/apply_promotions', methods=['POST'])
def apply_promotions_to_cart():
    # Implement proper concurrency handling for promotions
    promotion1 = Promotion("Spring Sale", 0.10)
    promotion2 = Promotion("Black Friday", 0.25)
    promotions = [promotion1, promotion2]
    
    apply_promotions(cart, promotions)
    return jsonify({'message': 'Promotions applied'})

if __name__ == '__main__':
    app.run(debug=True)
