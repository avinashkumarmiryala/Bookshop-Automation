-- Use the BookShop database
USE BookShop;

-- Create the Book table
CREATE TABLE Book (
    isbn VARCHAR(255) NOT NULL, -- ISBN is the primary key
    title VARCHAR(255) NOT NULL, -- Title must not be null
    author VARCHAR(255) NOT NULL, -- Author must not be null
    publisher VARCHAR(255) NOT NULL, -- Publisher must not be null
    price INT NOT NULL CHECK (price >= 0), -- Price must be non-negative
    stock INT NOT NULL DEFAULT 0 CHECK (stock >= 0), -- Stock defaults to 0, must be non-negative
    rack INT CHECK (rack >= 0), -- Rack number must be non-negative
    freq INT CHECK (freq >= 0), -- Frequency defaults to 0, must be non-negative
    num_required INT CHECK (num_required >= 0), -- Number required defaults to 0
    request_date DATE, -- Request date can be null
    average INT CHECK (average >= 0), -- Average defaults to 0
    image_url VARCHAR(255) NOT NULL, -- Image must not be null
    flag INT DEFAULT 1 CHECK (flag IN (0, 1)) -- Flag defaults to 1, can be 0 or 1
);

-- Create the BookRequest table
CREATE TABLE BookRequest (
    request_id INT AUTO_INCREMENT PRIMARY KEY, -- Auto-incrementing primary key
    isbn VARCHAR(255) NOT NULL, -- ISBN must not be null
    title VARCHAR(255) NOT NULL, -- Title must not be null
    author VARCHAR(255) NOT NULL, -- Author must not be null
    publisher VARCHAR(255) NOT NULL, -- Publisher must not be null
    num_required INT CHECK (num_required >= 0) -- Number required defaults to 0
    flag INT DEFAULT 1 CHECK (flag IN (0, 1)) -- Flag defaults to 1, can be 0 or 1
    --FOREIGN KEY (isbn) REFERENCES Book(isbn) -- Foreign key to Book table
);

-- Create the Store table
CREATE TABLE Store (
    arrival_date DATE NOT NULL, -- Arrival date must not be null
    quantity_arrived INT NOT NULL CHECK (quantity_arrived > 0), -- Quantity must be non-negative
    isbn VARCHAR(255) NOT NULL, -- ISBN must not be null
    title VARCHAR(255) NOT NULL, -- Title must not be null
    author VARCHAR(255) NOT NULL, -- Author must not be null
    publisher VARCHAR(255) NOT NULL, -- Publisher must not be null
    price INT NOT NULL CHECK (price > 0), -- Price must be non-negative
    image_url VARCHAR(255) NOT NULL -- Image must not be null
    flag INT DEFAULT 1 CHECK (flag IN (0, 1)) -- Flag defaults to 1, can be 0 or 1
    --FOREIGN KEY (isbn) REFERENCES Book(isbn) -- Foreign key to Book table
);

-- Create the VendorSupply table
CREATE TABLE VendorSupply (
    vendor_id INT AUTO_INCREMENT PRIMARY KEY, -- Auto-incrementing primary key
    vendor_name VARCHAR(255) NOT NULL, -- Vendor name must not be null
    vendor_address VARCHAR(1023) NOT NULL, -- Vendor address must not be null
    contact_info VARCHAR(15) NOT NULL, -- Contact info must not be null
    publisher VARCHAR(255) NOT NULL -- Publisher must not be null
);

-- Create the cart table
CREATE TABLE cart (
    sale_id INT AUTO_INCREMENT PRIMARY KEY, -- Auto-incrementing primary key
    isbn VARCHAR(255) NOT NULL, -- ISBN must not be null
    quantity INT NOT NULL CHECK (quantity >= 0), -- Quantity must be non-negative
    user_id VARCHAR(255) NOT NULL
    --FOREIGN KEY (isbn) REFERENCES Book(isbn) -- Foreign key to Book table
);

-- Create the transaction_details table
CREATE TABLE transaction_details (
    transaction_id INT AUTO_INCREMENT PRIMARY KEY, -- Auto-incrementing primary key
    sale_id INT NOT NULL, -- Sale ID must not be null
    isbn VARCHAR(255) NOT NULL, -- ISBN must not be null
    quantity_sold INT NOT NULL CHECK (quantity_sold >= 0), -- Quantity sold must be non-negative
    subtotal INT NOT NULL CHECK (subtotal >= 0), -- Subtotal must be non-negative
    date_of_purchase DATE NOT NULL, -- Date of purchase must not be null
    --FOREIGN KEY (sale_id) REFERENCES cart(sale_id), -- Foreign key to cart table
    --FOREIGN KEY (isbn) REFERENCES Book(isbn) -- Foreign key to Book table
);

-- Create the customer table
CREATE TABLE customer (
    username VARCHAR(31), --PRIMARY KEY -- Username is the primary key
    passwd VARCHAR(15) NOT NULL, -- Password must not be null
    customer_name VARCHAR(255) NOT NULL, -- Customer name must not be null
    contact_info VARCHAR(15) NOT NULL, -- Contact info must not be null
    customer_address VARCHAR(1023) NOT NULL -- Customer address must not be null
);