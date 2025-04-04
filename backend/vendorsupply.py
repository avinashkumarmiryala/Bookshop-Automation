class VendorSupply:
    def __init__(self, vendor_id= None, vendor_name=None, vendor_address=None, contact_info=None, publisher=None):
        """Constructor to initialize VendorSupply object."""
        self.vendor_id = vendor_id
        self.vendor_name = vendor_name
        self.vendor_address = vendor_address
        self.contact_info = contact_info
        self.publisher = publisher

    def add_details(self,conn):
        """Inserts the vendor supply details into the database."""  
        cursor = conn.cursor()
        checkvs="SELECT * FROM VendorSupply WHERE publisher=%s;"
        checkother="SELECT * FROM VendorSupply WHERE vendor_name=%s;"
        cursor.execute(checkvs,(self.publisher,))
        vsres=cursor.fetchone()
        if(vsres):
            return {"message":f"A Vendor exists for the given Publisher...\n Can't add a new vendor."}
        cursor.execute(checkother,(self.vendor_name,))
        splres=cursor.fetchone()
        if(splres):
            return {"message":f"A Publisher exists for the given Vendor...\n Can't add a new publisher."}

        sql = "INSERT INTO VendorSupply (vendor_name, vendor_address, contact_info, publisher) VALUES (%s, %s, %s, %s)"
        values = (self.vendor_name, self.vendor_address, self.contact_info, self.publisher)

        cursor.execute(sql, values)
        conn.commit()

        cursor.close()
        
        return {"message": "Vendor details added successfully!"}  # ✅ Return JSON response

    @staticmethod
    def delete_from_Vendor_Supply(conn,publisher):
        """Deletes a vendor by publisher."""  
        cursor = conn.cursor()

        test="SELECT vendor_name FROM VendorSupply WHERE publisher=%s"
        cursor.execute(test,(publisher,))
        testres=cursor.fetchone()
        if not testres:
            return {"message":f"No Vendors found for the given publisher"}
           
        sql = "DELETE FROM VendorSupply WHERE publisher = %s"
        cursor.execute(sql, (publisher,))

        conn.commit()
        cursor.close()
        
        return {"message": f"Vendor for publisher {publisher} deleted successfully!"}  # ✅ Return JSON response

    @staticmethod
    def get_all_vendors(conn):
        """Fetches all vendor details from the database and returns as JSON."""  
        cursor = conn.cursor()

        query = "SELECT * FROM VendorSupply;"
        cursor.execute(query)
        
        rows = cursor.fetchall()
        cursor.close()
        
        if not rows:
            return {"message": "No vendors found!"}  # ✅ Return JSON response

        # Convert data into list of dictionaries
        vendors = [{"vendor_id": row[0], "vendor_name": row[1], "vendor_address": row[2], "contact_info": row[3], "publisher": row[4]} for row in rows]
        return {"message": vendors}

