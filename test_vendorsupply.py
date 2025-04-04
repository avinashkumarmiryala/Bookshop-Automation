import unittest
from unittest.mock import MagicMock
from backend.vendorsupply import VendorSupply

class TestVendorSupply(unittest.TestCase):
    def setUp(self):
        self.conn = MagicMock()
        self.cursor = MagicMock()
        self.conn.cursor.return_value = self.cursor

    def test_add_details_success(self):
        self.cursor.fetchone.side_effect = [None, None]  # No existing vendor or publisher
        vendor = VendorSupply("V001", "Test Vendor", "123 Street", "9876543210", "Test Publisher")
        
        result = vendor.add_details(self.conn)
        self.cursor.execute.assert_called()  # Ensure SQL execution
        self.conn.commit.assert_called()
        self.assertEqual(result, {"message": "Vendor details added successfully!"})
    
    def test_add_details_existing_vendor(self):
        self.cursor.fetchone.side_effect = [("Existing Vendor",), None]  # Existing vendor
        vendor = VendorSupply("V001", "Existing Vendor", "123 Street", "9876543210", "Test Publisher")
        
        result = vendor.add_details(self.conn)
        self.assertEqual(result, {"message": "A Vendor exists for the given Publisher...\n Can't add a new vendor."})
    
    def test_add_details_existing_publisher(self):
        self.cursor.fetchone.side_effect = [None, ("Existing Publisher",)]  # Existing publisher
        vendor = VendorSupply("V001", "Test Vendor", "123 Street", "9876543210", "Existing Publisher")
        
        result = vendor.add_details(self.conn)
        self.assertEqual(result, {"message": "A Publisher exists for the given Vendor...\n Can't add a new publisher."})
    
    def test_delete_from_Vendor_Supply_success(self):
        self.cursor.fetchone.return_value = ("Test Vendor",)
        
        result = VendorSupply.delete_from_Vendor_Supply(self.conn, "Test Publisher")
        self.cursor.execute.assert_called()
        self.conn.commit.assert_called()
        self.assertEqual(result, {"message": "Vendor for publisher Test Publisher deleted successfully!"})
    
    def test_delete_from_Vendor_Supply_no_vendor(self):
        self.cursor.fetchone.return_value = None
        
        result = VendorSupply.delete_from_Vendor_Supply(self.conn, "Unknown Publisher")
        self.assertEqual(result, {"message": "No Vendors found for the given publisher"})
    
    def test_get_all_vendors_success(self):
        self.cursor.fetchall.return_value = [(1, "Vendor1", "Address1", "12345", "Pub1")]
        
        result = VendorSupply.get_all_vendors(self.conn)
        self.assertEqual(result, {"message": [{"vendor_id": 1, "vendor_name": "Vendor1", "vendor_address": "Address1", "contact_info": "12345", "publisher": "Pub1"}]})
    
    def test_get_all_vendors_no_vendors(self):
        self.cursor.fetchall.return_value = []
        
        result = VendorSupply.get_all_vendors(self.conn)
        self.assertEqual(result, {"message": "No vendors found!"})

if __name__ == "__main__":
    unittest.main()
