import unittest
from unittest.mock import MagicMock, patch
from backend.inventory import Inventory

class TestInventory(unittest.TestCase):
    
    def setUp(self):
        self.conn = MagicMock()
        self.cursor = self.conn.cursor.return_value
        
        self.inventory = Inventory(
            arrival_date="2025-03-30",
            quantity_arrived=10,
            isbn="1234567890",
            title="Test Book",
            author="Test Author",
            publisher="Test Publisher",
            price=500,
            image_url="test_image.jpg"
        )
    
    def test_add_to_store_success(self):
        # No existing book in Store or Book tables
        self.cursor.fetchone.side_effect = [None, None]
        
        result = self.inventory.add_to_store(self.conn)
        
        self.cursor.execute.assert_called()
        self.conn.commit.assert_called_once()
        self.assertEqual(result, {"message": "Book added into the store successfully..."})
    
    def test_add_to_store_title_mismatch(self):
        # Book exists in store but title does not match
        self.cursor.fetchone.side_effect = [("Wrong Title", "Test Author", "Test Publisher"), None]
        
        result = self.inventory.add_to_store(self.conn)
        
        self.assertEqual(result, {"message": "Can't add the Book .Title of the book doesn't match"})
    
    def test_display_book_stock_with_data(self):
        # Mocking data retrieval
        self.cursor.fetchall.return_value = [("2025-03-30", 10, "1234567890", "Test Book", "Test Author", "Test Publisher", 500, "test_image.jpg",1)]
        
        result = Inventory.display_book_stock(self.conn)
        
        self.assertEqual(result, {"books": [{"isbn": "1234567890", "title": "Test Book", "quantity_arrived": 10, "arrival_date": "2025-03-30", "image_url":"test_image.jpg","flag": 1}]})
    
    def test_display_book_stock_empty(self):
        self.cursor.fetchall.return_value = []
        
        result = Inventory.display_book_stock(self.conn)
        
        self.assertEqual(result, {"message": "No books found!"})
    
    def test_update_book_stock_success(self):
        self.cursor.fetchall.return_value = [("1234567890", 10, "Test Book", "Test Author", "Test Publisher", 500, "test_image.jpg")]
        self.cursor.fetchone.side_effect = [(1,), (450,), (5,), (None,)]
        
        result = Inventory.update_book_stock(self.conn)
        
        self.cursor.execute.assert_called()
        self.conn.commit.assert_called_once()
        self.assertEqual(result, {"message": "The stock has been updated successfully."})
    
    def test_update_book_stock_no_stock(self):
        self.cursor.fetchall.return_value = []
        
        result = Inventory.update_book_stock(self.conn)
        
        self.assertEqual(result, {"message": "No stock to update."})
    
    def test_delete_from_store_success(self):
        self.cursor.fetchone.side_effect = [("1234567890", "2025-03-30"), ("1234567890", "2025-03-30")]
        
        result = Inventory.delete_from_Store(self.conn, "1234567890", "2025-03-30")
        
        self.cursor.execute.assert_called()
        self.conn.commit.assert_called_once()
        self.assertEqual(result, {"message": "Book with isbn 1234567890 recieved on 2025-03-30 deleted successfully from Store!"})
    
    def test_delete_from_store_not_found(self):
        self.cursor.fetchone.return_value = None
        
        result = Inventory.delete_from_Store(self.conn, "9999999999", "2025-03-30")
        
        self.assertEqual(result, {"message": "Book with isbn 9999999999 not found in Store."})
    
    def test_delete_from_store_wrong_date(self):
        self.cursor.fetchone.side_effect = [("1234567890", "2025-03-29"), None]
        
        result = Inventory.delete_from_Store(self.conn, "1234567890", "2025-03-30")
        
        self.assertEqual(result, {"message": "Book with isbn 1234567890 has not  arrived on 2025-03-30."})

if __name__ == "__main__":
    unittest.main()
