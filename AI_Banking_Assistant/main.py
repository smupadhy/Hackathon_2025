from fastapi import FastAPI, HTTPException
import pymysql
import os

# In production, you'd do: DB_HOST = os.environ["DB_HOST"], etc.
DB_HOST = "banking-db-cluster.cluster-cxmi8o0oebpe.us-east-1.rds.amazonaws.com"
DB_USER = "admin"
DB_PASS = "[CTcwO9wTM~D(WB4OpwP5qw2qRiM"
DB_NAME = "banking_db"

app = FastAPI()

def get_db():
    # In production, you might use a connection pool or a library like SQLAlchemy.
    return pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASS,
        database=DB_NAME,
        cursorclass=pymysql.cursors.DictCursor
    )

@app.get("/balance/{customer_id}")
def get_balance(customer_id: int):
    conn = get_db()
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT account_id, account_type, balance
                FROM accounts
                WHERE customer_id=%s
            """, (customer_id,))
            rows = cursor.fetchall()
            return {"customer_id": customer_id, "accounts": rows}
    finally:
        conn.close()

@app.post("/pay-credit-card")
def pay_credit_card(customer_id: int, card_id: int, amount: float):
    conn = get_db()
    try:
        with conn.cursor() as cursor:
            # Find a savings account
            cursor.execute("""
                SELECT account_id, balance FROM accounts
                WHERE customer_id=%s AND account_type='Savings'
                LIMIT 1
            """, (customer_id,))
            account = cursor.fetchone()
            if not account:
                raise HTTPException(status_code=400, detail="No savings account found.")
            if account["balance"] < amount:
                raise HTTPException(status_code=400, detail="Insufficient balance.")

            new_balance = account["balance"] - amount
            cursor.execute("""
                UPDATE accounts
                SET balance=%s
                WHERE account_id=%s
            """, (new_balance, account["account_id"]))

            # Update credit card outstanding
            cursor.execute("""
                UPDATE credit_cards
                SET outstanding_amount = outstanding_amount - %s
                WHERE card_id=%s
            """, (amount, card_id))

            # Insert a transaction record
            cursor.execute("""
                INSERT INTO transactions (account_id, txn_type, amount, txn_date, description)
                VALUES (%s, 'DEBIT', %s, NOW(), 'Credit card bill payment')
            """, (account["account_id"], amount))

            conn.commit()
            return {
                "message": "Bill paid successfully.",
                "new_account_balance": new_balance
            }
    finally:
        conn.close()

@app.get("/loan-eligibility/{customer_id}")
def check_loan_eligibility(customer_id: int):
    conn = get_db()
    try:
        with conn.cursor() as cursor:
            # Gather cibil, income, existing loans
            cursor.execute("""
                SELECT cibil_score, monthly_income
                FROM customers
                WHERE customer_id=%s
            """, (customer_id,))
            cust = cursor.fetchone()
            if not cust:
                raise HTTPException(status_code=404, detail="Customer not found.")

            cibil = cust["cibil_score"]
            income = cust["monthly_income"]

            # Basic logic: if cibil > 700 and income > 50000 => eligible for personal loan up to 5 * income
            if cibil > 700 and income > 50000:
                max_loan = income * 5
                return {"eligible": True, "max_loan_amount": max_loan}
            else:
                return {"eligible": False, "message": "Not eligible based on cibil/income"}
    finally:
        conn.close()
