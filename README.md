# Book Haven - Bookshop Automation Software

Book Haven is a software to automate various activities of a small book store.
## Features

- View all books that the store sells
- Search books by author or title
- Book details including title, author, publisher, price, stock, and rack location
- Shopping cart functionality
- Book management (add, delete, update price)


## Technologies Used

- **Frontend**: HTML, CSS, JavaScript
- **Backend**: Python with Flask
- **Database**: MySQL

## Installation

1. Clone the repository:
     ```bash
   git clone <repository-url>
   cd book-haven
2. Set up the Python environment:
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    pip install -r requirements.txt
3. Set up the MySQL database:
    mysql -u username -p
    CREATE DATABASE bookshop;
    USE bookshop;
4. Run the SQL script to create tables:
    mysql -u username -p bookshop < database.sql
5. Configure the database connection in the application.

6. Start the Flask server:
    python app.py
7. Access the application at `http://127.0.0.1:5000`
## Usage

### Viewing Books
- Click on "View All Books" to display all available books in the store
- Use the search bars to find books by author or title

### Shopping Cart
- Click on the cart icon to view your shopping cart
- Add books to cart by clicking "Add to Cart" button
- Review and checkout from the cart sidebar

### Book Management (Clerk)
- Add new books with details and image URLs or update the old stock
- Update book prices
- Delete books from inventory
- Add vendor, view vendors and delete vendor 
- See Bookrequests for the ones we didnt sell yet
- See Transaction Statistics of a particular book between 2 dates
## Project Structure

book-haven/
├── app.py                     # Main Flask application
├── database.sql               # SQL file for database
├── backend/
│   ├── book.py                # Backend for book class and its functions
│   ├── bookrequest.py         # Backend for bookrequest table
│   ├── customer.py            # Backend for customer class
│   ├── inventory.py           # Backend for inventory class
│   ├── salesdetails.py        # Backend for sale functions
│   ├── transactiondetails.py  # Backend for transactiondetails class
│   ├── vendorsupply.py        # Backend for vendor class
│   └── db_connection.py
├── static/
│   ├── styles.css             # CSS for most HTML files
│   ├── cartstyles.css         # CSS for cart
│   ├── clerk.css              # CSS for clerk page
│   ├── loginstyles.css        # CSS for login page
│   ├── script.js              # JavaScript for login
│   ├── book.js                # Book operations
│   ├── cart.js                # Shopping cart functionality
│   ├── searchbar.js           # Search functionality
│   ├── bookrequest.js         # Request books never sold
│   ├── generate_bill.js       # Bill generation and payment gateway
│   ├── statistics.js          # Sales statistics between dates
│   ├── storeops.js            # Store operations
│   └── vendor.js              # Vendor operations
├── templates/
│   ├── index.html             # Home page
│   ├── clerk.html             # Clerk page
│   ├── cart.html              # Cart page
│   ├── generate_bill.html     # Generated bill page
│   ├── login.html             # Login page
│   ├── proceed_to_pay.html    # Payment gateway page
│   └── order_confirmed.html   # Payment success page
└── README.md                  # Documentation file
