import unittest
from unittest.mock import MagicMock
from backend.book import Book  # Replace 'your_module' with the actual module name

class TestBookMethods(unittest.TestCase):

    def setUp(self):
        """Set up a mock database connection before each test."""
        self.mock_conn = MagicMock()
        self.mock_cursor = MagicMock()
        self.mock_conn.cursor.return_value = self.mock_cursor

    def test_save_to_Book(self):
        """Test saving a book to the database."""
        book = Book(isbn="1234567890", title="Test Book", author="Test Author", publisher="Test Publisher",
                    price=19.99, stock=10, rack="A1", image_url="http://example.com/image.jpg")
        
        self.mock_cursor.execute.return_value = None
        self.mock_conn.commit.return_value = None
        
        result = book.save_to_Book(self.mock_conn)
        self.assertEqual(result['message'], "Book 'Test Book' added successfully!")
        self.mock_cursor.execute.assert_called_once()  # Check if the execute method was called
        self.mock_conn.commit.assert_called_once()  # Check if commit was called

    def test_delete_from_Book(self):
        """Test deleting a book from the database by ISBN."""
        book = Book(isbn="1234567890", title="Test Book", author="Test Author", publisher="Test Publisher",
                    price=19.99, stock=10, rack="A1", image_url="http://example.com/image.jpg")

        # Mock the database response
        self.mock_cursor.fetchone.return_value = ("1234567890", "Test Book", "Test Author", "Test Publisher", 19.99, 10, "A1", 0, 0, None, 0, "http://example.com/image.jpg")
        
        result = book.delete_from_Book(self.mock_conn, "1234567890")
        self.assertEqual(result['message'], "Book with isbn 1234567890 deleted successfully!")
        self.mock_cursor.execute.assert_called_with("DELETE FROM Book WHERE isbn = %s;", ("1234567890",))

        # Test for book not found
        self.mock_cursor.fetchone.return_value = None
        result = book.delete_from_Book(self.mock_conn, "1234567890")
        self.assertEqual(result['message'], "Book with isbn 1234567890 not found in the Shop!")

    def test_edit_price(self):
        """Test updating the price of a book."""
        book = Book(isbn="1234567890", title="Test Book", author="Test Author", publisher="Test Publisher",
                    price=19.99, stock=10, rack="A1", image_url="http://example.com/image.jpg")
        
        # Mock the database response
        self.mock_cursor.fetchone.return_value = ("1234567890", "Test Book", "Test Author", "Test Publisher", 19.99, 10, "A1", 0, 0, None, 0, "http://example.com/image.jpg")
        
        result = book.edit_price(self.mock_conn, "1234567890", 25.99)
        self.assertEqual(result['message'], "Price updated successfully for ISBN 1234567890!")
        self.mock_cursor.execute.assert_called_with("UPDATE Book SET price = %s WHERE isbn = %s;", (25.99, "1234567890"))

        # Test for book not found
        self.mock_cursor.fetchone.return_value = None
        result = book.edit_price(self.mock_conn, "1234567890", 25.99)
        self.assertEqual(result['message'], "Book not found!")

    def test_search_by_title(self):
        """Test searching for books by title."""
        book = Book(isbn="1234567890", title="Test Book", author="Test Author", publisher="Test Publisher",
                    price=19.99, stock=10, rack="A1", image_url="http://example.com/image.jpg")
        
        # Mock the database response
        self.mock_cursor.fetchall.return_value = [
            ("1234567890", "Test Book", "Test Author", 10, "A1", "http://example.com/image.jpg")
        ]
        
        result = book.search_by_title(self.mock_conn, "Test Book")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['isbn'], "1234567890")
        self.assertEqual(result[0]['title'], "Test Book")
        self.assertEqual(result[0]['image_url'], "http://example.com/image.jpg")

        # Test for no books found
        self.mock_cursor.fetchall.return_value = []
        result = book.search_by_title(self.mock_conn, "Nonexistent Book")
        self.assertEqual(result['message'], "No books found.")

    def test_search_by_author(self):
        """Test searching for books by author."""
        book = Book(isbn="1234567890", title="Test Book", author="Test Author", publisher="Test Publisher",
                    price=19.99, stock=10, rack="A1", image_url="http://example.com/image.jpg")
        
        # Mock the database response
        self.mock_cursor.fetchall.return_value = [
            ("1234567890", "Test Book", "Test Author", 10, "A1", "http://example.com/image.jpg")
        ]
        
        result = book.search_by_author(self.mock_conn, "Test Author")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['isbn'], "1234567890")
        self.assertEqual(result[0]['author'], "Test Author")
        self.assertEqual(result[0]['image_url'], "http://example.com/image.jpg")

        # Test for no books found
        self.mock_cursor.fetchall.return_value = []
        result = book.search_by_author(self.mock_conn, "Nonexistent Author")
        self.assertEqual(result['message'], "No books found.")

    def test_get_all_books(self):
        """Test fetching all books from the database."""
        book = Book(isbn="1234567890", title="Test Book", author="Test Author", publisher="Test Publisher",
                    price=19.99, stock=10, rack="A1", image_url="http://example.com/image.jpg")

        # Mock the database response
        self.mock_cursor.fetchall.return_value = [
            ("1234567890", "Test Book", "Test Author", "Test Publisher", 19.99, 10, "A1", 0, 0, None, 0, "http://example.com/image.jpg")
        ]
        
        result = book.get_all_books(self.mock_conn)
        self.assertEqual(len(result['message']), 1)
        self.assertEqual(result['message'][0]['isbn'], "1234567890")
        self.assertEqual(result['message'][0]['title'], "Test Book")

        # Test for no books found
        self.mock_cursor.fetchall.return_value = []
        result = book.get_all_books(self.mock_conn)
        self.assertEqual(result['message'], "No books found!")

if __name__ == '__main__':
    unittest.main()
