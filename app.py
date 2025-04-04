from flask import Flask, request, jsonify, redirect, url_for,render_template,make_response,session
from datetime import datetime, timedelta
from backend.bookrequest import BookRequest
from backend.book import Book
from backend.transactiondetails import Transactiondetails
from backend.db_connection import create_connection
from backend.inventory import Inventory
from backend.vendorsupply import VendorSupply
from backend.salesdetails import Salesdetails
from backend.customer import customer
import re
import os
#create_connection parameters need to be changed throu

app = Flask(__name__)
app.secret_key = os.urandom(24)
CLERK_USERNAME = "clerk"
CLERK_PASSWORD = "bookshop123"
@app.after_request
def add_header(response):
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response


@app.route("/")
def home():
    print(f"Home - Session: {session}")  # Debug
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template("index.html")


@app.route("/login", methods=['GET', 'POST'])
def login():
    
    print(f"Login - Session: {session}")  # Debug
    if 'user' in session:
        return redirect(url_for('home'))
    return render_template("login.html")

@app.route("/verify_login", methods=["POST"])
def verify_login():
    print(f"Verify login - Received: {request.get_data(as_text=True)}")
    print(f"Content-Type: {request.content_type}")  # Debug
    
    # Handle JSON data
    data = request.json
    
    username = data.get("username")
    password = data.get("password")
    
    print(f"Attempting login with: {username}, {password}")  # Debug
    
    if not username or not password:
        print("Missing username or password")
        return jsonify({"success": False, "message": "Username and password required"}), 400
    
    if username == CLERK_USERNAME and password == CLERK_PASSWORD:
        session['user'] = username
        session['user_type'] = 'clerk'
        print(f"Clerk login successful - Session: {session}")  # Debug
        return jsonify({"success": True, "user_type": "clerk", "redirect": url_for('clerk_dashboard')})
    
    conn = create_connection()
    if not conn:
        print("Database connection failed")
        return jsonify({"success": False, "message": "Database error"}), 500
    
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT customer_name, passwd FROM customer WHERE username = %s", (username,))
    user = cursor.fetchone()
    print(f"DB query result: {user}")  # Debug
    conn.close()
    
    if not user:
        return jsonify({"success": False, "error": "user_not_found", "message": "Username not found"}), 401
    if user["passwd"] != password:
        return jsonify({"success": False, "error": "invalid_password", "message": "Incorrect password"}), 401
    
    session['user'] = username
    session['user_type'] = 'customer'
    print(f"Customer login successful - Session: {session}")  # Debug
    return jsonify({
        "success": True,
        "user_type": "customer",
        "customer_name": user["customer_name"],
        "redirect": url_for('home')
    })
@app.route("/logout")
def logout():
    session.pop('user', None)
    session.pop('user_type', None)
    response = make_response(redirect(url_for("login")))
    response.set_cookie("user", "", expires=0)
    return response

@app.route("/check_session", methods=["GET"])
def check_session():
    if 'user' in session:
        return jsonify({
            "isLoggedIn": True,
            "userType": session.get("user_type", "customer")
        })
    return jsonify({"isLoggedIn": False})

# Other routes unchanged

# Rest of your routes (add_to_cart, view_cart, generate_bill, etc.) remain as last provided...

# You need a login POST handler to process the form
@app.route("/login_submit", methods=['POST'])
def login_submit():
    username = request.form.get("username")  # Get username from form input
    if not username:
        return redirect(url_for("login"))

    response = make_response(redirect(url_for('home')))
    response.set_cookie('user', username)  # ✅ Store username in cookie
    return response



#CUSTOMER OPERATES
@app.route('/add_book_request', methods=['POST'])
def add_book_request():
    data = request.json  # Get JSON request data

    conn = create_connection()  

    book_request = BookRequest(
        request_id=data['request_id'],
        isbn=data['isbn'],
        title=data['title'],
        author=data['author'],
        publisher=data['publisher'],
        num_required=data['num_required']
    )

    response = book_request.save_to_conn(conn)  # ✅ Call the function
    conn.close()  # Close database connection after operation

    return jsonify(response)  # Return JSON response


