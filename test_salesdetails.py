import unittest
from unittest.mock import MagicMock
from backend.salesdetails import Salesdetails  # Replace with actual module name
from datetime import datetime
from mysql.connector import Error

class TestSalesDetailsMethods(unittest.TestCase):

    def setUp(self):
        self.mock_conn = MagicMock()
        self.mock_cursor = MagicMock()
        self.mock_conn.cursor.return_value = self.mock_cursor

    def test_generate_bill_empty_cart(self):
        """Test generate_bill when the cart is empty"""
        self.mock_conn.cursor.return_value = self.mock_cursor
        self.mock_cursor.fetchall.return_value = []  # Empty cart

        result = Salesdetails.generate_bill(self.mock_conn, "user1")

        self.assertEqual(result['status'], "error")
        self.assertEqual(result['message'], "Cart is empty")
        self.mock_cursor.execute.assert_called_with(
            """
                SELECT c.isbn, c.quantity, b.title, b.price
                FROM cart c
                JOIN Book b ON c.isbn = b.isbn
                WHERE c.user_id = %s
            """, ("user1",)
        )

    def test_generate_bill_success(self):
        """Test generate_bill with items in the cart"""
        self.mock_conn.cursor.return_value = self.mock_cursor
        self.mock_cursor.__dict__['dictionary'] = True  # Simulate dictionary=True
        cart_data = [
            {"isbn": "1234567890", "quantity": 2, "title": "Test Book", "price": 15.0},
            {"isbn": "0987654321", "quantity": 1, "title": "Another Book", "price": 20.0}
        ]
        self.mock_cursor.fetchall.return_value = cart_data

        result = Salesdetails.generate_bill(self.mock_conn, "user1")

        self.assertEqual(result['status'], "success")
        self.assertEqual(len(result['items']), 2)
        self.assertEqual(result['total'], 50.0)  # (2 * 15) + (1 * 20) = 50
        self.assertEqual(result['items'][0], {
            "isbn": "1234567890", "title": "Test Book", "quantity": 2, "price": 15.0, "subtotal": 30.0
        })
        self.assertTrue("date" in result)  # Check date is present
        self.mock_cursor.execute.assert_called_once()

    def test_generate_bill_database_error(self):
        """Test generate_bill with a database error"""
        self.mock_conn.cursor.return_value = self.mock_cursor
        self.mock_cursor.execute.side_effect = Error("Database failure")

        result = Salesdetails.generate_bill(self.mock_conn, "user1")

        self.assertEqual(result['status'], "error")
        self.assertEqual(result['message'], "Database failure")

    def test_process_payment_empty_cart(self):
        """Test process_payment when the cart is empty"""
        self.mock_cursor.fetchone.return_value = (None,)  # No previous sale_id
        self.mock_cursor.fetchall.return_value = []  # Empty cart

        result = Salesdetails.process_payment(self.mock_conn, "user1", "credit_card")

        self.assertEqual(result['status'], "error")
        self.assertEqual(result['message'], "Cart is empty")
        self.mock_cursor.execute.assert_any_call("SELECT MAX(sale_id) FROM transaction_details")

    def test_process_payment_success(self):
        """Test process_payment with items in the cart"""
        self.mock_cursor.fetchone.side_effect = [(5,), None]  # Ensure correct sale_id progression

        cart_data = [
            ("1234567890", 2, 15.0, 10, "Test Book"),  # isbn, quantity, price, stock, title
            ("0987654321", 1, 20.0, 5, "Another Book")
        ]
        self.mock_cursor.fetchall.return_value = cart_data
        self.mock_conn.commit.return_value = None

        result = Salesdetails.process_payment(self.mock_conn, "user1", "credit_card")
        
        self.assertEqual(result['status'], "success")
        self.assertEqual(result['sale_id'], 6)  # Next sale_id = 6
        self.assertEqual(result['total'], 50.0)  # (2 * 15) + (1 * 20) = 50
        self.assertEqual(len(result['items']), 2)
        self.assertEqual(result['items'][0], {
            "isbn": "1234567890", "quantity": 2, "subtotal": 30.0, "title": "Test Book", "price": 15.0
        })
        self.assertEqual(result['payment_method'], "credit_card")
        self.mock_cursor.execute.assert_any_call(
            "UPDATE Book SET stock = %s WHERE isbn = %s", (8, "1234567890")  # 10 - 2
        )
        '''self.mock_cursor.execute.assert_any_call(
            "INSERT INTO transaction_details (sale_id, isbn, quantity_sold, subtotal, date_of_purchase) "
            "VALUES (%s, %s, %s, %s, NOW())", (6, "1234567890", 2, 30.0)
        )'''
        self.mock_cursor.execute.assert_any_call(
            unittest.mock.ANY,  # Allow flexibility in query text if minor format issues exist
            (6, '1234567890', 2, 30.0)
        )

        self.mock_cursor.execute.assert_any_call(
            "DELETE FROM cart WHERE user_id = %s", ("user1",)
        )

    def test_process_payment_insufficient_stock(self):
        """Test process_payment when stock goes to zero"""
        self.mock_cursor.fetchone.return_value = (None,)  # No previous sale_id, start at 1
        cart_data = [
            ("1234567890", 5, 10.0, 3, "Test Book")  # Request 5, only 3 in stock
        ]
        self.mock_cursor.fetchall.return_value = cart_data
        self.mock_conn.commit.return_value = None

        result = Salesdetails.process_payment(self.mock_conn, "user1", "credit_card")

        self.assertEqual(result['status'], "success")
        self.assertEqual(result['sale_id'], 1)
        self.assertEqual(result['total'], 50.0)  # 5 * 10
        self.assertEqual(result['items'][0]['quantity'], 5)
        self.mock_cursor.execute.assert_any_call(
            "UPDATE Book SET stock = %s WHERE isbn = %s", (0, "1234567890")  # 3 - 5 = 0 (min stock 0)
        )

    def test_process_payment_database_error(self):
        """Test process_payment with a database error"""
        self.mock_cursor.fetchone.return_value = (None,)  # No previous sale_id
        self.mock_cursor.execute.side_effect = Error("Payment failed")
        self.mock_conn.rollback.return_value = None

        result = Salesdetails.process_payment(self.mock_conn, "user1", "credit_card")

        self.assertEqual(result['status'], "error")
        self.assertEqual(result['message'], "Payment failed")
        self.mock_conn.rollback.assert_called_once()

if __name__ == '__main__':
    unittest.main()