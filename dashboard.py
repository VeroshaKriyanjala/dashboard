import streamlit as st
import mysql.connector
import pandas as pd
import plotly.express as px
import time

def get_table_columns(table_name):
    """Dynamically fetch column names from database"""
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="123456",
        database="sensor_db"
    )
    cursor = conn.cursor()
    
    cursor.execute(f"SHOW COLUMNS FROM {table_name}")
    columns = [col[0] for col in cursor.fetchall()]
    
    cursor.close()
    conn.close()
    return columns

def get_data(query):
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="123456",
        database="sensor_db"
    )
    
    try:
        df = pd.read_sql(query, con=conn, parse_dates=['timestamp'])
    finally:
        conn.close()
    
    return df.sort_values(by="timestamp")

def generate_query(selected_columns, aggregations, aliases, table_name):
    base_query = "SELECT "
    
    selected_items = []
    for col, agg, alias in zip(selected_columns, aggregations, aliases):
        if agg:
            item = f"{agg}({col}) AS {alias}"
        else:
            item = f"{col} AS {alias}"
        selected_items.append(item)
    
    base_query += ", ".join(selected_items)
    base_query += f" FROM {table_name} ORDER BY timestamp DESC LIMIT 100"
    
    return base_query

def main():
    st.set_page_config(page_title="Real-Time Sensor Dashboard", layout="wide")

    st.markdown("<h2 style='text-align: center; color: white;'>Real-Time Sensor Dashboard</h2>", 
                unsafe_allow_html=True)

    # Table selection
    table_name = st.text_input("Enter Table Name", "sensor_data")
    
    try:
        all_columns = get_table_columns(table_name)
        max_rows = len(all_columns)
    except Exception as e:
        st.error(f"Error fetching columns: {str(e)}")
        return

    # Initialize session state
    if 'num_rows' not in st.session_state:
        st.session_state.num_rows = 1
    if 'last_refresh' not in st.session_state:
        st.session_state.last_refresh = time.time()

    # Column configuration
    st.subheader("Column Configuration")
    
    # Header
    cols = st.columns([3, 2, 2, 1])
    with cols[0]: st.markdown("**Column**")
    with cols[1]: st.markdown("**Aggregation**")
    with cols[2]: st.markdown("**Alias**")
    with cols[3]: st.markdown("")

    # Dynamic rows
    selected_columns = []
    aggregations = []
    aliases = []

    for i in range(st.session_state.num_rows):
        cols = st.columns([3, 2, 2, 1])
        
        with cols[0]:
            col = st.selectbox(
                f"Column {i}", 
                options=all_columns,
                key=f"col_{i}"
            )
            selected_columns.append(col)
        
        with cols[1]:
            agg = st.selectbox(
                f"Aggregation {i}", 
                [None, "AVG", "SUM", "COUNT", "MAX", "MIN"], 
                key=f"agg_{i}"
            )
            aggregations.append(agg)
        
        with cols[2]:
            alias = st.text_input(
                f"Alias {i}", 
                value=col,
                key=f"alias_{i}"
            )
            aliases.append(alias)
        
        with cols[3]:
            if i == st.session_state.num_rows - 1:
                if st.session_state.num_rows < max_rows:
                    if st.button("➕", key=f"add_{i}"):
                        st.session_state.num_rows += 1
                        st.rerun()
                if st.session_state.num_rows > 1:
                    if st.button("➖", key=f"remove_{i}"):
                        st.session_state.num_rows -= 1
                        st.rerun()

    # Query generation
    query = generate_query(selected_columns, aggregations, aliases, table_name)
    st.code(f"Generated SQL:\n{query}", language="sql")

    # Refresh controls
    refresh_col1, refresh_col2 = st.columns([2, 1])
    with refresh_col1:
        refresh_interval = st.selectbox(
            "Auto Refresh Interval",
            options=["5s", "10s", "30s", "1m"],
            index=0
        )
    with refresh_col2:
        if st.button("🔄 Manual Refresh"):
            st.session_state.last_refresh = time.time()
            st.rerun()

    # Auto-refresh logic
    interval_map = {
        "5s": 5,
        "10s": 10,
        "30s": 30,
        "1m": 60
    }
    interval = interval_map[refresh_interval]
    
    if (time.time() - st.session_state.last_refresh) > interval:
        st.session_state.last_refresh = time.time()
        st.rerun()

    # Data display
    try:
        data = get_data(query)
        if data.empty:
            st.warning("No data found")
            return

        # Dynamic metrics
        value_columns = [col for col in data.columns if col != 'timestamp']
        metric_cols = st.columns(len(value_columns))
        
        for idx, col in enumerate(value_columns):
            with metric_cols[idx]:
                current = data[col].iloc[-1]
                previous = data[col].iloc[-2] if len(data) > 1 else current
                delta = current - previous
                st.metric(f"{col}", f"{current:.2f}", delta=f"{delta:.2f}")

        # Dynamic plot
        fig = px.line(data, x='timestamp', y=value_columns,
                      title="Time Series Data",
                      labels={'value': 'Measurements', 'timestamp': 'Time'},
                      template="plotly_dark")
        fig.update_layout(height=400, margin=dict(l=20, r=20, t=40, b=20))
        st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        st.error(f"Error fetching data: {str(e)}")

if __name__ == "__main__":
    main()