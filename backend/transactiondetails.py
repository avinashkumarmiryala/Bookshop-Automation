from mysql.connector import Error
from backend.book import Book

class Transactiondetails:
    def __init__(self, transaction_id, sale_id, isbn, quantity_sold, subtotal, date_of_purchase):
        self.transaction_id = transaction_id
        self.sale_id = sale_id
        self.isbn = isbn
        self.quantity_sold = quantity_sold
        self.subtotal = subtotal
        self.date_of_purchase = date_of_purchase

    @staticmethod
    def add_to_cart(conn, isbn, quantity,user_id):
        cursor = conn.cursor()
        try:
            # Get total stock and sum of quantities in all carts for this ISBN
            cursor.execute("""
                SELECT stock, 
                    COALESCE((SELECT SUM(quantity) FROM cart WHERE isbn = %s AND user_id = %s), 0)
                FROM Book WHERE isbn = %s;
            """, (isbn, user_id,isbn))
            result = cursor.fetchone()
            if not result:
                return {"message": f"❌ Error: Book with ISBN {isbn} not found.", "status": "error"}

            stock_total = result[0]
            total_in_carts = result[1]
            stock_available = stock_total - total_in_carts  # What's left after all carts
            original_quantity = quantity  # Store the requested amount

            # If no stock is available after accounting for carts
            if stock_available <= 0:
                cursor.execute("UPDATE Book SET num_required = num_required + %s WHERE isbn = %s", (quantity, isbn))
                conn.commit()
                return {
                    "message": f"⚠️ '{isbn}' is fully reserved or out of stock! Your request for {quantity} copies has been recorded.",
                    "status": "out_of_stock"
                }

            # Cap the quantity to what's available
            flag = 0
            if quantity > stock_available:
                quantity = stock_available
                flag = 1

            cursor.execute("SELECT DISTINCT sale_id FROM cart WHERE user_id = %s", (user_id,))
            existing_sale = cursor.fetchone()
            if existing_sale:
                sale_id = existing_sale[0]
            else:
                cursor.execute("SELECT MAX(sale_id) FROM transaction_details")
                last_sale = cursor.fetchone()
                sale_id = last_sale[0] + 1 if last_sale and last_sale[0] is not None else 1

            cursor.execute("SELECT quantity FROM cart WHERE sale_id = %s AND isbn = %s AND user_id = %s", (sale_id, isbn,user_id))
            existing_item = cursor.fetchone()

            if existing_item:
                new_quantity = existing_item[0] + quantity
                cursor.execute("UPDATE cart SET quantity = %s WHERE sale_id = %s AND isbn = %s AND user_id = %s",
                            (new_quantity, sale_id, isbn,user_id))
            else:
                cursor.execute("INSERT INTO cart (sale_id, isbn, quantity,user_id) VALUES (%s, %s, %s, %s)",
                            (sale_id, isbn, quantity,user_id))

            conn.commit()
            
            if flag == 0:
                return {"message": f"✅ Added {quantity} copies of ISBN {isbn} to cart (Sale ID: {sale_id}).", "status": "success"}
            else:
                missing_quantity = original_quantity - stock_available
                cursor.execute("UPDATE Book SET num_required = num_required + %s WHERE isbn = %s", (missing_quantity, isbn))
                conn.commit()
                return {
                    "message": f"✅ Added {stock_available} copies to cart. The remaining {missing_quantity} copies have been requested.",
                    "status": "warning"
                }
        except Error as err:
            conn.rollback()
            return {"message": f"❌ Database error: {err}", "status": "error"}
        finally:
            cursor.close()

    # Other methods (view_cart, update_cart_item, etc.) remain unchanged...

    @staticmethod
    def transactions_statistics(conn, isbn, start_date, end_date):
        """Fetch transaction statistics for a given ISBN"""
        cursor = conn.cursor()
        query = """SELECT SUM(quantity_sold) FROM transaction_details WHERE isbn = %s AND date_of_purchase BETWEEN %s AND %s"""
        cursor.execute(query, (isbn, start_date, end_date))
        result = cursor.fetchone()
        check="""SELECT title FROM Book WHERE isbn=%s"""
        cursor.execute(check,(isbn,))
        checkres= cursor.fetchone()
        if not checkres:
            return { "message":f"The book with {isbn} is not being sold currently..."}
        cursor.close()
        return {"isbn": isbn, "total_sold": result[0] if result and result[0] is not None else 0}

    @staticmethod
    def view_cart(conn, user_id):
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("""
                SELECT c.isbn, c.quantity, b.title, b.author, b.price, b.image_url
                FROM cart c
                JOIN Book b ON c.isbn = b.isbn
                WHERE c.user_id = %s
            """, (user_id,))
            cart_items = cursor.fetchall()
            print(f"Cart items fetched: {cart_items}")  # Debug
            return cart_items  # Return list for /view_cart
        except Error as err:
            print(f"Error: {err}")
            return []
        finally:
            cursor.close()

    @staticmethod
    def update_cart(conn, isbn, quantity, user_id):  # Added user_id
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT sale_id, quantity FROM cart WHERE isbn = %s AND user_id = %s", (isbn, user_id))
            cart_item = cursor.fetchone()
            if not cart_item:
                return {"message": f"Item with ISBN {isbn} not in cart", "status": "error"}

            sale_id, current_quantity = cart_item
            if quantity <= 0:
                cursor.execute("DELETE FROM cart WHERE isbn = %s AND sale_id = %s AND user_id = %s", (isbn, sale_id, user_id))
                conn.commit()
                return {"message": f"Removed item with ISBN {isbn}", "status": "success"}

            cursor.execute("SELECT stock FROM Book WHERE isbn = %s", (isbn,))
            stock = cursor.fetchone()[0]
            if quantity > stock:
                quantity = stock
                message = f"Adjusted to available stock ({stock})"
            else:
                message = f"Updated to {quantity}"
            cursor.execute("UPDATE cart SET quantity = %s WHERE isbn = %s AND sale_id = %s AND user_id = %s", 
                          (quantity, isbn, sale_id, user_id))
            conn.commit()
            return {"message": message, "status": "success"}
        except Error as err:
            conn.rollback()
            return {"message": f"Error: {err}", "status": "error"}
        finally:
            cursor.close()
    @staticmethod
    def remove_from_cart(conn, isbn):
        """Remove an item from cart"""
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM cart WHERE isbn = %s", (isbn,))
            conn.commit()
            return {"message": f"Item removed from cart", "status": "success"}
        except Error as err:
            conn.rollback()
            return {"message": f"Error removing item: {err}", "status": "error"}
        finally:
            cursor.close()