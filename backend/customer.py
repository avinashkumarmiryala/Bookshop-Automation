#add customer
class customer:
    def __init__(self, username, passwd, customer_name, contact_info, customer_address):
        self.username = username
        self.passwd = passwd
        self.customer_name = customer_name
        self.contact_info = contact_info
        self.customer_address = customer_address
    
    def add_customer(self,conn):
        """Inserts the vendor supply details into the database."""  
        cursor = conn.cursor()

        sql = "INSERT INTO customer (username, passwd, customer_name, contact_info, customer_address) VALUES (%s, %s, %s, %s, %s)"
        values = (self.username, self.passwd, self.customer_name, self.contact_info, self.customer_address)

        cursor.execute(sql, values)
        conn.commit()

        cursor.close()
        
        return {"message": "Customer details added successfully!"}  # ✅ Return JSON response 