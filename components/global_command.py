"""
Global Command Center Module - Main overview dashboard showing health metrics
across all selected stores
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

def show_global_command():
    """Display the Global Command Center dashboard"""
    st.header("Global Command Center")
    
    # Get filtered data based on selected stores and date range
    health_data = get_filtered_health_data()
    
    if health_data.empty:
        st.warning("No data available for the selected stores and time period.")
        return
    
    # Calculate latest health scores
    latest_health = health_data.sort_values('date').groupby('store').last().reset_index()
    
    # Dashboard layout 
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.subheader("Business Health Overview")
        show_health_dial(latest_health)
        
    with col2:
        st.subheader("Critical Alerts")
        show_alerts(health_data)
    
    # Health metrics by store
    st.subheader("Health Metrics by Store")
    show_health_by_store(latest_health)
    
    # Health trends over time
    st.subheader("Business Health Trends")
    show_health_trends(health_data)
    
    # Show metric comparisons
    st.subheader("Key Performance Areas")
    col1, col2 = st.columns(2)
    
    with col1:
        show_metric_radar_chart(latest_health)
    
    with col2:
        metric_to_show = st.selectbox(
            "Select metric to analyze:", 
            ["overall_health", "theft_score", "rewards_score", "traffic_score", "employee_score"],
            format_func=lambda x: x.replace('_', ' ').title()
        )
        show_metric_comparison(latest_health, metric_to_show)

def get_filtered_health_data():
    """Get health data filtered by selected stores and date range"""
    if 'business_health' not in st.session_state:
        return pd.DataFrame()
    
    health_data = st.session_state.business_health.copy()
    
    # Filter by selected stores
    if st.session_state.selected_stores:
        health_data = health_data[health_data['store'].isin(st.session_state.selected_stores)]
    
    # Filter by date range
    if st.session_state.date_range:
        start_date, end_date = st.session_state.date_range
        health_data = health_data[(health_data['date'] >= pd.Timestamp(start_date)) & 
                                 (health_data['date'] <= pd.Timestamp(end_date))]
    
    return health_data

def show_health_dial(latest_health):
    """Display an overall health dial for all selected stores"""
    # Get average health across all selected stores
    avg_health = latest_health['overall_health'].mean()
    
    # Create gauge/dial chart
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=avg_health,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Overall Business Health"},
        gauge={
            'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "darkblue"},
            'bar': {'color': "darkblue"},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, 40], 'color': '#FF4136'},  # Red
                {'range': [40, 70], 'color': '#FFDC00'},  # Yellow
                {'range': [70, 100], 'color': '#2ECC40'}  # Green
            ],
        }
    ))
    
    fig.update_layout(
        height=300,
        margin=dict(l=30, r=30, t=30, b=0),
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Health status text
    if avg_health >= 70:
        st.success("Business health is GOOD")
    elif avg_health >= 40:
        st.warning("Business health needs ATTENTION")
    else:
        st.error("Business health is CRITICAL")

def show_alerts(health_data):
    """Display critical alerts for the selected stores and time period"""
    # Get the most recent data for each store
    recent_data = health_data.sort_values('date').groupby('store').last().reset_index()
    
    # Collect all alerts
    all_alerts = []
    for _, row in recent_data.iterrows():
        if isinstance(row['alerts'], list) and row['alerts']:
            for alert in row['alerts']:
                all_alerts.append({
                    'store': row['store'],
                    'alert': alert,
                    'date': row['date']
                })
    
    # If no alerts, show a message
    if not all_alerts:
        st.info("No critical alerts at this time.")
        return
    
    # Display alerts in a color-coded format
    alert_df = pd.DataFrame(all_alerts)
    
    for i, row in alert_df.iterrows():
        alert_text = f"🚨 **{row['store']}**: {row['alert']} ({row['date'].strftime('%m/%d/%Y')})"
        st.error(alert_text)
    
    # Additional "historical" alerts that might be interesting
    st.markdown("---")
    st.caption("Recent Notifications:")
    st.info("📊 Weekly performance report available for download")
    st.warning("⚠️ Riverside Convenience: Rewards program engagement down 5% this week")

def show_health_by_store(latest_health):
    """Show health metrics for each store in a bar chart"""
    # Create a horizontal bar chart comparing stores
    fig = px.bar(
        latest_health,
        x='overall_health',
        y='store',
        orientation='h',
        color='overall_health',
        color_continuous_scale=['red', 'yellow', 'green'],
        range_color=[0, 100],
        labels={'overall_health': 'Business Health Score', 'store': 'Store'},
        height=300
    )
    
    fig.update_layout(
        margin=dict(l=0, r=0, t=10, b=0),
        coloraxis_showscale=False,
        yaxis={'categoryorder': 'total ascending'}
    )
    
    st.plotly_chart(fig, use_container_width=True)

def show_health_trends(health_data):
    """Display business health trends over time"""
    # Group by date across all stores
    daily_health = health_data.groupby('date')['overall_health'].mean().reset_index()
    
    # Create line chart
    fig = px.line(
        daily_health,
        x='date',
        y='overall_health',
        labels={'date': 'Date', 'overall_health': 'Business Health Score'},
        height=300
    )
    
    fig.update_layout(
        margin=dict(l=0, r=0, t=10, b=0),
        xaxis_title="",
        yaxis_title="Health Score",
        yaxis_range=[0, 100]
    )
    
    # Add colored background zones
    fig.add_shape(
        type="rect",
        x0=daily_health['date'].min(),
        x1=daily_health['date'].max(),
        y0=0,
        y1=40,
        fillcolor="rgba(255, 65, 54, 0.2)",
        line_width=0
    )
    
    fig.add_shape(
        type="rect",
        x0=daily_health['date'].min(),
        x1=daily_health['date'].max(),
        y0=40,
        y1=70,
        fillcolor="rgba(255, 220, 0, 0.2)",
        line_width=0
    )
    
    fig.add_shape(
        type="rect",
        x0=daily_health['date'].min(),
        x1=daily_health['date'].max(),
        y0=70,
        y1=100,
        fillcolor="rgba(46, 204, 64, 0.2)",
        line_width=0
    )
    
    st.plotly_chart(fig, use_container_width=True)

def show_metric_radar_chart(latest_health):
    """Display a radar chart showing all metrics for each store"""
    # Get average metrics across stores
    avg_metrics = latest_health.mean()
    
    # Create radar chart
    categories = ['Theft Prevention', 'Rewards Program', 'Store Traffic', 'Employee Productivity']
    values = [
        avg_metrics['theft_score'],
        avg_metrics['rewards_score'],
        avg_metrics['traffic_score'],
        avg_metrics['employee_score']
    ]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        name='Business Performance'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100]
            )
        ),
        showlegend=False,
        height=350,
        margin=dict(l=10, r=10, t=10, b=10)
    )
    
    st.plotly_chart(fig, use_container_width=True)

def show_metric_comparison(latest_health, metric):
    """Show a comparison of the selected metric across stores"""
    # Format the metric name for display
    metric_name = metric.replace('_', ' ').title()
    
    # Create a horizontal bar chart
    fig = px.bar(
        latest_health,
        x=metric,
        y='store',
        orientation='h',
        color=metric,
        color_continuous_scale=['red', 'yellow', 'green'],
        range_color=[0, 100],
        labels={metric: f'{metric_name} Score', 'store': 'Store'},
        height=350
    )
    
    fig.update_layout(
        margin=dict(l=0, r=0, t=10, b=10),
        coloraxis_showscale=False,
        yaxis={'categoryorder': 'total ascending'}
    )
    
    st.plotly_chart(fig, use_container_width=True)
