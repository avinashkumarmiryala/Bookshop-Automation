import unittest
from unittest.mock import MagicMock
from backend.bookrequest import BookRequest  # Replace 'book_request' with the actual module name

class TestBookRequestMethods(unittest.TestCase):

    def setUp(self):
        """Set up a mock database connection before each test."""
        self.mock_conn = MagicMock()
        self.mock_cursor = MagicMock()
        self.mock_conn.cursor.return_value = self.mock_cursor


    def test_save_to_conn_existing_book(self):
        """Test the case where a book already exists in the database and can't be added again."""
        book_request = BookRequest(request_id=None, isbn="1234567890", title="Test Book", 
                                author="Test Author", publisher="Test Publisher", num_required=5)

        # Mock the database response for checking if the book already exists
        self.mock_cursor.fetchone.return_value = (10,)  # Simulating the existence of the book with num_required = 10

        # Mock the database response for checking the BookRequest table
        self.mock_cursor.execute.return_value = None

        result = book_request.save_to_conn(self.mock_conn)
        
        # Here we check for the "already exists" message
        self.assertEqual(result['message'], "This book already exists! Can't add the same book again...")
        self.mock_cursor.execute.assert_called()  # Ensure the execute method was called


    def test_delete_request_success(self):
        """Test deleting an existing book request."""
        book_request = BookRequest(request_id=None, isbn="1234567890", title="Test Book", 
                                   author="Test Author", publisher="Test Publisher", num_required=5)

        # Mock the database response for the request to be deleted
        self.mock_cursor.fetchone.return_value = ("1234567890", "Test Book", "Test Author", "Test Publisher", 5, 5)
        
        result = book_request.delete_request(self.mock_conn, "1234567890", "2025-04-01")
        self.assertEqual(result['message'], "Book with isbn 1234567890 recieved on 2025-04-01 deleted successfully from BookRequest!")
        self.mock_cursor.execute.assert_called_with("DELETE FROM BookRequest WHERE isbn = %s and request_date=%s;", ("1234567890", "2025-04-01"))

    def test_delete_request_not_found(self):
        """Test when the book request does not exist."""
        book_request = BookRequest(request_id=None, isbn="1234567890", title="Test Book", 
                                   author="Test Author", publisher="Test Publisher", num_required=5)

        # Mock the database response for a book not found
        self.mock_cursor.fetchone.return_value = None
        
        result = book_request.delete_request(self.mock_conn, "1234567890", "2025-04-01")
        self.assertEqual(result['message'], "Book with isbn 1234567890 not found in Book Request table.")
        
    def test_make_request(self):
        """Test fetching all book requests with vendor details."""
        book_request = BookRequest(request_id=None, isbn="1234567890", title="Test Book", 
                                   author="Test Author", publisher="Test Publisher", num_required=5)
        
        # Mock the database response for publishers
        self.mock_cursor.fetchall.return_value = [("Test Publisher",)]
        
        # Mock the vendor details query
        self.mock_cursor.fetchone.return_value = ("V001", "Vendor Name", "Vendor Contact", "Vendor Address")
        
        result = book_request.make_request(self.mock_conn)
        self.assertEqual(result['results'][0]['publisher'], "Test Publisher")
        self.assertEqual(result['results'][0]['vendor_details']['vendor_name'], "Vendor Name")

    def test_make_request_no_vendor(self):
        """Test when no vendor is found for a publisher."""
        book_request = BookRequest(request_id=None, isbn="1234567890", title="Test Book", 
                                   author="Test Author", publisher="Test Publisher", num_required=5)
        
        # Mock the database response for publishers
        self.mock_cursor.fetchall.return_value = [("Test Publisher",)]
        
        # Mock the vendor details query returning None (no vendor)
        self.mock_cursor.fetchone.return_value = None
        
        result = book_request.make_request(self.mock_conn)
        self.assertEqual(result['results'][0]['publisher'], "Test Publisher")
        self.assertEqual(result['results'][0]['message'], "No vendor found for publisher 'Test Publisher'.")

    def test_get_all_requests(self):
        """Test fetching all book requests."""
        book_request = BookRequest(request_id=None, isbn="1234567890", title="Test Book", 
                                   author="Test Author", publisher="Test Publisher", num_required=5)
        
        # Mock the database response for fetching requests
        self.mock_cursor.fetchall.return_value = [
            (1, "1234567890", "Test Book", "Test Author", "Test Publisher", 5)
        ]
        
        result = book_request.get_all_requests(self.mock_conn)
        self.assertEqual(result['message'], "📚 Book Requests")
        self.assertEqual(result['requests'][0]['isbn'], "1234567890")

    def test_get_all_requests_no_data(self):
        """Test when no book requests exist."""
        book_request = BookRequest(request_id=None, isbn="1234567890", title="Test Book", 
                                   author="Test Author", publisher="Test Publisher", num_required=5)
        
        # Mock the database response for no requests
        self.mock_cursor.fetchall.return_value = []
        
        result = book_request.get_all_requests(self.mock_conn)
        self.assertEqual(result['message'], "📌 No book requests found.")

    def test_make_request_from_book(self):
        """Test making requests based on books with pending requests."""
        book_request = BookRequest(request_id=None, isbn="1234567890", title="Test Book", 
                                   author="Test Author", publisher="Test Publisher", num_required=5)
        
        # Mock the database response for publishers with pending requests
        self.mock_cursor.fetchall.return_value = [("Test Publisher",)]
        
        # Mock the vendor details query
        self.mock_cursor.fetchone.return_value = ("V001", "Vendor Name", "Vendor Contact", "Vendor Address")
        
        result = book_request.make_request_from_book(self.mock_conn)
        self.assertEqual(result['results'][0]['publisher'], "Test Publisher")
        self.assertEqual(result['results'][0]['vendor_details']['vendor_name'], "Vendor Name")

    def test_make_request_from_book_no_vendor(self):
        """Test when no vendor is found for a book's publisher."""
        book_request = BookRequest(request_id=None, isbn="1234567890", title="Test Book", 
                                   author="Test Author", publisher="Test Publisher", num_required=5)
        
        # Mock the database response for publishers with pending requests
        self.mock_cursor.fetchall.return_value = [("Test Publisher",)]
        
        # Mock the vendor details query returning None (no vendor)
        self.mock_cursor.fetchone.return_value = None
        
        result = book_request.make_request_from_book(self.mock_conn)
        self.assertEqual(result['results'][0]['publisher'], "Test Publisher")
        self.assertEqual(result['results'][0]['message'], "No vendor found for publisher 'Test Publisher'.")

if __name__ == '__main__':
    unittest.main()