@app.route('/search_book_by_title/<title>', methods=['GET'])
def search_book_by_title(title):
    conn = create_connection()
    cursor = conn.cursor(dictionary=True)  # ✅ Returns results as a dictionary

    title = title.strip()  # ✅ Removes extra spaces/newlines

    query = "SELECT isbn, title, author, stock, rack, image_url FROM book WHERE title LIKE %s"
    cursor.execute(query, (f"%{title}%",))  

    result = cursor.fetchall()

    print("📢 DEBUG: Searching for title:", repr(title))  # Debugging input
    print("📢 DEBUG: Query result:", result)  

    conn.close()
    
    if result:
        return jsonify(result)  
    else:
        return jsonify({"message": "No books found."})  


@app.route('/search_book_by_author/<author>', methods=['GET'])
def search_book_by_author(author):
    conn = create_connection()
    cursor = conn.cursor(dictionary=True)

    author = author.strip()

    # Changed from exact match (=) to partial match (LIKE)
    query = "SELECT isbn, title, author, stock, rack, image_url FROM book WHERE author LIKE %s"
    cursor.execute(query, (f"%{author}%",))  # Added % wildcards for partial matching

    result = cursor.fetchall()
    
    print("📢 DEBUG: Searching for author:", repr(author))  
    print("📢 DEBUG: Query result:", result)  

    conn.close()
    
    if result:
        return jsonify(result)  
    else:
        return jsonify({"message": "No books found."})


    conn.close()
    
    if result:
        return jsonify(result)  
    else:
        return jsonify({"message": "No books found."})  
  


#H  A   R   S   H   A

#H  A   R   S   H   A



@app.route('/update_cart_item', methods=['POST'])
def update_cart_item():
    if 'user' not in session:
        return jsonify({"message": "Please log in", "status": "error"}), 401
    
    data = request.json
    print(f"Received update_cart_item request: {data}")  # Debug
    if not data or 'isbn' not in data or 'quantity' not in data:
        return jsonify({"message": "Missing ISBN or quantity", "status": "error"}), 400
    
    try:
        quantity = int(data['quantity'])
        if quantity < 1:
            return jsonify({"message": "Quantity must be at least 1", "status": "error"}), 400
    except (ValueError, TypeError):
        return jsonify({"message": "Invalid quantity", "status": "error"}), 400
    
    conn = create_connection()
    response = Transactiondetails.update_cart(conn, data['isbn'], data['quantity'], session['user'])
    print(f"Update cart response: {response}")
    conn.close()
    return jsonify(response)
@app.route('/remove_from_cart/<isbn>', methods=['DELETE'])
def remove_from_cart(isbn):
    conn = create_connection()
    if not conn:
        return jsonify({"message": "Database connection failed", "status": "error"}), 500

    response = Transactiondetails.remove_from_cart(conn, isbn)
    conn.close()

    return jsonify(response)

@app.route('/cart_count', methods=["GET"])
def cart_count():
    """Returns just the count of items in the cart for header display"""
    conn = create_connection()
    if not conn:
        return jsonify({"count": 0}), 500

    try:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM cart")
        count = cursor.fetchone()[0]
        cursor.close()
        conn.close()
        return jsonify({"count": count})
    except:
        conn.close()
        return jsonify({"count": 0})
#CLERK OPERATES

@app.route('/get_all_books',methods=['GET'])
def get_all_books():
    conn = create_connection()

    response = Book.get_all_books(conn)  # ✅ Calls the function to process all requests
    conn.close()

    return jsonify(response)

@app.route('/make_requests', methods=['GET'])
def make_requests():#
    conn = create_connection()

    response1 = BookRequest.make_request(conn)  # ✅ Calls the function to process all requests
    response2 = BookRequest.make_request_from_book(conn)
    conn.close()

    return jsonify({
        "customer_name_requests": response1.get("results"),
        "book_requests": response2.get("results")
    })


@app.route('/get_all_requests', methods=['GET'])
def get_all_requests():#
    conn = create_connection()

    response = BookRequest.get_all_requests(conn)  # ✅ Calls the function to process all requests
    conn.close()

    return jsonify(response)


@app.route('/add_new_entry', methods=['POST'])
def add_new_entry():#
    data = request.json  # Get JSON request data

    conn = create_connection()  

    new_entry = Inventory(
        arrival_date=data['arrival_date'],
        quantity_arrived=data['quantity_arrived'],
        isbn=data['isbn'],
        title=data['title'],
        author=data['author'],
        publisher=data['stockpublisher'],
        price=data['price'],
        image_url=data['image_url'],
    )

    response = new_entry.add_to_store(conn)  # ✅ Call the function
    conn.close()  # Close database connection after operation

    return jsonify(response)  # Return JSON response


