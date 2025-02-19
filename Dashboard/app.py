import streamlit as st
import time
import pandas as pd
import plotly.express as px
from database import get_table_columns, get_data
from query_builder import generate_query
from ui_components import render_column_configuration
from autorefresh import auto_refresh

# Streamlit Page Config
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
    st.stop()

# Column Configuration UI
selected_columns, aggregations, aliases = render_column_configuration(all_columns, max_rows)

# Generate Query
query = generate_query(selected_columns, aggregations, aliases, table_name)
st.code(f"Generated SQL:\n{query}", language="sql")

# Auto-refresh
refresh_interval = auto_refresh()

# Fetch and display data
try:
    data = get_data(query)
    if data.empty:
        st.warning("No data found")
    else:
        # Dynamic Metrics
        value_columns = [col for col in data.columns if col != 'timestamp']
        metric_cols = st.columns(len(value_columns))

        for idx, col in enumerate(value_columns):
            with metric_cols[idx]:
                current = data[col].iloc[-1]
                previous = data[col].iloc[-2] if len(data) > 1 else current
                delta = current - previous
                st.metric(f"{col}", f"{current:.2f}", delta=f"{delta:.2f}")

        # Line Chart
        fig = px.line(data, x='timestamp', y=value_columns, title="Time Series Data",
                      labels={'value': 'Measurements', 'timestamp': 'Time'}, template="plotly_dark")
        fig.update_layout(height=400, margin=dict(l=20, r=20, t=40, b=20))
        st.plotly_chart(fig, use_container_width=True)

except Exception as e:
    st.error(f"Error fetching data: {str(e)}")
