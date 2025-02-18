import streamlit as st
import mysql.connector
import pandas as pd
import time
from st_autorefresh import st_autorefresh

# Auto-refresh every 5 seconds
st_autorefresh(interval=5000, limit=None, key="data_refresh")

def get_data():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="123456",
        database="sensor_db"
    )
    
    query = """
    SELECT timestamp, value 
    FROM sensor_data
    ORDER BY timestamp DESC
    LIMIT 100
    """
    
    df = pd.read_sql(query, conn, parse_dates=['timestamp'])
    conn.close()
    return df

def main():
    st.title("Real-Time Sensor Dashboard")
    
    data = get_data()
    
    # Display latest value
    latest = data.iloc[0]
    st.metric("Current Value", f"{latest['value']:.2f}", 
              delta=f"{latest['value'] - data.iloc[1]['value']:.2f} from previous")
    
    # Show time series chart
    st.line_chart(data.set_index('timestamp'))

if __name__ == "__main__":
    main()