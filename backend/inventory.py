from backend.book import Book
import random

class Inventory:
    def __init__(self, arrival_date: str, quantity_arrived: int, isbn: str,title: str,author: str,publisher: str,price: int,image_url: str):
        """Initialize inventory with arrival date, quantity, and isbn."""
        self.arrival_date=arrival_date
        self.quantity_arrived=quantity_arrived
        self.isbn=isbn
        self.title=title
        self.author=author
        self.publisher=publisher
        self.price=price
        self.image_url = image_url
        self.flag=1

    def add_to_store(self,conn):        
        """Inserts the inventory details (arrival date, quantity, isbn,image_url) into the STORE table."""
        cursor = conn.cursor(buffered=True)
        
        checkstore="SELECT title,author,publisher FROM Store WHERE isbn=%s;"
        cursor.execute(checkstore,(self.isbn,))
        storeres=cursor.fetchone()
        if(storeres and storeres[0]!=self.title):
            return {"message":f"Can't add the Book .Title of the book doesn't match"}
        if(storeres and storeres[1]!=self.author):
            return {"message":f"Can't add the Book .Author of the book doesn't match"}
        if(storeres and storeres[2]!=self.publisher):
            return {"message":f"Can't add the Book .Publisher of the book doesn't match"}
        
        checkbook="SELECT title,author,publisher FROM Book WHERE isbn=%s;"
        cursor.execute(checkbook,(self.isbn,))
        bookres=cursor.fetchone()
        if(bookres and bookres[0]!=self.title):
            return {"message":f"Can't add the Book .Title of the book doesn't match"}
        if(bookres and bookres[1]!=self.author):
            return {"message":f"Can't add the Book .Author of the book doesn't match"}
        if(bookres and bookres[2]!=self.publisher):
            return {"message":f"Can't add the Book .Publisher of the book doesn't match"}

        
        sql = "INSERT INTO Store(arrival_date, quantity_arrived, isbn, title, author, publisher, price,image_url) VALUES (%s, %s, %s, %s, %s, %s, %s,%s)"
        values = (self.arrival_date, self.quantity_arrived, self.isbn, self.title, self.author, self.publisher, self.price,self.image_url)

        cursor.execute(sql, values)
        #conn.commit()
        Inventory.update_book_stock(conn)
        
        cursor.close()

        return {"message":f"Book added into the store successfully..."}

    @staticmethod
    def display_book_stock(conn):
        """Fetches all book requests from the database""" 
        cursor = conn.cursor()
        
        # Find the Publisher for the Given Request ID
        query = "SELECT * FROM Store;"
        cursor.execute(query)
        
        rows = cursor.fetchall()    # Fetch all rows from the table

        cursor.close()

        if not rows:
            return {"message": "No books found!"}  # ✅ Return JSON response

        # Convert data into list of dictionaries
        books = [{"isbn": row[2], "title": row[3], "quantity_arrived": row[1], "arrival_date": row[0], "image_url":row[7],"flag":row[8]} for row in rows]
        return {"books": books}
    
    @staticmethod
    def update_book_stock(conn):
        """ Updates the stock quantity in the BOOK table by adding quantity_arrived to the existing stock.
            If a book with the given isbn does not exist, it calls Book.save_to_Book() to add it.
            Also updates average procurement time, resets request_date, increments freq, and sets num_required. """
    
        cursor = conn.cursor(buffered=True)

        stock_query = "SELECT isbn, quantity_arrived, title, author, publisher, price, image_url FROM Store WHERE flag>0;"
        cursor.execute(stock_query)
        stock_result = cursor.fetchall()

        if not stock_result:
            return {"message": "No stock to update."}

        for res in stock_result:
            isbn, quantity_arrived, title, author, publisher, price,image_url= res
            

            # ✅ 1️⃣ Check if the book exists in the Book table
            check_query = "SELECT COUNT(*) FROM Book WHERE isbn = %s;"
            cursor.execute(check_query, (isbn,))
            book_exists = cursor.fetchone()[0]  

            if book_exists>0:
                # ✅ 2️⃣ Update stock if the book exists
                book_query = "UPDATE Book SET stock = stock + %s WHERE isbn = %s;"
                cursor.execute(book_query, (quantity_arrived, isbn))

                spl_query = "SELECT price FROM Book WHERE isbn=%s;"
                cursor.execute(spl_query, (isbn,))
                spl_ans = cursor.fetchone()

                if spl_ans and price != spl_ans[0]:  # Ensure spl_ans is not None
                    price_query = "UPDATE Book SET price = %s WHERE isbn = %s;"
                    cursor.execute(price_query, (price, isbn))  # Use 'price' instead of 'spl_ans[0]'

            else:
                # ✅ 3️⃣ Book does not exist → Add it using Book.save_to_Book()
                rack = round(random.uniform(1, 10), 1)
                new_book = Book(isbn, title, author, publisher, price, quantity_arrived, rack, image_url)
                try:
                    new_book.save_to_Book(conn)
                except Exception as e:
                    return {"error": f"Failed to add new book: {str(e)}"}


            # ✅ 4️⃣ Calculate `d` (difference between req_date and arrival_date)
            date_diff_query = """
                SELECT DATEDIFF(s.arrival_date, IFNULL(b.request_date, s.arrival_date))
                FROM Book b
                JOIN Store s ON b.isbn = s.isbn
                WHERE b.isbn = %s AND s.flag=1;
            """
            cursor.execute(date_diff_query, (isbn,))
            date_diff_result = cursor.fetchone()

            d = date_diff_result[0] if date_diff_result and len(date_diff_result) > 0 and date_diff_result[0] is not None else 0

            # ✅ 5️⃣ Update average procurement time
            avg_query = """
                UPDATE Book
                SET average = GREATEST(((IFNULL(average, 0) * IFNULL(freq, 0)) + %s) / (IFNULL(freq, 0) + 1), 0)
                WHERE isbn = %s;
            """
            cursor.execute(avg_query, (d, isbn))

            # ✅ 6️⃣ Reset request_date to NULL
            req_query = "UPDATE Book SET request_date = NULL WHERE isbn = %s;"
            cursor.execute(req_query, (isbn,))

            # ✅ 7️⃣ Increment frequency of supply
            freq_query = "UPDATE Book SET freq = IFNULL(freq, 0) + 1 WHERE isbn = %s;"
            cursor.execute(freq_query, (isbn,))

            # ✅ 8️⃣ Reset num_required to 0
            num_query = "UPDATE Book SET num_required = GREATEST(num_required - %s,0) WHERE isbn = %s;"
            cursor.execute(num_query, (quantity_arrived,isbn))

            set_query="""
                UPDATE Store
                SET flag = 0
                WHERE isbn = %s;
            """
            cursor.execute(set_query, (isbn,))

        conn.commit()
        cursor.close()

        return {"message": "The stock has been updated successfully."}
    
    @staticmethod
    def delete_from_Store(conn, isbn, arrival_date):
        """Delete a book from MySQL by isbn"""
        cursor = conn.cursor(buffered=True)
        
        # Check if the book exists
        book_sql="SELECT * FROM Store WHERE isbn = %s;"
        cursor.execute(book_sql, (isbn,))
        check=cursor.fetchone()
        if not check:
            return {"message":f"Book with isbn {isbn} not found in Store."}


        check_sql = "SELECT * FROM Store WHERE isbn = %s and arrival_date=%s;"
        cursor.execute(check_sql, (isbn,arrival_date))
        book = cursor.fetchone()

        if book:
            sql = "DELETE FROM Store WHERE isbn = %s and arrival_date=%s;"

            cursor.execute(sql, (isbn,arrival_date))
            conn.commit()

            message = {"message": f"Book with isbn {isbn} recieved on {arrival_date} deleted successfully from Store!"}
        else:
            message = {"message": f"Book with isbn {isbn} has not  arrived on {arrival_date}."}

        cursor.close()
        return message

