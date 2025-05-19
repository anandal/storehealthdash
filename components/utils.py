"""
Utility functions for the dashboard
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def get_stores_data():
    """Get data for all stores"""
    if 'store_info' not in st.session_state:
        return pd.DataFrame()
    
    return st.session_state.store_info

def get_store_names():
    """Get list of all store names"""
    stores_data = get_stores_data()
    if stores_data.empty:
        return ["Store 1", "Store 2", "Store 3"]  # Fallback
    
    return stores_data['store_name'].tolist()

def get_user_role():
    """Get current user role"""
    return st.session_state.user_role

def set_user_role(role):
    """Set user role (Owner or Manager)"""
    st.session_state.user_role = role
    
    # If switching to Manager, make sure a store is selected
    if role == "Manager" and not st.session_state.selected_store:
        st.session_state.selected_store = get_store_names()[0]
        st.session_state.selected_stores = [st.session_state.selected_store]

def show_login_screen():
    """Show login screen for role selection"""
    st.markdown("## Welcome to the Convenience Store Health Dashboard")
    st.markdown("### Please select your role to continue")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("")
        st.markdown("")
        
        # Create a card-like container for login
        with st.container():
            st.markdown("#### Select your role")
            
            role = st.radio(
                "Your role in the business",
                ["Owner", "Manager"],
                horizontal=True,
                label_visibility="collapsed"
            )
            
            if role == "Owner":
                st.markdown("As an **Owner**, you'll have access to data across all stores with comprehensive comparative analytics.")
            else:
                st.markdown("As a **Manager**, you'll focus on data specific to your assigned store(s).")
            
            # Store selection for manager
            if role == "Manager":
                store_options = get_store_names()
                selected_store = st.selectbox(
                    "Select your store",
                    store_options
                )
                st.session_state.selected_store = selected_store
            
            st.markdown("")
            
            if st.button("Login", use_container_width=True):
                set_user_role(role)
                st.success(f"Logged in as {role}")
                st.rerun()

def format_date_range(date_range):
    """Format date range for display"""
    if not date_range or len(date_range) != 2:
        return "No date range selected"
    
    start_date, end_date = date_range
    return f"{start_date.strftime('%b %d, %Y')} to {end_date.strftime('%b %d, %Y')}"

def get_health_color(score):
    """Get color based on health score"""
    if score >= 70:
        return "green"
    elif score >= 40:
        return "orange"
    else:
        return "red"
