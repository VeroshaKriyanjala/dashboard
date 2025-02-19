import streamlit as st
from streamlit_autorefresh import st_autorefresh

def auto_refresh():
    """Handles automatic refreshing based on selected interval."""
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

    interval_map = {"5s": 5000, "10s": 10000, "30s": 30000, "1m": 60000}
    refresh_milliseconds = interval_map[refresh_interval]

    st_autorefresh(interval=refresh_milliseconds, key="auto_refresh")
    return refresh_interval
