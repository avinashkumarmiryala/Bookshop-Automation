USE BookShop;
CREATE TABLE Book(
	isbn VARCHAR(255),
    title VARCHAR(255),
    author VARCHAR(255),
    publisher VARCHAR(255),
    price INT,
    stock INT,
    rack INT,
    freq INT,
    num_required INT,
    request_date DATE,
    average INT);
    
CREATE TABLE BookRequest(
	request_id INT,
    isbn VARCHAR(255),
    title VARCHAR(255),
    author VARCHAR(255),
    publisher VARCHAR(255),
    num_required INT);
    
CREATE TABLE Store(
	arrival_date DATE,
    quantity_arrived INT,
    isbn VARCHAR(255),
    title VARCHAR(255),
    author VARCHAR(255),
    publisher VARCHAR(255),
    price INT);
    
CREATE TABLE VendorSupply(
	vendor_id INT,
    vendor_name VARCHAR(255),
    vendor_address VARCHAR(1023),
    contact_info VARCHAR(15),
    publisher VARCHAR(255));
    
CREATE TABLE cart(
    sale_id INT,
    isbn VARCHAR(255),
    quantity INT
);

CREATE TABLE transaction_details(
    transaction_id INT,
    sale_id INT,
    isbn VARCHAR(255), 
    quantity_sold INT,
    subtotal INT,
    date_of_purchase DATE
);

CREATE TABLE customer(
	username VARCHAR(31),
    passwd VARCHAR(15),
    customer_name VARCHAR(255),
    contact_info VARCHAR(15),
    customer_address VARCHAR(1023));
INSERT INTO Book (isbn, title, author, publisher, price, stock, rack, freq, num_required, request_date, average)
VALUES ('2345bhjk7888', 'ABCDE', 'Ram', 'Kumar', 2425, 14, 56, 2, 0, '2005-12-31', 67,'https://is5-ssl.mzstatic.com/image/thumb/Publication/v4/cb/e9/13/cbe913ee-b696-f26f-1581-23231b1a4c7a/PridePrejudice-Cover.jpg/100000x100000-999.jpg');






