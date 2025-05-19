"""
Rewards Program Analytics Module - Visualizes member engagement and campaign performance
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

def show_rewards_analytics():
    """Display rewards program analytics dashboard"""
    st.header("Rewards Program Analytics")
    
    # Get filtered data based on selected stores and date range
    rewards_data = get_filtered_rewards_data()
    campaign_data = get_filtered_campaign_data()
    
    if rewards_data.empty:
        st.warning("No rewards data available for the selected stores and time period.")
        return
    
    # Dashboard layout
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Rewards Program Overview")
        show_rewards_kpis(rewards_data)
    
    with col2:
        st.subheader("Member Growth")
        show_member_growth(rewards_data)
    
    # Campaign performance
    st.subheader("Campaign Performance")
    show_campaign_performance(campaign_data)
    
    # Store comparison
    st.subheader("Rewards Program Comparison Across Stores")
    show_store_comparison(rewards_data)
    
    # Active campaigns and engagement
    st.subheader("Campaign Engagement Trends")
    show_campaign_engagement(rewards_data)

def get_filtered_rewards_data():
    """Get rewards data filtered by selected stores and date range"""
    if 'rewards_data' not in st.session_state:
        return pd.DataFrame()
    
    rewards_data = st.session_state.rewards_data.copy()
    
    # Filter by selected stores
    if st.session_state.selected_stores:
        rewards_data = rewards_data[rewards_data['store'].isin(st.session_state.selected_stores)]
    
    # Filter by date range
    if st.session_state.date_range:
        start_date, end_date = st.session_state.date_range
        rewards_data = rewards_data[(rewards_data['date'] >= pd.Timestamp(start_date)) & 
                                   (rewards_data['date'] <= pd.Timestamp(end_date))]
    
    return rewards_data

def get_filtered_campaign_data():
    """Get campaign data filtered by selected stores"""
    if 'campaign_performance' not in st.session_state:
        return pd.DataFrame()
    
    campaign_data = st.session_state.campaign_performance.copy()
    
    # Filter by selected stores
    if st.session_state.selected_stores:
        campaign_data = campaign_data[campaign_data['store'].isin(st.session_state.selected_stores)]
    
    return campaign_data

def show_rewards_kpis(rewards_data):
    """Display key performance indicators for rewards program"""
    # Get latest data for each store to calculate current totals
    latest_data = rewards_data.sort_values('date').groupby('store').last().reset_index()
    
    # Calculate KPIs
    total_members = latest_data['total_members'].sum()
    avg_campaign_engagement = rewards_data['campaign_engagement'].mean() * 100  # Convert to percentage
    
    # Calculate new member acquisition over the period
    first_data = rewards_data.sort_values('date').groupby('store').first().reset_index()
    latest_data = rewards_data.sort_values('date').groupby('store').last().reset_index()
    
    new_members = (latest_data['total_members'].sum() - first_data['total_members'].sum())
    
    # Display metrics
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Total Active Members", f"{total_members:,}")
        
        # Calculate daily growth rate
        date_range = (rewards_data['date'].max() - rewards_data['date'].min()).days
        if date_range > 0:
            daily_growth = new_members / date_range
            st.metric("Daily Member Growth", f"{daily_growth:.1f}")
        else:
            st.metric("Daily Member Growth", "N/A")
    
    with col2:
        st.metric("New Members in Period", f"{new_members:,}")
        st.metric("Avg. Campaign Engagement", f"{avg_campaign_engagement:.1f}%")

def show_member_growth(rewards_data):
    """Show member growth over time"""
    # Aggregate total members by date across all stores
    daily_members = rewards_data.groupby('date')['total_members'].sum().reset_index()
    
    # Create line chart
    fig = px.line(
        daily_members,
        x='date',
        y='total_members',
        labels={'date': 'Date', 'total_members': 'Total Members'},
        height=250
    )
    
    fig.update_layout(
        margin=dict(l=0, r=0, t=10, b=0),
        xaxis_title="",
        yaxis_title="Members"
    )
    
    st.plotly_chart(fig, use_container_width=True)

def show_campaign_performance(campaign_data):
    """Display performance of different campaigns"""
    if campaign_data.empty:
        st.warning("No campaign data available for the selected stores.")
        return
    
    # View options
    view_option = st.radio(
        "View by:",
        ["Participation Rate", "Redemption Rate", "ROI"],
        horizontal=True
    )
    
    # Map option to column
    column_map = {
        "Participation Rate": "participation_rate",
        "Redemption Rate": "redemption_rate",
        "ROI": "roi"
    }
    
    column = column_map[view_option]
    
    # Aggregate data by campaign
    campaign_summary = campaign_data.groupby('campaign')[column].mean().reset_index()
    campaign_summary = campaign_summary.sort_values(column, ascending=False)
    
    # Create bar chart
    fig = px.bar(
        campaign_summary,
        x='campaign',
        y=column,
        color=column,
        color_continuous_scale='Blues',
        labels={'campaign': 'Campaign', column: view_option},
        height=300
    )
    
    fig.update_layout(
        margin=dict(l=0, r=0, t=10, b=0),
        coloraxis_showscale=False,
        xaxis_title=""
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Show detailed campaign data
    with st.expander("View Campaign Details"):
        # Average metrics by campaign across all stores
        campaign_details = campaign_data.groupby('campaign').agg({
            'participation_rate': 'mean',
            'redemption_rate': 'mean',
            'roi': 'mean'
        }).reset_index()
        
        campaign_details.columns = ['Campaign', 'Participation Rate (%)', 'Redemption Rate (%)', 'ROI']
        
        # Format for display
        campaign_details['Participation Rate (%)'] = campaign_details['Participation Rate (%)'].round(1)
        campaign_details['Redemption Rate (%)'] = campaign_details['Redemption Rate (%)'].round(1)
        campaign_details['ROI'] = campaign_details['ROI'].apply(lambda x: f"{x:.2f}x")
        
        st.dataframe(campaign_details, use_container_width=True)

def show_store_comparison(rewards_data):
    """Compare rewards program performance across stores"""
    # Get latest data for each store
    latest_data = rewards_data.sort_values('date').groupby('store').last().reset_index()
    
    # Create comparison visualization
    tab1, tab2 = st.tabs(["Member Count", "New Member Growth"])
    
    with tab1:
        # Sort by total members
        latest_data_sorted = latest_data.sort_values('total_members')
        
        fig = px.bar(
            latest_data_sorted,
            x='total_members',
            y='store',
            orientation='h',
            labels={'total_members': 'Total Members', 'store': 'Store'},
            color='total_members',
            color_continuous_scale='Blues',
            height=300
        )
        
        fig.update_layout(
            margin=dict(l=0, r=0, t=10, b=0),
            coloraxis_showscale=False
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        # Calculate new members in period for each store
        first_data = rewards_data.sort_values('date').groupby('store').first().reset_index()
        latest_data = rewards_data.sort_values('date').groupby('store').last().reset_index()
        
        growth_data = pd.DataFrame({
            'store': latest_data['store'],
            'new_members': latest_data['total_members'] - first_data['total_members']
        })
        
        growth_data_sorted = growth_data.sort_values('new_members')
        
        fig = px.bar(
            growth_data_sorted,
            x='new_members',
            y='store',
            orientation='h',
            labels={'new_members': 'New Members in Period', 'store': 'Store'},
            color='new_members',
            color_continuous_scale='Blues',
            height=300
        )
        
        fig.update_layout(
            margin=dict(l=0, r=0, t=10, b=0),
            coloraxis_showscale=False
        )
        
        st.plotly_chart(fig, use_container_width=True)

def show_campaign_engagement(rewards_data):
    """Show campaign engagement trends over time"""
    # Aggregate campaign engagement by date
    engagement_data = rewards_data.groupby('date')[['campaign_engagement', 'active_campaigns']].mean().reset_index()
    
    # Create dual-axis chart
    fig = go.Figure()
    
    # Add campaign engagement line
    fig.add_trace(go.Scatter(
        x=engagement_data['date'],
        y=engagement_data['campaign_engagement'] * 100,  # Convert to percentage
        name='Engagement Rate',
        line=dict(color='royalblue', width=3)
    ))
    
    # Add active campaigns line
    fig.add_trace(go.Scatter(
        x=engagement_data['date'],
        y=engagement_data['active_campaigns'],
        name='Active Campaigns',
        line=dict(color='green', width=2, dash='dash'),
        yaxis='y2'
    ))
    
    # Update layout for dual y-axes
    fig.update_layout(
        height=350,
        margin=dict(l=0, r=0, t=10, b=0),
        xaxis=dict(title=""),
        yaxis=dict(
            title="Engagement Rate (%)",
            titlefont=dict(color='royalblue'),
            tickfont=dict(color='royalblue')
        ),
        yaxis2=dict(
            title="Active Campaigns",
            titlefont=dict(color='green'),
            tickfont=dict(color='green'),
            anchor="x",
            overlaying="y",
            side="right"
        ),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Rewards usage breakdown
    st.subheader("Rewards Usage")
    
    # Mock data for rewards popularity
    rewards = ['Free Coffee', 'Discount Coupon', 'Loyalty Points', 'Free Snack']
    popularity = [42, 28, 20, 10]
    
    fig = px.pie(
        names=rewards,
        values=popularity,
        hole=0.4,
        labels={'names': 'Reward Type', 'values': 'Popularity (%)'}
    )
    
    fig.update_layout(
        height=300,
        margin=dict(l=0, r=0, t=10, b=0),
        legend=dict(orientation="h", yanchor="bottom", y=0, xanchor="center", x=0.5)
    )
    
    st.plotly_chart(fig, use_container_width=True)
