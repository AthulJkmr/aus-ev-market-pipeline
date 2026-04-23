import streamlit as st
import pandas as pd
import sqlite3
import os

# Configure the page layout
st.set_page_config(page_title="EV Market Analysis", page_icon="⚡", layout="wide")

def load_data():
    """Fetch cleaned vehicle data from local SQLite database."""
    db_path = os.path.join("output", "ev_market.db")
    
    try:
        conn = sqlite3.connect(db_path)
        query = "SELECT * FROM vehicles"
        df = pd.read_sql_query(query, conn)
        conn.close()
        return df
    except Exception as e:
        st.error(f"Failed to connect to database: {e}")
        return pd.DataFrame()

# Dashboard Header
st.title("⚡ EV & Hybrid Market Dashboard")
st.markdown("Automated pipeline tracking market availability and performance metrics.")

# Fetch and load data
df = load_data()

if not df.empty:
    # KPI Section
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Models Tracked", len(df))
    col2.metric("Unique Manufacturers", df['Manufacturer'].nunique())
    
    st.divider()
    
    # Data Table Section
    st.subheader("Current Market Data")
    # Display the dataframe with built-in sorting and scrolling
    st.dataframe(df, use_container_width=True, hide_index=True)
else:
    st.warning("No data available. Run the extraction and load scripts first.")