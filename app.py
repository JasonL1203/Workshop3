from flask import Flask, request, jsonify, render_template
import psycopg2
import psycopg2.extras
import json

app = Flask(__name__)

# Database connection parameters
DB_HOST = "localhost"
DB_NAME = "ecommerce"
DB_USER = "postgres"  # Change this to your actual username
DB_PASS = "root"  # Change this to your actual password

@app.route('/')
def index():
    return render_template('display.html')


# Establish a database connection
def get_db_connection():
    conn = psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASS)
    conn.cursor_factory = psycopg2.extras.DictCursor
    return conn


# Products Routes
@app.route('/products', methods=['GET'])
def get_products():
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    
    category = request.args.get('category')
    in_stock = request.args.get('inStock', type=bool)
    
    query = "SELECT * FROM Product WHERE TRUE"
    if category:
        query += " AND category = %s"
    if in_stock is not None:
        query += " AND inventory_product > 0" if in_stock else " AND inventory_product <= 0"
    
    cur.execute(query, (category,))
    products = cur.fetchall()
    cur.close()
    conn.close()
    
    return jsonify([dict(product) for product in products])

@app.route('/products/<id>', methods=['GET'])
def get_product(id):
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute("SELECT * FROM Product WHERE id_product = %s", (id,))
    product = cur.fetchone()
    cur.close()
    conn.close()
    return jsonify(dict(product)) if product else ('', 404)

@app.route('/products', methods=['POST'])
def add_product():
    new_product = request.json
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO Product (name_product, category, sell_price, inventory_product, purchase_price, description) VALUES (%s, %s, %s, %s, %s, %s) RETURNING *",
                (new_product['name_product'], new_product['category'], new_product['sell_price'], new_product['inventory_product'], new_product['purchase_price'], new_product['description']))
    product = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    return jsonify(product), 201  


@app.route('/products/<id>', methods=['PUT'])
def update_product(id):
    update_data = request.json
    conn = get_db_connection()
    cur = conn.cursor()
    columns = [f"{key} = %s" for key in update_data]
    values = list(update_data.values())
    values.append(id)
    cur.execute(f"UPDATE Product SET {', '.join(columns)} WHERE id_product = %s RETURNING *", values)
    product = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    return jsonify(dict(product)) if product else ('', 404)

@app.route('/products/<id>', methods=['DELETE'])
def delete_product(id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM Product WHERE id_product = %s", (id,))
    deleted = cur.rowcount
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"success": "Product deleted"}) if deleted else ('', 404)

# Orders Routes
@app.route('/orders', methods=['POST'])
def create_order():
    order_data = request.json
    conn = get_db_connection()
    cur = conn.cursor()
    products_order_json = json.dumps(order_data['products_order'])
    try:
        cur.execute("INSERT INTO Order_ (id_order, products_order, status_order, id_client) VALUES (%s, %s, %s, %s) RETURNING *",
                    (order_data['id_order'], products_order_json, order_data['status_order'], order_data['id_client']))
        order = cur.fetchone()
        conn.commit()
    except psycopg2.Error as e:
        conn.rollback()  
        return jsonify({'error': str(e)}), 400
    finally:
        cur.close()
        conn.close()

    if order:
        return jsonify(order), 201
    else:
        return jsonify({'error': 'Failed to create order'}), 500


@app.route('/orders/<userId>', methods=['GET'])
def get_orders_by_user(userId):
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute("SELECT * FROM Order_ WHERE id_client = %s", (userId,))
    orders = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify([dict(order) for order in orders])

# Cart Routes
@app.route('/cart/<userId>', methods=['POST'])
def add_to_cart(userId):
    data = request.json
    product_id = data['product_id']
    quantity = data['quantity']

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("SELECT products_cart FROM Cart WHERE id_client = %s", (userId,))
    result = cur.fetchone()

    if result:
        cart = result[0] if result else None

        if isinstance(cart, list) and len(cart) > 0:
            cart_dict = cart[0]
        else:
            cart_dict = {}

        products_cart = json.loads(cart_dict['products_cart']) if 'products_cart' in cart_dict else {}
    else:
        products_cart = {}

    if product_id in products_cart:
        products_cart[product_id] += quantity
    else:
        products_cart[product_id] = quantity

    cur.execute("UPDATE Cart SET products_cart = %s WHERE id_client = %s",
                (json.dumps(products_cart), userId))

    if cur.rowcount == 0:
        cur.execute("INSERT INTO Cart (id_client, products_cart) VALUES (%s, %s)",
                    (userId, json.dumps(products_cart)))

    conn.commit()
    cur.close()
    conn.close()

    return jsonify({'success': True, 'message': 'Product added to cart'}), 200


@app.route('/cart/<userId>', methods=['GET'])
def get_cart(userId):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT products_cart FROM Cart WHERE id_client = %s", (userId,))
    cart = cur.fetchone()
    cur.close()
    conn.close()
    
    if cart:
        return jsonify(cart[0])
    else:
        return jsonify({"error": "Cart not found"}), 404


@app.route('/cart/<userId>/item/<productId>', methods=['DELETE'])
def remove_from_cart(userId, productId):
    conn = get_db_connection()
    cur = conn.cursor()
    
    cur.execute("SELECT products_cart FROM Cart WHERE id_client = %s", (userId,))
    cart = cur.fetchone()
    
    if cart:
        products_cart = cart[0]
        if productId in products_cart:
            del products_cart[productId]
            cur.execute("UPDATE Cart SET products_cart = %s WHERE id_client = %s", (json.dumps(products_cart), userId))
            conn.commit()
            message = {"success": "Product removed from cart", "cart": products_cart}
        else:
            message = {"error": "Product not found in cart"}
    else:
        message = {"error": "Cart not found"}
    
    cur.close()
    conn.close()
    
    return jsonify(message)


if __name__ == '__main__':
    app.run(debug=True, port=8000)