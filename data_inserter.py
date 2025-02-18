import time
import random
import mysql.connector

def insert_data():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="123456",
        database="sensor_db"
    )
    cursor = conn.cursor()
    
    try:
        while True:
            # Generate random data (simulate sensor reading)
            value = random.uniform(10, 30)
            
            cursor.execute("""
                INSERT INTO sensor_data (value)
                VALUES (%s)
            """, (value,))
            
            conn.commit()
            print(f"Inserted value: {value}")
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("Stopping data inserter")
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    insert_data()