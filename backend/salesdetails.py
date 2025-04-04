from mysql.connector import Error
from datetime import datetime
from backend.transactiondetails import Transactiondetails

class Salesdetails:
    @staticmethod
    def generate_bill(conn, user_id):  # Keep user_id for filtering
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("""
                SELECT c.isbn, c.quantity, b.title, b.price
                FROM cart c
                JOIN Book b ON c.isbn = b.isbn
                WHERE c.user_id = %s
            """, (user_id,))
            cart_items = cursor.fetchall()
            print(f"Cart items: {cart_items}")  # Debug
            if not cart_items:
                return {"status": "error", "message": "Cart is empty"}

            total = 0
            items = []
            for item in cart_items:
                subtotal = item["quantity"] * item["price"]
                total += subtotal
                items.append({
                    "isbn": item["isbn"],
                    "title": item["title"],
                    "quantity": item["quantity"],
                    "price": item["price"],
                    "subtotal": subtotal
                })

            return {
                "status": "success",
                "items": items,
                "total": total,
                "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
        except Error as err:
            print(f"Error: {err}")
            return {"status": "error", "message": str(err)}
        finally:
            cursor.close()

    @staticmethod
    def process_payment(conn, username, payment_method):
        cursor = conn.cursor()
        try:
            # Generate a unique sale_id
            cursor.execute("SELECT MAX(sale_id) FROM transaction_details")
            last_sale = cursor.fetchone()
            sale_id = (last_sale[0] + 1) if last_sale and last_sale[0] is not None else 1
            

            cursor.execute("""
                SELECT c.isbn, c.quantity, b.price, b.stock, b.title
                FROM cart c
                JOIN Book b ON c.isbn = b.isbn
                WHERE c.user_id = %s;
            """, (username,))
            cart_items = cursor.fetchall()
            if not cart_items:
                return {"status": "error", "message": "Cart is empty"}

            total = 0
            items = []

            for isbn, quantity, price, current_stock, title in cart_items:
                subtotal = price * quantity
                total += subtotal
                new_stock = max(current_stock - quantity, 0)
                
                # Update book stock
                cursor.execute("UPDATE Book SET stock = %s WHERE isbn = %s", (new_stock, isbn))
                
                # Insert into transaction_details (transaction_id will auto-increment)
                cursor.execute("""
                    INSERT INTO transaction_details (sale_id, isbn, quantity_sold, subtotal, date_of_purchase)
                    VALUES (%s, %s, %s, %s, NOW())
                """, (sale_id, isbn, quantity, subtotal))
                
                items.append({
                    "isbn": isbn, 
                    "quantity": quantity, 
                    "subtotal": subtotal, 
                    "title": title, 
                    "price": price
                })

            # Clear the cart
            cursor.execute("DELETE FROM cart WHERE user_id = %s", (username,))
            conn.commit()
            print("Payment success for sale_id",sale_id)
            return {
                "status": "success",
                "sale_id": sale_id,
                "items": items,
                "total": total,
                "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "payment_method": payment_method
            }
        except Error as err:
            conn.rollback()
            print(f"Error: {err}")
            #print("sale_id",sale_id)
            return {"status": "error", "message": str(err)}
        finally:
            cursor.close()