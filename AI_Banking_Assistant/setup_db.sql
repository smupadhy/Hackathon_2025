CREATE TABLE customers (
    customer_id INT PRIMARY KEY,
    name VARCHAR(100),
    phone VARCHAR(15),
    cibil_score INT,
    income DECIMAL(10,2),
    existing_loans DECIMAL(10,2)
);

CREATE TABLE accounts (
    account_id INT PRIMARY KEY,
    customer_id INT,
    account_type VARCHAR(50),
    balance DECIMAL(15,2),
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

INSERT INTO customers VALUES
(1, 'Amit Sharma', '9876543210', 780, 120000, 50000),
(2, 'Priya Gupta', '8765432109', 650, 70000, 100000);