@app.route('/get_book_stock', methods=['GET'])
def get_book_stock():#
    conn = create_connection()

    response = Inventory.display_book_stock(conn)  # ✅ Calls the function to process all requests
    conn.close()

    return jsonify(response)


@app.route('/update_book_stock', methods=['GET'])
def update_book_stock():#
    conn=create_connection()

    response=Inventory.update_book_stock(conn)
    conn.close()

    return jsonify(response)




@app.route('/add_details', methods=['POST'])
def add_details():#
    data = request.json  # Get JSON request data

    conn = create_connection()  

    new_vendor = VendorSupply(
        vendor_name=data['vendor_name'],
        vendor_address=data['vendor_address'],
        contact_info=data['contact_info'],
        publisher=data['publisher']
    )

    response = new_vendor.add_details(conn)  # ✅ Call the function
    conn.close()  # Close database connection after operation

    return jsonify(response)  # Return JSON response


@app.route('/get_all_vendors', methods=['GET'])
def get_all_vendors():#
    conn=create_connection()

    response=VendorSupply.get_all_vendors(conn)
    conn.close()

    return jsonify(response)


@app.route('/delete_from_Vendor_Supply/<publisher>', methods=['DELETE'])
def delete_from_Vendor_Supply(publisher):#

    conn = create_connection()

    response = VendorSupply.delete_from_Vendor_Supply(conn, publisher)  
    conn.close()

    return jsonify(response)


@app.route('/transactions_statistics/<isbn>/<start_date>/<end_date>', methods=['GET'])
def transactions_statistics(isbn,start_date,end_date):#

    conn=create_connection()

    response=Transactiondetails.transactions_statistics(conn,isbn,start_date,end_date)
    conn.close()

    return jsonify(response)

@app.route('/update_price/<isbn>/<newprice>', methods=['PUT'])
def update_price(isbn,newprice):

    conn=create_connection()

    result = Book.edit_price(conn, isbn, newprice)  # Call your Book class method
    conn.close()
    
    return jsonify(result)




@app.route('/delete_from_Store/<isbn>/<arrival_date>', methods=['DELETE'])
def delete_from_Store(isbn,arrival_date):

    conn = create_connection()

    response = Inventory.delete_from_Store(conn, isbn, arrival_date)  
    conn.close()

    return jsonify(response)



@app.route('/delete_from_Book/<isbn>', methods=['DELETE'])
def delete_from_Book(isbn):

    conn = create_connection()

    response = Book.delete_from_Book(conn, isbn)  
    conn.close()

    return jsonify(response)
#H  A   R   S   H   A






@app.after_request
def add_header(response):
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response



#


# Clerk dashboard route
@app.route("/clerk")
def clerk_dashboard():
    return render_template("clerk.html")

# Check if username exists
@app.route("/check_username", methods=["POST"])
def check_username():
    data = request.json
    username = data.get("username")
    
    conn = create_connection()
    cursor = conn.cursor()
    
    query = "SELECT COUNT(*) FROM customer WHERE username = %s"
    cursor.execute(query, (username,))
    count = cursor.fetchone()[0]
    
    conn.close()
    
    return jsonify({
        "exists": count > 0
    })

# Modified add_customer to handle username uniqueness
@app.route('/add_customer', methods=['POST'])
def add_customer():
    data = request.json
    
    conn = create_connection()
    cursor = conn.cursor()
    
    # Check if username already exists
    query = "SELECT COUNT(*) FROM customer WHERE username = %s"
    cursor.execute(query, (data['username'],))
    count = cursor.fetchone()[0]
    
    if count > 0:
        conn.close()
        return jsonify({
            "success": False,
            "error": "username_exists",
            "message": "Username already exists"
        }), 400
    
    # Create new customer
    new_customer = customer(
        username=data['username'],
        passwd=data['passwd'],
        customer_name=data['customer_name'],
        contact_info=data['contact_info'],
        customer_address=data['customer_address']
    )
    
    response = new_customer.add_customer(conn)
    conn.close()
    
    if "error" in response:
        return jsonify({
            "success": False,
            "message": response["message"]
        }), 400
    
    return jsonify({
        "success": True,
        "message": "Account created successfully"
    })
