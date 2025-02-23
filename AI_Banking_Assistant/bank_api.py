from fastapi import FastAPI
import pymysql

app = FastAPI()

# Connect to RDS
db = pymysql.connect(
    host="banking-db-cluster.cluster-cxmi8o0oebpe.us-east-1.rds.amazonaws.com",
    user="admin",
    password="[CTcwO9wTM~D(WB4OpwP5qw2qRiM",
    database="banking_db"
)

@app.get("/income/{customer_id}")
def get_income(customer_id: int):
    try:
        cursor = db.cursor()
        cursor.execute("SELECT income FROM customers WHERE customer_id = %s", (customer_id,))
        income = cursor.fetchone()
        return {"customer_id": customer_id, "income": income[0]}
    except Exception as e:
        print("Error:", e)
        raise HTTPException(status_code=500, detail=str(e))
