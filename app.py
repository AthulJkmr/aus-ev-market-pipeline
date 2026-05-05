import streamlit as st
import pandas as pd
import sqlite3
import os
import plotly.express as px

st.set_page_config(page_title="EV Market Data", page_icon="🚗", layout="wide")

@st.cache_data(ttl=3600)
def load_data():
    db_path = os.path.join("output", "ev_market.db")
    if not os.path.exists(db_path):
        return pd.DataFrame()
    try:
        with sqlite3.connect(db_path) as conn:
            return pd.read_sql_query("SELECT * FROM vehicles", conn)
    except Exception as e:
        st.error(f"Failed to connect to database: {e}")
        return pd.DataFrame()

def main():
    st.title("Australian EV Market Dashboard")
    st.write("Tracking electric vehicle availability, specifications, and efficiency metrics.")

    df = load_data()

    if df.empty:
        st.warning("No data found. Please run the ETL scripts first.")
        return

    # Sidebar filters
    st.sidebar.header("Filters")
    mfg_options = df['Manufacturer'].unique().tolist()
    selected_mfg = st.sidebar.multiselect("Manufacturer", options=mfg_options, default=mfg_options)
    
    drivetrain_options = df['Drivetrain'].dropna().unique().tolist() if 'Drivetrain' in df.columns else []
    selected_drives = st.sidebar.multiselect("Drivetrain", options=drivetrain_options, default=drivetrain_options)

    # Apply filters
    filtered_df = df[df['Manufacturer'].isin(selected_mfg)]
    if selected_drives:
        filtered_df = filtered_df[filtered_df['Drivetrain'].isin(selected_drives)]

    if filtered_df.empty:
        st.info("No vehicles match the selected filters.")
        return

    # High-level metrics
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Models Tracked", len(filtered_df))
    col2.metric("Manufacturers", filtered_df['Manufacturer'].nunique())
    
    dominant_class = filtered_df['Vehicle_Class'].mode()[0] if 'Vehicle_Class' in filtered_df.columns and not filtered_df.empty else "N/A"
    col3.metric("Most Common Class", dominant_class)
    
    if 'Combined_MPGe' in filtered_df.columns and pd.to_numeric(filtered_df['Combined_MPGe'], errors='coerce').notnull().any():
        avg_eff = round(pd.to_numeric(filtered_df['Combined_MPGe'], errors='coerce').mean(), 1)
        col4.metric("Avg Combined MPGe", avg_eff)
    else:
        col4.metric("Avg Combined MPGe", "N/A")

    st.divider()

    # Main dashboard tabs
    tab1, tab2, tab3 = st.tabs(["Market Overview", "Efficiency", "Raw Data"])

    with tab1:
        c1, c2 = st.columns(2)
        with c1:
            st.subheader("Models per Manufacturer")
            bar_data = filtered_df['Manufacturer'].value_counts().reset_index()
            bar_data.columns = ['Manufacturer', 'Count']
            fig_bar = px.bar(bar_data, x='Manufacturer', y='Count', text='Count', template="plotly_dark")
            fig_bar.update_traces(textposition='outside')
            fig_bar.update_layout(xaxis_title="", yaxis_title="Count", showlegend=False)
            st.plotly_chart(fig_bar, use_container_width=True)

        with c2:
            st.subheader("Drivetrain Split")
            if 'Drivetrain' in filtered_df.columns and filtered_df['Drivetrain'].notnull().any():
                fig_sun = px.sunburst(filtered_df.fillna("Unknown"), path=['Manufacturer', 'Drivetrain'], template="plotly_dark")
                st.plotly_chart(fig_sun, use_container_width=True)
            else:
                st.write("Drivetrain data missing from source.")

    with tab2:
        st.subheader("City MPGe Distribution")
        if 'City_MPGe' in filtered_df.columns and pd.to_numeric(filtered_df['City_MPGe'], errors='coerce').notnull().any():
            eff_df = filtered_df.dropna(subset=['City_MPGe']).copy()
            eff_df['City_MPGe'] = pd.to_numeric(eff_df['City_MPGe'], errors='coerce')
            fig_box = px.box(eff_df, x="Manufacturer", y="City_MPGe", color="Manufacturer", template="plotly_dark", points="all")
            fig_box.update_layout(xaxis_title="", yaxis_title="City MPGe", showlegend=False)
            st.plotly_chart(fig_box, use_container_width=True)
        else:
            st.write("Efficiency data not available.")

    with tab3:
        st.subheader("Database Extract")
        st.dataframe(filtered_df, use_container_width=True, hide_index=True)

if __name__ == "__main__":
    main()