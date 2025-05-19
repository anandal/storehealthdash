"""
Database Administration Module - Provides interface for database management
"""

import streamlit as st
import pandas as pd
from database import save_data_to_db, load_data_from_db, init_db
from data_generator import generate_demo_data
import time

def show_database_admin():
    """Display database administration interface"""
    st.header("Database Administration")
    
    # Only allow owners to access this page
    if st.session_state.user_role != "Owner":
        st.warning("You need Owner privileges to access this page.")
        return
    
    st.markdown("""
    This module allows you to manage the dashboard's database. You can:
    - Save current data to the database
    - Load data from the database
    - Reset the database with new demo data
    """)
    
    # Database operations
    st.subheader("Database Operations")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("Save Data to Database", use_container_width=True):
            with st.spinner("Saving data to database..."):
                success = save_data_to_db()
                if success:
                    st.success("Data successfully saved to the database!")
                else:
                    st.error("Failed to save data to the database.")
    
    with col2:
        if st.button("Load Data from Database", use_container_width=True):
            with st.spinner("Loading data from database..."):
                success = load_data_from_db()
                if success:
                    st.success("Data successfully loaded from the database!")
                else:
                    st.error("Failed to load data from the database or no data available.")
    
    with col3:
        if st.button("Generate New Demo Data", use_container_width=True):
            if st.session_state.get('show_demo_warning', False):
                st.session_state.show_demo_warning = False
                with st.spinner("Generating new demo data..."):
                    generate_demo_data()
                    time.sleep(1)  # Give time for the UI to update
                    st.success("New demo data generated successfully!")
            else:
                st.session_state.show_demo_warning = True
                st.warning("⚠️ This will replace all current data with new demo data. Press again to confirm.")
    
    # Database status and statistics
    st.subheader("Database Status")
    
    # Show basic statistics about the data
    data_stats = []
    
    if 'store_info' in st.session_state:
        data_stats.append({"Category": "Stores", "Count": len(st.session_state.store_info)})
    
    if 'theft_data' in st.session_state:
        data_stats.append({"Category": "Theft Incidents", "Count": len(st.session_state.theft_data)})
    
    if 'rewards_data' in st.session_state:
        data_stats.append({"Category": "Rewards Records", "Count": len(st.session_state.rewards_data)})
    
    if 'traffic_patterns' in st.session_state:
        data_stats.append({"Category": "Traffic Patterns", "Count": len(st.session_state.traffic_patterns)})
    
    if 'daily_traffic' in st.session_state:
        data_stats.append({"Category": "Daily Traffic Records", "Count": len(st.session_state.daily_traffic)})
    
    if 'mobile_usage_patterns' in st.session_state:
        data_stats.append({"Category": "Mobile Usage Patterns", "Count": len(st.session_state.mobile_usage_patterns)})
    
    if 'shift_usage_data' in st.session_state:
        data_stats.append({"Category": "Employee Shift Records", "Count": len(st.session_state.shift_usage_data)})
    
    if 'business_health' in st.session_state:
        data_stats.append({"Category": "Business Health Records", "Count": len(st.session_state.business_health)})
    
    if data_stats:
        st.dataframe(pd.DataFrame(data_stats), use_container_width=True)
    else:
        st.info("No data available. Generate demo data or load from database.")
    
    # Database backup and restore (simulated)
    st.subheader("Backup & Restore")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Create Database Backup", use_container_width=True):
            st.info("Creating backup... (Simulated)")
            time.sleep(1)
            st.success(f"Backup created successfully: backup_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.sql")
    
    with col2:
        st.selectbox("Available Backups", 
                   ["backup_20250519_090000.sql", "backup_20250518_120000.sql", "backup_20250517_080000.sql"],
                   disabled=True)
        st.button("Restore Selected Backup", disabled=True, use_container_width=True)
    
    # Advanced settings
    st.subheader("Advanced Settings")
    
    with st.expander("Database Connection"):
        col1, col2 = st.columns(2)
        with col1:
            st.text_input("Database Host", value="localhost", disabled=True)
            st.text_input("Database Name", value="store_dashboard", disabled=True)
        with col2:
            st.text_input("Database User", value="postgres", disabled=True)
            st.text_input("Database Port", value="5432", disabled=True)
    
    # Data Export
    st.subheader("Data Export")
    
    export_type = st.selectbox("Select export format", ["CSV", "Excel", "JSON"])
    
    if st.button("Export All Data", use_container_width=True):
        st.info(f"Exporting all data as {export_type}... (Simulated)")
        time.sleep(1)
        st.success(f"Data exported successfully: store_data_{pd.Timestamp.now().strftime('%Y%m%d')}.{export_type.lower()}")
        
        if export_type == "CSV":
            # Create a sample CSV file for download
            if 'store_info' in st.session_state:
                csv = st.session_state.store_info.to_csv(index=False)
                st.download_button(
                    label="Download CSV",
                    data=csv,
                    file_name=f"store_data_{pd.Timestamp.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv"
                )