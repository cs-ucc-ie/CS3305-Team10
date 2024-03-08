import mysql.connector

# MySQL connection configuration
mysql_config = {
    'host': 'cs1.ucc.ie',
    'user': 'facialrecognition2024',
    'password': 'caipu',
    'database': 'facialrecognition2024'
}

try:
    connection = mysql.connector.connect(**mysql_config)
    cursor = connection.cursor()
    print("Connected to the database.")
    
    create_table_query = """
    CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(255) NOT NULL,
        email VARCHAR(255) NOT NULL,
        password VARCHAR(255) NOT NULL
    )
    """

    cursor.execute(create_table_query)
    print("Table 'users' created successfully.")

    connection.commit()
    cursor.close()
    connection.close()
except mysql.connector.Error as e:
    print(f"Error: {e}")
