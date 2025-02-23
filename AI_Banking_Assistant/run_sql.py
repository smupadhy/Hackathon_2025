import pymysql
import boto3
import json

def get_secret(secret_name, region_name="us-east-1"):
    """
    Retrieves the secret from AWS Secrets Manager and returns it as a dict.
    We expect the secret to contain at least 'username' and 'password' keys.
    """
    client = boto3.client("secretsmanager", region_name=region_name)
    response = client.get_secret_value(SecretId=secret_name)
    secret_string = response["SecretString"]
    return json.loads(secret_string)

if __name__ == "__main__":
    # -----------------------------------------------------
    # 1) SET THESE VALUES FOR YOUR ENVIRONMENT
    # -----------------------------------------------------
    SECRET_NAME = "rds!cluster-ecd13850-8804-4a1d-be7b-94216b3f992f"  # e.g. "AmazonRDS-banking-db-cluster-XXXXX"
    REGION = "us-east-1"            # region where the secret lives
    HOST = "banking-db-cluster.cluster-cxmi8o0oebpe.us-east-1.rds.amazonaws.com"
    PORT = 3306
    DB_NAME = "banking_db"
    SQL_FILE = "DB_new.sql"       # The SQL script you want to run

    # -----------------------------------------------------
    # 2) RETRIEVE USERNAME/PASSWORD FROM SECRETS MANAGER
    # -----------------------------------------------------
    try:
        secret = get_secret(SECRET_NAME, REGION)
        db_user = secret["username"]
        db_pass = secret["password"]
        print("Retrieved username/password from Secrets Manager.")

        # -----------------------------------------------------
        # 3) CONNECT TO YOUR AURORA DATABASE
        # -----------------------------------------------------
        connection = pymysql.connect(
            host=HOST,
            user=db_user,
            password=db_pass,
            database=DB_NAME,
            port=PORT
        )
        print("Connected to Aurora DB successfully!")

        # -----------------------------------------------------
        # 4) READ AND EXECUTE YOUR SQL SCRIPT
        # -----------------------------------------------------
        with open(SQL_FILE, "r", encoding="utf-8") as file:
            sql_script = file.read()

        statements = sql_script.split(";")  # split by semicolons
        with connection.cursor() as cursor:
            for statement in statements:
                statement = statement.strip()
                if statement:
                    cursor.execute(statement)

        # Make sure the changes are persisted
        connection.commit()
        print("SQL script executed successfully!")

    except Exception as e:
        print("Error:", e)

    finally:
        if 'connection' in locals() and connection.open:
            connection.close()
            print("Connection closed.")
