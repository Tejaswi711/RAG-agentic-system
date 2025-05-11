import pymysql
from pymysql import Error


def create_db_connection():
    """
    Establishes a connection to the MySQL database.
    Returns connection object if successful, None otherwise.
    """
    try:
        connection = pymysql.connect(
            host="localhost",
            user="fedreg_user",
            password="NewRootPass123!",
            database="federal_register",
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor  # Returns results as dictionaries
        )
        print("Successfully connected to MySQL database!")
        return connection

    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None


def execute_query(connection, query, params=None):
    """
    Executes a SQL query and returns the results.
    """
    try:
        with connection.cursor() as cursor:
            cursor.execute(query, params or ())

            # For SELECT queries
            if query.strip().upper().startswith('SELECT'):
                return cursor.fetchall()
            # For INSERT/UPDATE/DELETE
            else:
                connection.commit()
                return cursor.rowcount

    except Error as e:
        print(f"Database error: {e}")
        connection.rollback()
        return None


def main():
    # Establish connection
    conn = create_db_connection()
    if not conn:
        return

    try:
        # Example 1: Create a table (if doesn't exist)
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS documents (
            id INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            content TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
        execute_query(conn, create_table_sql)
        print("✔ Table check/creation completed")

        # Example 2: Insert sample data
        insert_sql = "INSERT INTO documents (title, content) VALUES (%s, %s)"
        res = execute_query(conn, insert_sql, ("First Document", "Sample content here"))
        print(f"Inserted {res} row(s)")

        # Example 3: Query data
        results = execute_query(conn, "SELECT * FROM documents")
        print("Query results:")
        for row in results:
            print(f"ID: {row['id']}, Title: {row['title']}")

    finally:
        # Always close the connection
        if conn and conn.open:
            conn.close()
            print("Database connection closed")


if __name__ == "__main__":
    main()
