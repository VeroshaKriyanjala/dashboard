def generate_query(selected_columns, aggregations, aliases, table_name):
    """Generates SQL query based on selected columns, aggregations, and aliases."""
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
