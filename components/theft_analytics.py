"""
Theft Analytics Module - Visualizes theft patterns across stores and time periods
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

def show_theft_analytics():
    """Display theft analytics dashboard"""
    st.header("Theft Analytics")
    
    # Get filtered data based on selected stores and date range
    theft_data = get_filtered_theft_data()
    
    if theft_data.empty:
        st.warning("No theft data available for the selected stores and time period.")
        return
    
    # Dashboard layout
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Theft Incidents Overview")
        show_theft_kpis(theft_data)
    
    with col2:
        st.subheader("Severity Breakdown")
        show_severity_breakdown(theft_data)
    
    # Trend analysis
    st.subheader("Theft Incidents Trends")
    show_theft_trends(theft_data)
    
    # Store comparison
    st.subheader("Theft Comparison Across Stores")
    show_store_comparison(theft_data)
    
    # Heatmap analysis
    st.subheader("Theft Patterns Heatmap")
    show_heatmap_analysis(theft_data)
    
    # Incident details
    st.subheader("Incident Details")
    show_incident_details(theft_data)

def get_filtered_theft_data():
    """Get theft data filtered by selected stores and date range"""
    if 'theft_data' not in st.session_state:
        return pd.DataFrame()
    
    theft_data = st.session_state.theft_data.copy()
    
    # Filter by selected stores
    if st.session_state.selected_stores:
        theft_data = theft_data[theft_data['store'].isin(st.session_state.selected_stores)]
    
    # Filter by date range
    if st.session_state.date_range:
        start_date, end_date = st.session_state.date_range
        theft_data = theft_data[(theft_data['timestamp'] >= pd.Timestamp(start_date)) & 
                               (theft_data['timestamp'] <= pd.Timestamp(end_date))]
    
    return theft_data

def show_theft_kpis(theft_data):
    """Display key performance indicators for theft analytics"""
    # Calculate KPIs
    total_incidents = len(theft_data)
    total_value = theft_data['value'].sum()
    resolved_count = theft_data[theft_data['resolved']].shape[0]
    resolution_rate = (resolved_count / total_incidents * 100) if total_incidents > 0 else 0
    
    # Display metrics
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Total Theft Incidents", total_incidents)
        st.metric("Estimated Value Loss", f"${total_value}")
    
    with col2:
        st.metric("Resolved Incidents", f"{resolved_count} ({resolution_rate:.1f}%)")
        
        # Daily incident rate
        date_range = (theft_data['timestamp'].max() - theft_data['timestamp'].min()).days
        if date_range > 0:
            daily_rate = total_incidents / date_range
            st.metric("Daily Incident Rate", f"{daily_rate:.2f}")
        else:
            st.metric("Daily Incident Rate", "N/A")

def show_severity_breakdown(theft_data):
    """Show breakdown of theft incidents by severity"""
    # Count incidents by severity
    severity_counts = theft_data['severity'].value_counts().reset_index()
    severity_counts.columns = ['Severity', 'Count']
    
    # Create pie chart
    colors = {'Low': '#FFDC00', 'Medium': '#FF851B', 'High': '#FF4136'}
    
    fig = px.pie(
        severity_counts,
        names='Severity',
        values='Count',
        color='Severity',
        color_discrete_map=colors,
        hole=0.4
    )
    
    fig.update_layout(
        margin=dict(l=10, r=10, t=10, b=10),
        legend=dict(orientation="h", yanchor="bottom", y=0, xanchor="center", x=0.5)
    )
    
    st.plotly_chart(fig, use_container_width=True)

def show_theft_trends(theft_data):
    """Display trends in theft incidents over time"""
    # Aggregate by date
    theft_data['date'] = theft_data['timestamp'].dt.date
    daily_thefts = theft_data.groupby('date').size().reset_index(name='incidents')
    
    # Create line chart
    fig = px.line(
        daily_thefts,
        x='date',
        y='incidents',
        labels={'date': 'Date', 'incidents': 'Number of Incidents'},
        height=350
    )
    
    # Add trend line
    x = np.array(range(len(daily_thefts)))
    y = daily_thefts['incidents'].values
    
    if len(x) > 1:
        z = np.polyfit(x, y, 1)
        p = np.poly1d(z)
        
        fig.add_trace(go.Scatter(
            x=daily_thefts['date'],
            y=p(x),
            mode='lines',
            name='Trend',
            line=dict(color='red', dash='dash')
        ))
    
    fig.update_layout(
        margin=dict(l=0, r=0, t=10, b=0),
        xaxis_title="",
        yaxis_title="Incident Count"
    )
    
    st.plotly_chart(fig, use_container_width=True)

def show_store_comparison(theft_data):
    """Compare theft incidents across stores"""
    # Aggregate by store
    store_thefts = theft_data.groupby('store').agg(
        incidents=('store', 'count'),
        avg_value=('value', 'mean'),
        total_value=('value', 'sum')
    ).reset_index()
    
    # Create comparison visualization
    tab1, tab2 = st.tabs(["Incident Count", "Financial Impact"])
    
    with tab1:
        fig = px.bar(
            store_thefts,
            x='incidents',
            y='store',
            orientation='h',
            labels={'incidents': 'Number of Incidents', 'store': 'Store'},
            color='incidents',
            color_continuous_scale=['green', 'yellow', 'red'],
            height=300
        )
        
        fig.update_layout(
            margin=dict(l=0, r=0, t=10, b=0),
            coloraxis_showscale=False,
            yaxis={'categoryorder': 'total ascending'}
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        fig = px.bar(
            store_thefts,
            x='total_value',
            y='store',
            orientation='h',
            labels={'total_value': 'Total Value Loss ($)', 'store': 'Store'},
            color='total_value',
            color_continuous_scale=['green', 'yellow', 'red'],
            height=300
        )
        
        fig.update_layout(
            margin=dict(l=0, r=0, t=10, b=0),
            coloraxis_showscale=False,
            yaxis={'categoryorder': 'total ascending'}
        )
        
        st.plotly_chart(fig, use_container_width=True)

def show_heatmap_analysis(theft_data):
    """Display heatmap analysis of theft patterns by time and day"""
    try:
        # Prepare data for heatmap
        theft_data['hour'] = theft_data['timestamp'].dt.hour
        theft_data['day_of_week'] = theft_data['timestamp'].dt.day_name()
        
        # Day order for proper sorting
        day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        
        # Aggregate data by day and hour
        heatmap_data = theft_data.groupby(['day_of_week', 'hour']).size().reset_index(name='incidents')
        
        # Create pivot table for heatmap
        pivot_data = heatmap_data.pivot(index='day_of_week', columns='hour', values='incidents').reindex(day_order)
        pivot_data = pivot_data.fillna(0)
        
        # Ensure all hours are represented (0-23)
        for hour in range(24):
            if hour not in pivot_data.columns:
                pivot_data[hour] = 0
        
        # Sort columns to ensure they're in correct order
        pivot_data = pivot_data.sort_index(axis=1)
        
        # Generate heatmap
        fig = px.imshow(
            pivot_data,
            labels=dict(x="Hour of Day", y="Day of Week", color="Incident Count"),
            x=list(range(24)),
            y=day_order,
            aspect="auto",
            color_continuous_scale='Reds'
        )
    except Exception as e:
        st.error(f"Error creating heatmap: {str(e)}")
        # Create an empty figure as fallback
        fig = go.Figure()
        st.warning("Could not display heatmap due to data issue. Please check that there is theft data available for the selected time period and stores.")
    
    fig.update_layout(
        height=400,
        margin=dict(l=10, r=10, t=10, b=10),
        coloraxis_colorbar=dict(title="Count")
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Insights about the heatmap
    st.info("📈 **Insights**: The heatmap shows when theft incidents are most likely to occur during the week. Darker colors indicate higher incident frequency.")

def show_incident_details(theft_data):
    """Show detailed list of incidents with filtering options"""
    # Add ability to filter by severity
    severity_filter = st.multiselect(
        "Filter by severity:",
        options=sorted(theft_data['severity'].unique()),
        default=sorted(theft_data['severity'].unique())
    )
    
    # Apply filter
    if severity_filter:
        filtered_data = theft_data[theft_data['severity'].isin(severity_filter)]
    else:
        filtered_data = theft_data
    
    # Sort by timestamp descending
    display_data = filtered_data.sort_values('timestamp', ascending=False)
    
    # Create a more display-friendly DataFrame
    display_cols = ['store', 'timestamp', 'severity', 'value', 'resolved']
    
    # Format for display
    formatted_data = display_data[display_cols].copy()
    formatted_data['timestamp'] = formatted_data['timestamp'].dt.strftime('%Y-%m-%d %H:%M')
    formatted_data['value'] = formatted_data['value'].apply(lambda x: f"${x}")
    formatted_data['resolved'] = formatted_data['resolved'].apply(lambda x: "✅" if x else "❌")
    
    # Rename columns
    formatted_data.columns = ['Store', 'Timestamp', 'Severity', 'Value', 'Resolved']
    
    # Show the data with pagination
    st.dataframe(formatted_data, use_container_width=True)
    
    st.caption(f"Showing {len(formatted_data)} incidents. Scroll to see more.")
    
    # Video review functionality
    st.markdown("### Incident Video Review")
    
    # Create a list of sample timestamps for the video clips
    video_timestamps = [
        "2025-05-18 14:32:15",
        "2025-05-17 19:45:22",
        "2025-05-16 21:12:08",
        "2025-05-15 18:37:41",
        "2025-05-14 22:05:19"
    ]
    
    # Display video clip selection
    selected_clip = st.selectbox(
        "Select a clip to review:", 
        video_timestamps,
        format_func=lambda x: f"Incident on {x}"
    )
    
    # Display a simulated video player
    st.markdown("#### Video Player")
    col1, col2 = st.columns([3, 1])
    
    with col1:
        # Show a placeholder for the video player
        st.image("https://pixabay.com/get/g6eec510558dfa25600ff6660297034967d54f1947969e767b9be106b148e0400f769740e189a96ced3f80e9d3d6e9db1792b2425682f4f180c2103d453ce3d38_1280.jpg", 
                 caption=f"10-second clip from {selected_clip}")
    
    with col2:
        st.markdown("##### Clip Controls")
        st.button("▶️ Play")
        st.button("⏸️ Pause")
        st.slider("Time", 0, 10, 0)
        st.download_button("Download Clip", data=b"Sample video data", file_name=f"theft_clip_{selected_clip.replace(' ', '_').replace(':', '')}.mp4", mime="video/mp4")
    
    st.markdown("##### Clip Details")
    st.markdown(f"**Timestamp:** {selected_clip}")
    st.markdown("**Camera:** Front Entrance")
    st.markdown("**Duration:** 10 seconds")
    
    st.divider()
    
    # Export functionality
    col1, col2 = st.columns(2)
    with col1:
        st.download_button("Export All Clips", data=b"Sample video archive", file_name="theft_clips.zip", mime="application/zip")
    with col2:
        st.download_button("Export Incident List", data=formatted_data.to_csv(index=False), file_name="theft_incidents.csv", mime="text/csv")
