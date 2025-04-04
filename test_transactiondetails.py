import unittest
from unittest.mock import MagicMock
from backend.transactiondetails import Transactiondetails  # Replace with actual module name
from backend.book import Book

class TestTransactionDetailsMethods(unittest.TestCase):

    def setUp(self):
        self.mock_conn = MagicMock()
        self.mock_cursor = MagicMock()
        self.mock_conn.cursor.return_value = self.mock_cursor

    def test_add_to_cart_success(self):
        """Test adding items to the cart when there is sufficient stock"""
        self.mock_cursor.fetchone.side_effect = [
            (10, 0),  # Stock = 10, total in carts = 0
            (1,),     # Existing sale_id = 1
            None      # No existing item in cart
        ]
        self.mock_conn.commit.return_value = None

        result = Transactiondetails.add_to_cart(self.mock_conn, "1234567890", 3, 1)

        self.assertEqual(result['status'], "success")
        self.assertIn("Added 3 copies of ISBN 1234567890 to cart", result['message'])
        self.mock_cursor.execute.assert_any_call(
            "INSERT INTO cart (sale_id, isbn, quantity,user_id) VALUES (%s, %s, %s, %s)",
            (1, "1234567890", 3, 1)
        )

    def test_add_to_cart_out_of_stock(self):
        """Test when the book is out of stock and the request is recorded"""
        self.mock_cursor.fetchone.side_effect = [
            (2, 0),  # Stock = 2, total in carts = 0
            (1,),    # Existing sale_id = 1
            None     # No existing item in cart
        ]
        self.mock_conn.commit.return_value = None

        result = Transactiondetails.add_to_cart(self.mock_conn, "1234567890", 5, 1)

        self.assertEqual(result['status'], "warning")
        self.assertEqual(result['message'], "✅ Added 2 copies to cart. The remaining 3 copies have been requested.")
        self.mock_cursor.execute.assert_any_call(
            "UPDATE Book SET num_required = num_required + %s WHERE isbn = %s", (3, "1234567890")
        )

    def test_transactions_statistics(self):
        """Test fetching transaction statistics"""
        self.mock_cursor.fetchone.side_effect = [
            (10,),        # Total sold = 10
            ("Test Book",) # Book exists
        ]

        result = Transactiondetails.transactions_statistics(self.mock_conn, "1234567890", "2025-01-01", "2025-04-01")

        self.assertEqual(result['isbn'], "1234567890")
        self.assertEqual(result['total_sold'], 10)
        self.mock_cursor.execute.assert_any_call(
            "SELECT SUM(quantity_sold) FROM transaction_details WHERE isbn = %s AND date_of_purchase BETWEEN %s AND %s",
            ("1234567890", "2025-01-01", "2025-04-01")
        )

    def test_transactions_statistics_no_book(self):
        """Test fetching transaction statistics for a book that does not exist"""
        self.mock_cursor.fetchone.side_effect = [
            (None,),  # No transactions
            None      # Book does not exist
        ]

        result = Transactiondetails.transactions_statistics(self.mock_conn, "9999999999", "2025-01-01", "2025-04-01")

        self.assertEqual(result['message'], "The book with 9999999999 is not being sold currently...")

    def test_view_cart(self):
        """Test viewing cart items"""
        # Ensure the cursor returned by conn.cursor() is our mock_cursor with dictionary=True
        self.mock_conn.cursor.return_value = self.mock_cursor
        self.mock_cursor.__dict__['dictionary'] = True  # Simulate dictionary=True behavior
        cart_data = [{
            'isbn': "1234567890", 'quantity': 2, 'title': "Test Book", 'author': "Test Author",
            'price': 15.0, 'image_url': "http://example.com/image.jpg"
        }]
        self.mock_cursor.fetchall.return_value = cart_data

        result = Transactiondetails.view_cart(self.mock_conn, 1)

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['isbn'], "1234567890")
        self.assertEqual(result, cart_data)  # Ensure the exact data is returned

    def test_update_cart(self):
        """Test updating an item in the cart"""
        self.mock_cursor.fetchone.side_effect = [
            (1, 3),  # sale_id = 1, current_quantity = 3
            (10,)    # Stock = 10
        ]
        self.mock_conn.commit.return_value = None

        result = Transactiondetails.update_cart(self.mock_conn, "1234567890", 5, "akmiryala")

        self.assertEqual(result['status'], "success")
        self.assertEqual(result['message'], "Updated to 5")
        self.mock_cursor.execute.assert_any_call(
            "UPDATE cart SET quantity = %s WHERE isbn = %s AND sale_id = %s AND user_id = %s",
            (5, "1234567890", 1, "akmiryala")
        )

    def test_update_cart_remove_item(self):
        """Test removing an item from the cart"""
        self.mock_cursor.fetchone.return_value = (1, 3)  # sale_id = 1, current_quantity = 3
        self.mock_conn.commit.return_value = None

        result = Transactiondetails.update_cart(self.mock_conn, "1234567890", 0, 1)

        self.assertEqual(result['status'], "success")
        self.assertEqual(result['message'], "Removed item with ISBN 1234567890")
        self.mock_cursor.execute.assert_any_call(
            "DELETE FROM cart WHERE isbn = %s AND sale_id = %s AND user_id = %s",
            ("1234567890", 1, 1)
        )

    def test_remove_from_cart(self):
        """Test removing an item from the cart"""
        self.mock_conn.commit.return_value = None

        result = Transactiondetails.remove_from_cart(self.mock_conn, "1234567890")

        self.assertEqual(result['status'], "success")
        self.assertEqual(result['message'], "Item removed from cart")
        self.mock_cursor.execute.assert_called_with(
            "DELETE FROM cart WHERE isbn = %s", ("1234567890",)
        )

if __name__ == '__main__':
    unittest.main()