import streamlit as st
import mysql.connector
import pandas as pd
import plotly.express as px
import time

def get_data():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="123456",
        database="sensor_db"
    )
    
    query = """
    SELECT timestamp, value1, value2 
    FROM sensor_data
    ORDER BY timestamp DESC
    LIMIT 100
    """
    
    df = pd.read_sql(query, con=conn, parse_dates=['timestamp'])  # Fix pandas SQL warning
    conn.close()
    
    return df.sort_values(by="timestamp")

def main():
    st.set_page_config(page_title="Real-Time Sensor Dashboard", layout="wide")

    st.markdown("<h2 style='text-align: center; color: white;'>Real-Time Sensor Dashboard</h2>", 
                unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    
    with col1:
        refresh_interval = st.selectbox(
            "Refresh Interval",
            options=["5s", "10s", "30s", "1m"],
            index=0
        )
        
    with col2:
        if st.button("Refresh Now"):
            st.session_state.manual_refresh = True 
            st.rerun()

    interval_map = {
        "5s": 5,
        "10s": 10,
        "30s": 30,
        "1m": 60
    }

    if "last_refresh_time" not in st.session_state:
        st.session_state.last_refresh_time = time.time()

    if time.time() - st.session_state.last_refresh_time >= interval_map[refresh_interval]:
        st.session_state.last_refresh_time = time.time()
        st.rerun()

    placeholder = st.empty()

    with placeholder.container():
        data = get_data()

        if not data.empty:
            latest = data.iloc[-1]
            prev_value1 = data.iloc[-2]['value1'] if len(data) > 1 else latest['value1']
            prev_value2 = data.iloc[-2]['value2'] if len(data) > 1 else latest['value2']
            
            st.metric("Current Value 1", f"{latest['value1']:.2f}", 
                    delta=f"{latest['value1'] - prev_value1:.2f} from previous")
            st.metric("Current Value 2", f"{latest['value2']:.2f}", 
                    delta=f"{latest['value2'] - prev_value2:.2f} from previous")

            fig = px.line(data, x='timestamp', y=['value1', 'value2'], 
                        title="Live Sensor Data",
                        labels={'timestamp': 'Time', 'value1': 'Sensor Value 1', 'value2': 'Sensor Value 2'},
                        template="plotly_dark")

            fig.update_traces(line=dict(width=1))
            fig.update_layout(height=400, margin=dict(l=0, r=0, t=30, b=0))
            
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("No data available from the database")

if __name__ == "__main__":
    main()
