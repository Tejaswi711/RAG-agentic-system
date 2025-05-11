import os
import pymysql
from dotenv import load_dotenv
from typing import Optional

load_dotenv()

def get_db_connection() -> Optional[pymysql.Connection]:
    try:
        return pymysql.connect(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASS'),
            database=os.getenv('DB_NAME'),
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
    except pymysql.Error as e:
        print(f"Connection failed: {e}")
        return None

# 3. Example usage
if __name__ == "__main__":
    conn = get_db_connection()
    if conn:
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT VERSION()")
                print("MySQL Version:", cursor.fetchone())
        finally:
            conn.close()
