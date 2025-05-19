import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import time

# Import components
from components.global_command import show_global_command
from components.theft_analytics import show_theft_analytics
from components.rewards_analytics import show_rewards_analytics
from components.traffic_analytics import show_traffic_analytics
from components.employee_analytics import show_employee_analytics
from components.utils import (
    get_stores_data, 
    get_store_names, 
    get_user_role, 
    set_user_role,
    show_login_screen
)
from data_generator import generate_demo_data
from assets.store_images import show_store_images

# Set page configuration
st.set_page_config(
    page_title="Convenience Store Health Dashboard",
    page_icon="🏪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state variables
if 'initialized' not in st.session_state:
    st.session_state.initialized = True
    st.session_state.selected_stores = []
    st.session_state.date_range = (datetime.now() - timedelta(days=30), datetime.now())
    st.session_state.active_module = "Global Command Center"
    st.session_state.user_role = None
    st.session_state.selected_store = None
    
    # Generate demo data for all components
    generate_demo_data()

# Show login screen if user is not logged in
if st.session_state.user_role is None:
    show_login_screen()
else:
    # Main application layout
    col1, col2, col3 = st.columns([1, 3, 1])
    with col2:
        st.title("Convenience Store Health Dashboard")
        st.caption("Multi-store performance analytics and business intelligence")

    # User role indicator and logout button
    col_role, col_logout = st.sidebar.columns([3, 1])
    with col_role:
        st.sidebar.markdown(f"**Logged in as:** {st.session_state.user_role}")
    with col_logout:
        if st.sidebar.button("Logout"):
            set_user_role(None)
            st.rerun()

    # Date range selector
    st.sidebar.header("Time Period")
    date_option = st.sidebar.selectbox(
        "Select Time Period",
        ["Today", "Yesterday", "Last 7 Days", "Last 30 Days", "Custom"],
        index=3
    )

    if date_option == "Today":
        st.session_state.date_range = (datetime.now().replace(hour=0, minute=0, second=0), datetime.now())
    elif date_option == "Yesterday":
        yesterday = datetime.now() - timedelta(days=1)
        st.session_state.date_range = (yesterday.replace(hour=0, minute=0, second=0), yesterday.replace(hour=23, minute=59, second=59))
    elif date_option == "Last 7 Days":
        st.session_state.date_range = (datetime.now() - timedelta(days=7), datetime.now())
    elif date_option == "Last 30 Days":
        st.session_state.date_range = (datetime.now() - timedelta(days=30), datetime.now())
    elif date_option == "Custom":
        start_date = st.sidebar.date_input("Start Date", datetime.now() - timedelta(days=30))
        end_date = st.sidebar.date_input("End Date", datetime.now())
        if start_date and end_date:
            if start_date <= end_date:
                st.session_state.date_range = (start_date, end_date)
            else:
                st.sidebar.error("End date must be after start date")

    # Store selector
    stores = get_store_names()
    
    if st.session_state.user_role == "Owner":
        st.sidebar.header("Store Selection")
        store_selection_option = st.sidebar.radio(
            "Choose stores to view",
            ["All Stores", "Select Specific Stores"]
        )
        
        if store_selection_option == "All Stores":
            st.session_state.selected_stores = stores
        else:
            st.session_state.selected_stores = st.sidebar.multiselect(
                "Select stores to view", 
                stores,
                default=stores[:2]
            )
            if not st.session_state.selected_stores:
                st.session_state.selected_stores = stores[:1]
    else:  # Manager
        # Managers can only see their assigned store
        st.sidebar.header("Your Store")
        st.session_state.selected_store = st.sidebar.selectbox(
            "Your assigned store", 
            [st.session_state.selected_store if st.session_state.selected_store else stores[0]]
        )
        st.session_state.selected_stores = [st.session_state.selected_store]

    # Module navigation
    st.sidebar.header("Dashboard Modules")
    modules = [
        "Global Command Center",
        "Theft Analytics",
        "Rewards Program Analytics",
        "Store Visit & Traffic Analytics",
        "Employee Productivity"
    ]
    selected_module = st.sidebar.radio("Select Module", modules)
    st.session_state.active_module = selected_module

    # Display the export options
    st.sidebar.header("Export Options")
    export_format = st.sidebar.selectbox("Export format", ["PDF", "CSV"])
    if st.sidebar.button("Export Current View"):
        st.sidebar.success(f"Exporting data as {export_format}... (Demo)")
        time.sleep(1)
        st.sidebar.download_button(
            label=f"Download {export_format}",
            data=b"Sample data for download",
            file_name=f"dashboard_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{export_format.lower()}",
            mime=f"application/{export_format.lower()}"
        )

    # Main content area
    st.divider()
    
    # Display the selected module
    if selected_module == "Global Command Center":
        show_global_command()
    elif selected_module == "Theft Analytics":
        show_theft_analytics()
    elif selected_module == "Rewards Program Analytics":
        show_rewards_analytics()
    elif selected_module == "Store Visit & Traffic Analytics":
        show_traffic_analytics()
    elif selected_module == "Employee Productivity":
        show_employee_analytics()

    # Show store images at the bottom if needed
    if st.checkbox("Show Store Images", value=False):
        show_store_images()
