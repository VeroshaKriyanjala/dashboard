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
            value1 = random.uniform(10, 30)
            value2 = random.uniform(15, 40)

            cursor.execute("""
                INSERT INTO sensor_data (value1, value2)
                VALUES (%s, %s)
            """, (value1, value2))
            
            conn.commit()
            print(f"Inserted value: {value1}, {value2}")
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("Stopping data inserter")
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    insert_data()
