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
from components.chart_styles import (
    apply_premium_styling,
    create_gauge_chart,
    create_bar_chart,
    create_line_chart,
    create_radar_chart,
    create_heatmap,
    SCENEIQ_COLORS
)

def show_global_command():
    """Display the Global Command Center dashboard"""
    st.header("SceneIQ™ Global Command Center")
    
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
    
    # Create premium styled gauge chart
    fig = create_gauge_chart(
        value=avg_health,
        title="Overall Business Health",
        min_val=0,
        max_val=100,
        threshold=[40, 70],  # Thresholds for red, yellow, green coloring
        height=300
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Health status text with modern styling
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
    # Create a premium styled horizontal bar chart comparing stores
    fig = create_bar_chart(
        df=latest_health,
        x='overall_health',
        y='store',
        title="Store Health Comparison",
        height=300
    )
    
    # Update with horizontal orientation and color gradient
    fig.update_traces(
        orientation='h',
        marker=dict(
            color=latest_health['overall_health'],
            colorscale='RdYlGn',  # Red-Yellow-Green scale
            cmin=0,
            cmax=100,
            colorbar=dict(
                title="Health Score",
                thickness=20,
                len=0.7
            )
        )
    )
    
    # Sort bars by health score
    fig.update_layout(
        yaxis={'categoryorder': 'total ascending'}
    )
    
    st.plotly_chart(fig, use_container_width=True)

def show_health_trends(health_data):
    """Display business health trends over time"""
    # Group by date across all stores
    daily_health = health_data.groupby('date')['overall_health'].mean().reset_index()
    
    # Create premium styled line chart
    fig = create_line_chart(
        df=daily_health,
        x='date',
        y='overall_health',
        title="Business Health Trend",
        height=350
    )
    
    # Add colored background zones for health ranges
    fig.add_shape(
        type="rect",
        x0=daily_health['date'].min(),
        x1=daily_health['date'].max(),
        y0=0,
        y1=40,
        fillcolor=f"rgba({int(SCENEIQ_COLORS['secondary'][1:3], 16)}, {int(SCENEIQ_COLORS['secondary'][3:5], 16)}, {int(SCENEIQ_COLORS['secondary'][5:7], 16)}, 0.1)",
        line_width=0
    )
    
    fig.add_shape(
        type="rect",
        x0=daily_health['date'].min(),
        x1=daily_health['date'].max(),
        y0=40,
        y1=70,
        fillcolor=f"rgba({int(SCENEIQ_COLORS['tertiary'][1:3], 16)}, {int(SCENEIQ_COLORS['tertiary'][3:5], 16)}, {int(SCENEIQ_COLORS['tertiary'][5:7], 16)}, 0.1)",
        line_width=0
    )
    
    fig.add_shape(
        type="rect",
        x0=daily_health['date'].min(),
        x1=daily_health['date'].max(),
        y0=70,
        y1=100,
        fillcolor=f"rgba({int(SCENEIQ_COLORS['success'][1:3], 16)}, {int(SCENEIQ_COLORS['success'][3:5], 16)}, {int(SCENEIQ_COLORS['success'][5:7], 16)}, 0.1)",
        line_width=0
    )
    
    # Enhance the line
    fig.update_traces(
        line=dict(width=3),
        mode='lines+markers',
        marker=dict(size=8, symbol='circle')
    )
    
    # Set y-axis range and add grid
    fig.update_layout(
        yaxis=dict(
            range=[0, 100],
            title="Health Score",
            gridcolor='rgba(0,0,0,0.1)'
        ),
        xaxis=dict(
            title="",
            gridcolor='rgba(0,0,0,0.1)'
        )
    )
    
    st.plotly_chart(fig, use_container_width=True)

def show_metric_radar_chart(latest_health):
    """Display a radar chart showing all metrics for each store"""
    # Check if we have valid data
    if latest_health.empty:
        st.warning("No data available for radar chart")
        return
    
    # Get average metrics across stores, making sure to handle non-numeric data
    try:
        # Ensure we're only averaging numeric columns
        numeric_health = latest_health.select_dtypes(include=['number'])
        avg_metrics = numeric_health.mean()
        
        # Create radar chart
        categories = ['Theft Prevention', 'Rewards Program', 'Store Traffic', 'Employee Productivity']
        
        # Ensure we have all the required metrics
        if all(key in avg_metrics for key in ['theft_score', 'rewards_score', 'traffic_score', 'employee_score']):
            values = [
                avg_metrics['theft_score'],
                avg_metrics['rewards_score'],
                avg_metrics['traffic_score'],
                avg_metrics['employee_score']
            ]
            
            # Create premium styled radar chart
            fig = create_radar_chart(
                categories=categories,
                values=values,
                title="Performance by Category",
                height=350
            )
            
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("Missing required metrics for radar chart")
    except Exception as e:
        st.warning(f"Could not create radar chart: {str(e)}")
        # Create a placeholder radar chart with default values
        categories = ['Theft Prevention', 'Rewards Program', 'Store Traffic', 'Employee Productivity']
        values = [70, 65, 75, 60]
        
        # Create premium styled radar chart with sample data
        fig = create_radar_chart(
            categories=categories,
            values=values,
            title="Performance by Category (Sample Data)",
            height=350
        )
        
        st.plotly_chart(fig, use_container_width=True)
        st.caption("Displaying sample data due to data processing issues")

def show_metric_comparison(latest_health, metric):
    """Show a comparison of the selected metric across stores"""
    # Format the metric name for display
    metric_name = metric.replace('_', ' ').title()
    
    # Create a premium styled bar chart
    fig = create_bar_chart(
        df=latest_health,
        x=metric,
        y='store',
        title=f"{metric_name} Comparison",
        height=350
    )
    
    # Update with horizontal orientation and color gradient
    fig.update_traces(
        orientation='h',
        marker=dict(
            color=latest_health[metric],
            colorscale='RdYlGn',  # Red-Yellow-Green scale
            cmin=0,
            cmax=100,
            colorbar=dict(
                title=f"{metric_name} Score",
                thickness=20,
                len=0.7
            )
        )
    )
    
    # Sort bars by score value
    fig.update_layout(
        yaxis={'categoryorder': 'total ascending'}
    )
    
    # Add score labels at the end of each bar
    for i, value in enumerate(latest_health[metric]):
        fig.add_annotation(
            x=value,
            y=i,
            text=f"{value:.1f}",
            showarrow=False,
            xshift=10,
            font=dict(color="black", size=12)
        )
    
    st.plotly_chart(fig, use_container_width=True)
