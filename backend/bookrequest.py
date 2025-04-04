from backend.book import Book
from backend.vendorsupply import VendorSupply

class BookRequest:
    def __init__(self, request_id:int, isbn:str, title:str, author:str, publisher:str, num_required:int):
        """Constructor: Initializes a BookRequest object"""
        self.request_id=request_id
        self.isbn= isbn
        self.title = title
        self.author = author
        self.publisher = publisher
        self.num_required= num_required
        self.flag=1

    # Database Operations
    def save_to_conn(self, conn):
        """Saves the request to the database, increments num_required if ISBN exists."""
        cursor = conn.cursor()

        def_query = "SELECT * FROM Book WHERE isbn = %s"
        cursor.execute(def_query, (self.isbn,))
        res = cursor.fetchone()
        if res:
            return{"message":"This book already exists! Can't add the same book again..."}

        # ✅ Check if ISBN already exists in BookRequest
        check_query = "SELECT num_required FROM BookRequest WHERE isbn = %s"
        cursor.execute(check_query, (self.isbn,))
        existing_request = cursor.fetchone()
        print(type(existing_request))

        if existing_request:
            # ✅ ISBN exists → Increment num_required
            num_required = int(existing_request[0]) + int(self.num_required)
            print(type(num_required))
            update_query = "UPDATE BookRequest SET num_required = %s WHERE isbn = %s"
            cursor.execute(update_query, (num_required, self.isbn))
            message = f"Updated request for '{self.title}': Total requested = {num_required}"

        else:
            # ✅ ISBN does not exist → Insert new request
            insert_query = "INSERT INTO BookRequest (isbn, title, author, publisher, num_required) VALUES (%s, %s, %s, %s, %s)"
            values = (self.isbn, self.title, self.author, self.publisher, self.num_required)
            cursor.execute(insert_query, values)
            message = f"New request added for '{self.title}'"

        conn.commit()
        cursor.close()
        
        return {"message": message}

    @staticmethod
    def delete_request(conn, isbn, request_date):
        """Delete a book from MySQL by isbn"""
        cursor = conn.cursor(buffered=True)
        
        # Check if the book exists
        book_sql="SELECT * FROM BookRequest WHERE isbn = %s;"
        cursor.execute(book_sql, (isbn,))
        check=cursor.fetchone()
        if not check:
            return {"message":f"Book with isbn {isbn} not found in Book Request table."}


        check_sql = "SELECT * FROM BookRequest WHERE isbn = %s and request_date=%s;"
        cursor.execute(check_sql, (isbn,request_date))
        book = cursor.fetchone()

        if book:
            sql = "DELETE FROM BookRequest WHERE isbn = %s and request_date=%s;"

            cursor.execute(sql, (isbn,request_date))
            conn.commit()

            message = {"message": f"Book with isbn {isbn} recieved on {request_date} deleted successfully from BookRequest!"}
        else:
            message = {"message": f"Book with isbn {isbn} has not been requested on {request_date}."}

        cursor.close()
        return message   
    

    @staticmethod
    def make_request(conn):
        """Fetches all BookRequests from the database"""
        cursor = conn.cursor()

        # Find all Publishers
        publisher_query = "SELECT publisher FROM BookRequest WHERE flag=1;"
        cursor.execute(publisher_query)
        publisher_results = cursor.fetchall()

        results = []  # List to store all responses

        for publisher in publisher_results:
            # Retrieve Vendor (vendor) Details Using Publisher
            vendor_query = """
                SELECT vendor_id, vendor_name, contact_info, vendor_address
                FROM VendorSupply
                WHERE publisher = %s;
            """
            cursor.execute(vendor_query, (publisher[0],))
            vendor_result = cursor.fetchone()

            if vendor_result:
                set_query="""
                    UPDATE BookRequest
                    SET flag = 0
                    WHERE publisher = %s;
                """
                cursor.execute(set_query, (publisher[0],))
                conn.commit()

                vendor_id, vendor_name, contact_info, vendor_address = vendor_result
                results.append({
                    "publisher": publisher[0],
                    "vendor_details": {
                        "vendor_name": vendor_name,
                        "vendor_id": vendor_id,
                        "contact_info": contact_info,
                        "vendor_address": vendor_address
                    }
                })
            else:
                results.append({
                    "publisher": publisher[0],
                    "message": f"No vendor found for publisher '{publisher[0]}'."
                })

        cursor.close()

        if results:
            return {"results": results}
        else:
            return {"message": "No book requests found."}

    
    @staticmethod
    def get_all_requests(conn):
        """Fetches all book requests from the database""" 
        cursor = conn.cursor()
        
        query = "SELECT * FROM BookRequest WHERE flag>0;"
        cursor.execute(query)
        
        rows = cursor.fetchall()  # Fetch all rows from the table
        flag=0
        if rows:
            flag=1
        cursor.close()

        if(flag):
            requests = [{"request_id": row[0], "isbn": row[1], "title": row[2], "num_required": row[5]} for row in rows]
            return {"message": "📚 Book Requests", "requests": requests}
           
        else:
            return {"message":"📌 No book requests found."}     
    
    @staticmethod
    def make_request_from_book(conn): 
        cursor = conn.cursor()
        
        # ✅ Get all publishers for books that have pending requests
        publisher_query = "SELECT publisher FROM Book WHERE num_required > 0 AND flag = 1;"
        cursor.execute(publisher_query)
        publisher_results = cursor.fetchall()  # Returns a list of tuples
        
        results=[]
        for publisher in publisher_results:
            # Retrieve Vendor (vendor) Details Using Publisher
            vendor_query = """
                SELECT vendor_id, vendor_name, contact_info, vendor_address
                FROM VendorSupply
                WHERE publisher = %s;
            """
            cursor.execute(vendor_query, (publisher[0],))
            vendor_result = cursor.fetchone()

            if vendor_result:
                set_query="""
                    UPDATE Book
                    SET flag = 0
                    WHERE publisher = %s;
                """
                cursor.execute(set_query, (publisher[0],))
                conn.commit()

                vendor_id, vendor_name, contact_info, vendor_address = vendor_result
                results.append({
                    "publisher": publisher[0],
                    "vendor_details": {
                        "vendor_name": vendor_name,
                        "vendor_id": vendor_id,
                        "contact_info": contact_info,
                        "vendor_address": vendor_address
                    }
                })
            else:
                results.append({
                    "publisher": publisher[0],
                    "message": f"No vendor found for publisher '{publisher[0]}'."
                })

        cursor.close()

        if results:
            return {"results": results}
        else:
            return {"message": "No book requests found."}
        
        
