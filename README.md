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
├── app.py                # Main Flask application
├── database.sql          # SQL File for database
├── backend/
    ├── book.py               # Backend for book class and its functions
    ├── bookrequest.py        # Backend for bookrequest table(only for the books we have never sold)
    ├── customer.py           # Backend for customer class and its functions
    ├── inventory.py          # Backend for inventory class and its functions
    ├── salesdetailes.py      # Backend for sale functions
    ├── transactiondetails.py # Backend for transactiondetails class and its functions
    ├── vendorsupply.py       # Backend for vendor class and its functions
    ├── db_connection.py  
├── static/
│   ├── styles.css      # CSS styles for most of html files
│   └── cartstyles.css  # CSS styles for cart 
│   └── clerk.css       # CSS styles for clerk page
│   └── loginstyles.css # CSS styles for login page
│   ├── script.js       # JavaScript for login
│   ├── book.js         # Book-related for view books and update book, delete book
│   ├── cart.js         # Shopping cart functionality
│   └── searchbar.js    # Search functionality
│   └── bookrequest.js  # For the request of books we never sold
│   └── generate_bill.js #For bill generation of items in cart and also lead to payment gateway
│   └── statistics.js    # For statistics of a book with sales between particular dates
│   └── storeops.js     #For store operations
│   └── vendor.js        #For vendor operations
├── templates/
│   └── index.html      # Main HTML page-Home page
│   └── clerk.html      # HTML page for clerk
│   └── cart.html       # HTML extension for cart
│   └── generate_bill.html #HTML page to show the generated bill
│   └── login.html       # HTML page for login
│   └── proceed_to_pay.html #HTML page for payment gateway
│   └── order_confirmed.html #HTML page to show if the payment was successful
└── README.md           # This documentation file
