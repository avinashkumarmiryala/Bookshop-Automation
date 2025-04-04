class Book:
    def __init__(self, isbn, title, author, publisher, price, stock, rack, image_url):
        self.isbn = isbn
        self.title = title
        self.author = author
        self.publisher = publisher
        self.price = price
        self.stock = stock
        self.rack = rack
        self.freq = 0
        self.num_required = 0
        self.request_date = None
        self.average = 0
        self.image_url = image_url  # ✅ Added Image URL
        self.flag=1
    def save_to_Book(self, conn):
        """Save book details into MySQL"""
        cursor = conn.cursor()

        sql = """
            INSERT INTO Book (isbn, title, author, publisher, price, stock, rack, freq, num_required, request_date, average, image_url)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = (self.isbn, self.title, self.author, self.publisher, self.price, self.stock, self.rack, self.freq, self.num_required, self.request_date, self.average, self.image_url)

        cursor.execute(sql, values)
        conn.commit()

        cursor.close()
        return {"message": f"Book '{self.title}' added successfully!"}

    
    @staticmethod
    def delete_from_Book(conn,isbn):
        """Delete a book from MySQL by isbn"""
        cursor = conn.cursor()

        check="SELECT * FROM Book WHERE isbn = %s;"
        cursor.execute(check,(isbn,))
        res=cursor.fetchone()
        if(res):
            sql = "DELETE FROM Book WHERE isbn = %s;"
            cursor.execute(sql, (isbn,))
            conn.commit()
            cursor.close()
            return {"message": f"Book with isbn {isbn} deleted successfully!"}  # ✅ Fixed

        else:
            conn.commit()
            cursor.close()
            return {"message": f"Book with isbn {isbn} not found in the Shop!"}  # ✅ Fixed
    @staticmethod
    def edit_price(conn, isbn, new_price):
            """Update the price of a book given its ISBN."""
            cursor = conn.cursor()

            check_query = "SELECT * FROM Book WHERE isbn = %s;"
            cursor.execute(check_query, (isbn,))
            book = cursor.fetchone()

            if not book:
                cursor.close()
                return {"message": "Book not found!"}

            update_query = "UPDATE Book SET price = %s WHERE isbn = %s;"
            cursor.execute(update_query, (new_price, isbn))
            conn.commit()

            cursor.close()
            return {"message": f"Price updated successfully for ISBN {isbn}!"}

    @staticmethod
    def search_by_title(conn, title):
        """Search for all books with a matching title (partial match)"""
        cursor = conn.cursor()

        sql = "SELECT isbn, title, author, stock, rack, image_url FROM Book WHERE title LIKE %s"
        cursor.execute(sql, (f"%{title}%",))
        books = cursor.fetchall()

        cursor.close()

        if books:
            return [
                {
                    "isbn": book[0],
                    "title": book[1],
                    "author": book[2],
                    "stock": book[3],
                    "rack": book[4],
                    "image_url": book[5]  # ✅ Added Image URL
                }
                for book in books
            ]
        return {"message": "No books found."}

    @staticmethod
    def search_by_author(conn, author):
        """Search for all books with a matching author (partial match)"""
        cursor = conn.cursor()

        sql = "SELECT isbn, title, author, stock, rack, image_url FROM Book WHERE author LIKE %s"
        cursor.execute(sql, (f"%{author}%",))
        books = cursor.fetchall()

        cursor.close()

        if books:
            return [
                {
                    "isbn": book[0],
                    "title": book[1],
                    "author": book[2],
                    "stock": book[3],
                    "rack": book[4],
                    "image_url": book[5]  # ✅ Added Image URL
                }
                for book in books
            ]
        return {"message": "No books found."}

    


    @staticmethod
    def get_all_books(conn):
        """Fetches all vendor details from the database and returns as JSON."""  
        cursor = conn.cursor()

        query = "SELECT * FROM Book;"
        cursor.execute(query)
        
        rows = cursor.fetchall()
        cursor.close()
        
        if not rows:
            return {"message": "No books found!"}  # ✅ Return JSON response

        # Convert data into list of dictionaries
        books = [{"isbn": row[0], "title": row[1], "author": row[2], "publisher": row[3], "price": row[4], "stock": row[5], "rack":row[6],"freq":row[7],"num_required":row[8],"request_date":row[9],"average":row[10],"image_url":row[11]} for row in rows]
        return {"message": books}
