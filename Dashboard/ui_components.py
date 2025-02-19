import streamlit as st

def render_column_configuration(all_columns, max_rows):
    """Renders the UI for column selection and configuration."""
    st.subheader("Column Configuration")

    # Header
    cols = st.columns([3, 2, 2, 1])
    with cols[0]: st.markdown("**Column**")
    with cols[1]: st.markdown("**Aggregation**")
    with cols[2]: st.markdown("**Alias**")
    with cols[3]: st.markdown("")

    # Initialize session state for active rows
    if 'active_rows' not in st.session_state:
        st.session_state.active_rows = [0]

    selected_columns, aggregations, aliases = [], [], []

    for row_id in st.session_state.active_rows:
        cols = st.columns([3, 2, 2, 1])

        with cols[0]:
            col = st.selectbox(f"Column {row_id}", options=all_columns, key=f"col_{row_id}")
            selected_columns.append(col)

        with cols[1]:
            agg = st.selectbox(f"Aggregation {row_id}", [None, "AVG", "SUM", "COUNT", "MAX", "MIN"], key=f"agg_{row_id}")
            aggregations.append(agg)

        with cols[2]:
            alias = st.text_input(f"Alias {row_id}", value=col, key=f"alias_{row_id}")
            aliases.append(alias)

        with cols[3]:
            if len(st.session_state.active_rows) > 1:
                if st.button("🗑️", key=f"remove_{row_id}"):
                    st.session_state.active_rows.remove(row_id)
                    st.rerun()

    # Add new row button
    if len(st.session_state.active_rows) < max_rows:
        if st.button("➕ Add Row"):
            new_id = max(st.session_state.active_rows) + 1
            st.session_state.active_rows.append(new_id)
            st.rerun()

    return selected_columns, aggregations, aliases
