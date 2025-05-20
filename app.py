import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import time
import os

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
from components.database_admin import show_database_admin
from components.ai_assistant import show_ai_assistant
from data_generator import generate_demo_data
from assets.store_images import show_store_images
from database import init_db, save_data_to_db, load_data_from_db

# Set page configuration
st.set_page_config(
    page_title="SceneIQ Store Health Dashboard",
    page_icon="🏪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Set custom theme with modern colors
st.markdown("""
<style>
    :root {
        --primary-color: #4285F4;
        --background-color: #f9f9f9;
        --secondary-background-color: #ffffff;
        --text-color: #262730;
        --font: 'Roboto', sans-serif;
    }
    
    /* Modern card styling */
    div.stBlock, div.stAlert {
        border-radius: 8px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        padding: 20px;
        background: white;
        border: none !important;
    }
    
    /* Button styling */
    .stButton>button {
        border-radius: 6px;
        font-weight: 500;
        transition: all 0.3s ease;
    }
    
    /* Header styling */
    h1, h2, h3 {
        font-weight: 600 !important;
        color: #1E3A8A !important;
    }
    
    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background-color: #ffffff;
        border-right: 1px solid #f0f0f0;
    }
    
    /* Widget label emphasis */
    .stSelectbox>label, .stSlider>label, .stDateInput>label {
        font-weight: 500 !important;
    }
    
    /* Improved metric styling */
    div[data-testid="stMetric"] {
        background: linear-gradient(to right, #f0f8ff, #ffffff);
        padding: 10px;
        border-radius: 8px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }
    
    /* Chart container styling */
    div[data-testid="stPlotlyChart"] {
        border-radius: 16px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        margin-bottom: 25px;
        padding: 12px;
        background: white;
        overflow: hidden;
    }
    
    /* Chart content styling for curved corners (works with Plotly) */
    .js-plotly-plot .plotly .main-svg {
        border-radius: 12px;
    }
    
    /* Style for bars to look more modern */
    .bar rect {
        rx: 6px;
        ry: 6px;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state variables
if 'initialized' not in st.session_state:
    st.session_state.initialized = True
    
    # Initialize with demo store selection
    demo_stores = ["Downtown Mart", "Riverside Convenience", "Oakwood Express", "Sunset Shop & Go"]
    st.session_state.selected_stores = demo_stores[:2]  # Select first two stores by default
    
    # Set other defaults
    st.session_state.date_range = (datetime.now() - timedelta(days=30), datetime.now())
    st.session_state.active_module = "Global Command Center"
    st.session_state.user_role = None
    st.session_state.selected_store = None
    
    # Initialize demo data for display
    generate_demo_data()
    
    # Make sure session state has selected stores
    if 'selected_stores' not in st.session_state or not st.session_state.selected_stores:
        st.session_state.selected_stores = ["Downtown Mart", "Riverside Convenience"]
    
    # Initialize the database if needed
    try:
        init_db()
        # Try to load data from database (but we already have session data)
        load_data_from_db()
    except Exception as e:
        # Just use the session data we already generated
        pass

# Show login screen if user is not logged in
if st.session_state.user_role is None:
    show_login_screen()
else:
    # Main application layout
    col1, col2, col3 = st.columns([1, 3, 1])
    with col2:
        st.title("SceneIQ™ Store Health Dashboard")
        st.caption("Multi-store performance analytics and business intelligence by SceneIQ")

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

    # Define available modules based on user role
    if st.session_state.user_role == "Owner":
        modules = [
            {"name": "Global Command Center", "icon": "🌐", "desc": "Overview of all store metrics"},
            {"name": "Theft Analytics", "icon": "🚨", "desc": "Monitor theft incidents across stores"},
            {"name": "Rewards Program Analytics", "icon": "🎁", "desc": "Track rewards program performance"},
            {"name": "Store Visit & Traffic Analytics", "icon": "👥", "desc": "Analyze customer traffic patterns"},
            {"name": "Employee Productivity", "icon": "📱", "desc": "Monitor employee mobile usage"},
            {"name": "AI Assistant", "icon": "🤖", "desc": "Get insights from your data"},
            {"name": "Database Admin", "icon": "⚙️", "desc": "Manage database settings"}  # Only owners can access database admin
        ]
    else:
        modules = [
            {"name": "Global Command Center", "icon": "🌐", "desc": "Overview of all store metrics"},
            {"name": "Theft Analytics", "icon": "🚨", "desc": "Monitor theft incidents across stores"},
            {"name": "Rewards Program Analytics", "icon": "🎁", "desc": "Track rewards program performance"},
            {"name": "Store Visit & Traffic Analytics", "icon": "👥", "desc": "Analyze customer traffic patterns"},
            {"name": "Employee Productivity", "icon": "📱", "desc": "Monitor employee mobile usage"},
            {"name": "AI Assistant", "icon": "🤖", "desc": "Get insights from your data"}
        ]
    
    # Simple compact header
    st.markdown("""
    <style>
    div.row-widget.stButton {
        margin: 0px;
        padding: 0px;
    }
    div.stButton > button {
        padding: 2px 5px;
        font-size: 0.7em;
        height: 30px;
        min-height: 30px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Simple and reliable row layout
    header_cols = st.columns([1, 3])
    with header_cols[0]:
        st.markdown("### 🏪 SceneIQ")
    with header_cols[1]:
        st.markdown(f"**{st.session_state.active_module}** | {datetime.now().strftime('%B %d, %Y')}")
    
    # Create ultra-compact horizontal navigation
    cols = st.columns(len(modules))
    for i, module in enumerate(modules):
        with cols[i]:
            btn_style = "primary" if module["name"] == st.session_state.active_module else "secondary"
            btn_label = f"{module['icon']}" # Just show icons to save space
            if st.button(
                btn_label, 
                key=f"nav_{module['name']}", 
                help=module['name'] + ": " + module['desc'],
                type=btn_style,
                use_container_width=True
            ):
                st.session_state.active_module = module["name"]
                st.rerun()
    
    # Add a thin separator line and no extra spacing
    st.markdown('<hr style="height:1px;border:none;background-color:#e0e0e0;margin:0;">', unsafe_allow_html=True)
    
    selected_module = st.session_state.active_module

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
    elif selected_module == "AI Assistant":
        show_ai_assistant()
    elif selected_module == "Database Admin":
        show_database_admin()

    # Show store images at the bottom if needed
    if st.checkbox("Show Store Images", value=False):
        show_store_images()
