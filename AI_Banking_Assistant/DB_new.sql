CREATE TABLE customers (
  customer_id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(100),
  phone VARCHAR(15),
  dob DATE,
  cibil_score INT,
  monthly_income DECIMAL(10,2),
  age INT,
  address VARCHAR(255)
);

CREATE TABLE accounts (
  account_id INT AUTO_INCREMENT PRIMARY KEY,
  customer_id INT,
  account_type VARCHAR(50),
  balance DECIMAL(15,2),
  FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

CREATE TABLE credit_cards (
  card_id INT AUTO_INCREMENT PRIMARY KEY,
  customer_id INT,
  card_number VARCHAR(16),
  credit_limit DECIMAL(15,2),
  outstanding_amount DECIMAL(15,2),
  due_date DATE,
  FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

CREATE TABLE transactions (
  transaction_id INT AUTO_INCREMENT PRIMARY KEY,
  account_id INT,
  txn_type VARCHAR(10),
  amount DECIMAL(15,2),
  txn_date DATETIME,
  description VARCHAR(255),
  FOREIGN KEY (account_id) REFERENCES accounts(account_id)
);

CREATE TABLE mutual_funds (
  mf_id INT AUTO_INCREMENT PRIMARY KEY,
  mf_name VARCHAR(100),
  mf_type VARCHAR(50),
  nav DECIMAL(10,2)
);

CREATE TABLE customer_mf_holdings (
  holding_id INT AUTO_INCREMENT PRIMARY KEY,
  customer_id INT,
  mf_id INT,
  units_held DECIMAL(10,2),
  purchase_cost DECIMAL(15,2),
  FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
  FOREIGN KEY (mf_id) REFERENCES mutual_funds(mf_id)
);

CREATE TABLE loans (
  loan_id INT AUTO_INCREMENT PRIMARY KEY,
  customer_id INT,
  loan_type VARCHAR(50),
  principal DECIMAL(15,2),
  interest_rate DECIMAL(5,2),
  tenure_months INT,
  monthly_emi DECIMAL(15,2),
  outstanding_principal DECIMAL(15,2),
  status VARCHAR(20),
  FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

INSERT INTO customers (name, phone, dob, cibil_score, monthly_income, age, address)
VALUES
('Amit Sharma', '9876543210', '1990-05-12', 780, 120000, 32, 'Mumbai, MH'),
('Priya Gupta', '8765432109', '1988-08-22', 650, 70000, 34, 'Delhi, DL');

INSERT INTO accounts (customer_id, account_type, balance)
VALUES (1, 'Savings', 75000), (1, 'Current', 25000),
       (2, 'Savings', 30000), (2, 'Current', 10000);

INSERT INTO credit_cards (customer_id, card_number, credit_limit, outstanding_amount, due_date)
VALUES (1, '1234123412341234', 100000, 5000, '2025-03-15'),
       (2, '9876987698769876', 80000, 3000, '2025-03-10');
