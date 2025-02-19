import mysql.connector
import pandas as pd

# Database Credentials (Can be loaded from config.json)
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "123456",
    "database": "sensor_db"
}

def get_table_columns(table_name):
    """Fetch column names dynamically from the database."""
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()
    
    cursor.execute(f"SHOW COLUMNS FROM {table_name}")
    columns = [col[0] for col in cursor.fetchall()]
    
    cursor.close()
    conn.close()
    return columns

def get_data(query):
    """Fetch data from MySQL and return a Pandas DataFrame."""
    conn = mysql.connector.connect(**DB_CONFIG)
    
    try:
        df = pd.read_sql(query, con=conn, parse_dates=['timestamp'])
    finally:
        conn.close()
    
    return df.sort_values(by="timestamp")