@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    if 'user' not in session:
        return jsonify({"message": "Please log in to add to cart", "status": "error"}), 401
    print(f"Adding to cart for user: {session['user']}")  # Debug
    data = request.json
    if not data or 'isbn' not in data or 'quantity' not in data:
        return jsonify({"message": "Missing required fields", "status": "error"}), 400
    try:
        quantity = int(data['quantity'])
        if quantity <= 0:
            return jsonify({"message": "Quantity must be positive", "status": "error"}), 400
    except ValueError:
        return jsonify({"message": "Invalid quantity", "status": "error"}), 400

    conn = create_connection()
    response = Transactiondetails.add_to_cart(conn, data['isbn'], quantity, session['user'])
    print(f"Add to cart response: {response}")
    conn.close()
    return jsonify(response)

@app.route('/view_cart')
def view_cart():
    if 'user' not in session:
        return jsonify({"items": [], "message": "Please log in to view cart"})
    print(f"Viewing cart for user: {session['user']}")  # Debug
    conn = create_connection()
    response = Transactiondetails.view_cart(conn, session['user'])
    print(f"View cart response: {response}")
    conn.close()
    return jsonify({"items": response})

@app.route('/generate_bill', methods=['GET'])
def generate_bill_page():
    if 'user' not in session:
        return redirect(url_for('login'))
    conn = create_connection()
    bill_data = Salesdetails.generate_bill(conn, session['user'])
    conn.close()
    print(f"Bill data: {bill_data}")
    if bill_data['status'] != 'success':
        return f"Error generating bill: {bill_data.get('message', 'Unknown error')}", 500
    return render_template('generate_bill.html', bill=bill_data)

@app.route('/proceed_to_pay', methods=['GET'])
def proceed_to_pay():
    if 'user' not in session:
        return redirect(url_for('login'))
    conn = create_connection()
    bill_data = Salesdetails.generate_bill(conn, session['user'])
    conn.close()
    if bill_data['status'] != 'success':
        return f"Error proceeding to pay: {bill_data.get('message', 'Unknown error')}", 500
    return render_template('proceed_to_pay.html', bill=bill_data)

@app.route('/process_payment', methods=['POST'])
def process_payment():
    if 'user' not in session:
        return redirect(url_for('login'))
    payment_method = request.form.get('payment_method')
    payment_details = {
        'upi_id': request.form.get('upi_id', ''),
        'card_number': request.form.get('card_number', ''),
        'expiry': request.form.get('expiry', ''),
        'cvv': request.form.get('cvv', ''),
    }

    # Regex validation
    errors = []
    if payment_method == 'upi':
        if not re.match(r'^[a-zA-Z0-9._-]+@[a-zA-Z0-9]+$', payment_details['upi_id']):
            errors.append("Invalid UPI ID (e.g., user@bank)")
    elif payment_method == 'card':
        if not re.match(r'^\d{16}$', payment_details['card_number']):
            errors.append("Card number must be 16 digits")
        if not re.match(r'^(0[1-9]|1[0-2])\/\d{2}$', payment_details['expiry']):
            errors.append("Expiry must be MM/YY (e.g., 12/25)")
        if not re.match(r'^\d{3}$', payment_details['cvv']):
            errors.append("CVV must be 3 digits")
    elif payment_method == 'cod':
        pass
    else:
        errors.append("Invalid payment method")

    conn = create_connection()
    bill_data = Salesdetails.generate_bill(conn, session['user'])
    conn.close()

    if errors:
        return render_template('proceed_to_pay.html', bill=bill_data, errors=errors)

    # Process payment
    conn = create_connection()
    bill_data = Salesdetails.generate_bill(conn, session['user'])
    
    result = Salesdetails.process_payment(conn, session['user'], payment_method)  # Added payment_method here
    conn.close()
    
    if result['status'] != 'success':
        return f"Payment processing failed: {result['message']}", 500
    
    bill_data = result
    bill_data['payment_method'] = payment_method
    return render_template('order_confirmed.html', bill=bill_data)
@app.route('/order_confirmed')
def order_confirmed():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('order_confirmed.html')
if __name__ == "__main__":
    app.run(debug=True)








