"""
Store Visit & Traffic Analytics Module - Visualizes visitor patterns and trends
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

def show_traffic_analytics():
    """Display store visit and traffic analytics dashboard"""
    st.header("Store Visit & Traffic Analytics")
    
    # Get filtered data based on selected stores and date range
    traffic_patterns = get_filtered_traffic_patterns()
    daily_traffic = get_filtered_daily_traffic()
    
    if traffic_patterns.empty or daily_traffic.empty:
        st.warning("No traffic data available for the selected stores and time period.")
        return
    
    # Dashboard layout
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Traffic Overview")
        show_traffic_kpis(daily_traffic)
    
    with col2:
        st.subheader("Traffic Distribution")
        show_traffic_distribution(daily_traffic)
    
    # Visitor trends
    st.subheader("Visitor Traffic Trends")
    show_visitor_trends(daily_traffic)
    
    # Store comparison
    st.subheader("Traffic Comparison Across Stores")
    show_store_comparison(daily_traffic)
    
    # Heatmap analysis
    st.subheader("Traffic Patterns Heatmap")
    show_heatmap_analysis(traffic_patterns)
    
    # Combined analysis
    st.subheader("Traffic vs. Theft Analysis")
    show_combined_analysis()

def get_filtered_traffic_patterns():
    """Get traffic pattern data filtered by selected stores"""
    if 'traffic_patterns' not in st.session_state:
        return pd.DataFrame()
    
    traffic_data = st.session_state.traffic_patterns.copy()
    
    # Filter by selected stores
    if st.session_state.selected_stores:
        traffic_data = traffic_data[traffic_data['store'].isin(st.session_state.selected_stores)]
    
    return traffic_data

def get_filtered_daily_traffic():
    """Get daily traffic data filtered by selected stores and date range"""
    if 'daily_traffic' not in st.session_state:
        return pd.DataFrame()
    
    traffic_data = st.session_state.daily_traffic.copy()
    
    # Filter by selected stores
    if st.session_state.selected_stores:
        traffic_data = traffic_data[traffic_data['store'].isin(st.session_state.selected_stores)]
    
    # Filter by date range
    if st.session_state.date_range:
        start_date, end_date = st.session_state.date_range
        traffic_data = traffic_data[(traffic_data['date'] >= pd.Timestamp(start_date)) & 
                                   (traffic_data['date'] <= pd.Timestamp(end_date))]
    
    return traffic_data

def show_traffic_kpis(daily_traffic):
    """Display key performance indicators for store traffic"""
    # Calculate KPIs
    total_visitors = daily_traffic['total_visitors'].sum()
    avg_daily_visitors = daily_traffic.groupby('date')['total_visitors'].sum().mean()
    
    # Calculate growth rate
    first_week = daily_traffic[daily_traffic['date'] <= daily_traffic['date'].min() + timedelta(days=7)]
    last_week = daily_traffic[daily_traffic['date'] >= daily_traffic['date'].max() - timedelta(days=7)]
    
    first_week_avg = first_week.groupby('date')['total_visitors'].sum().mean()
    last_week_avg = last_week.groupby('date')['total_visitors'].sum().mean()
    
    if first_week_avg > 0:
        growth_rate = (last_week_avg - first_week_avg) / first_week_avg * 100
    else:
        growth_rate = 0
    
    # Display metrics
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Total Visitors", f"{total_visitors:,}")
        st.metric("Average Daily Visitors", f"{int(avg_daily_visitors):,}")
    
    with col2:
        # Calculate busiest day
        busiest_date = daily_traffic.groupby('date')['total_visitors'].sum().idxmax()
        busiest_day = busiest_date.strftime("%A, %b %d")
        busiest_count = daily_traffic[daily_traffic['date'] == busiest_date]['total_visitors'].sum()
        
        st.metric("Busiest Day", f"{busiest_day} ({busiest_count:,} visitors)")
        st.metric("Visitor Trend", f"{growth_rate:.1f}%", 
                 delta_color="normal" if growth_rate >= 0 else "inverse")

def show_traffic_distribution(daily_traffic):
    """Show traffic distribution across stores"""
    # Aggregate by store
    store_traffic = daily_traffic.groupby('store')['total_visitors'].sum().reset_index()
    total = store_traffic['total_visitors'].sum()
    store_traffic['percentage'] = store_traffic['total_visitors'] / total * 100
    
    # Sort by traffic
    store_traffic = store_traffic.sort_values('total_visitors', ascending=False)
    
    # Create pie chart
    fig = px.pie(
        store_traffic,
        names='store',
        values='total_visitors',
        labels={'store': 'Store', 'total_visitors': 'Total Visitors'},
        hole=0.4
    )
    
    fig.update_layout(
        height=250,
        margin=dict(l=10, r=10, t=10, b=10),
        legend=dict(orientation="h", yanchor="bottom", y=0, xanchor="center", x=0.5)
    )
    
    st.plotly_chart(fig, use_container_width=True)

def show_visitor_trends(daily_traffic):
    """Display visitor traffic trends over time"""
    # Aggregate by date across all stores
    daily_visitors = daily_traffic.groupby('date')['total_visitors'].sum().reset_index()
    
    # Create line chart
    fig = px.line(
        daily_visitors,
        x='date',
        y='total_visitors',
        labels={'date': 'Date', 'total_visitors': 'Total Visitors'},
        height=350
    )
    
    # Add trend line
    x = np.array(range(len(daily_visitors)))
    y = daily_visitors['total_visitors'].values
    
    if len(x) > 1:
        z = np.polyfit(x, y, 1)
        p = np.poly1d(z)
        
        fig.add_trace(go.Scatter(
            x=daily_visitors['date'],
            y=p(x),
            mode='lines',
            name='Trend',
            line=dict(color='red', dash='dash')
        ))
    
    fig.update_layout(
        margin=dict(l=0, r=0, t=10, b=0),
        xaxis_title="",
        yaxis_title="Visitor Count"
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Day of week analysis
    st.subheader("Day of Week Analysis")
    
    # Add day of week
    daily_traffic['day_of_week'] = daily_traffic['date'].dt.day_name()
    
    # Order days properly
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    
    # Aggregate by day of week
    day_traffic = daily_traffic.groupby('day_of_week')['total_visitors'].mean().reindex(day_order).reset_index()
    
    # Create bar chart
    fig = px.bar(
        day_traffic,
        x='day_of_week',
        y='total_visitors',
        labels={'day_of_week': 'Day of Week', 'total_visitors': 'Average Visitors'},
        color='total_visitors',
        color_continuous_scale='Blues',
        height=300
    )
    
    fig.update_layout(
        margin=dict(l=0, r=0, t=10, b=0),
        coloraxis_showscale=False,
        xaxis_title=""
    )
    
    st.plotly_chart(fig, use_container_width=True)

def show_store_comparison(daily_traffic):
    """Compare traffic across stores"""
    # Aggregate by store
    store_summary = daily_traffic.groupby('store').agg(
        total_visitors=('total_visitors', 'sum'),
        avg_daily_visitors=('total_visitors', 'mean'),
        max_visitors=('total_visitors', 'max')
    ).reset_index()
    
    # Sort by total visitors
    store_summary = store_summary.sort_values('total_visitors', ascending=True)
    
    # Create horizontal bar chart
    fig = px.bar(
        store_summary,
        x='avg_daily_visitors',
        y='store',
        orientation='h',
        labels={'avg_daily_visitors': 'Average Daily Visitors', 'store': 'Store'},
        color='avg_daily_visitors',
        color_continuous_scale='Blues',
        height=300
    )
    
    fig.update_layout(
        margin=dict(l=0, r=0, t=10, b=0),
        coloraxis_showscale=False
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Display detailed stats
    with st.expander("View Detailed Traffic Statistics"):
        # Format for display
        display_data = store_summary.copy()
        display_data['total_visitors'] = display_data['total_visitors'].apply(lambda x: f"{int(x):,}")
        display_data['avg_daily_visitors'] = display_data['avg_daily_visitors'].apply(lambda x: f"{int(x):,}")
        display_data['max_visitors'] = display_data['max_visitors'].apply(lambda x: f"{int(x):,}")
        
        display_data.columns = ['Store', 'Total Visitors', 'Avg. Daily Visitors', 'Max Daily Visitors']
        
        st.dataframe(display_data, use_container_width=True)

def show_heatmap_analysis(traffic_patterns):
    """Display heatmap analysis of traffic patterns by time and day"""
    # Get day order for proper sorting
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    
    # Create pivot table for heatmap
    pivot_data = traffic_patterns.pivot_table(
        index='day_of_week', 
        columns='hour', 
        values='visitor_count',
        aggfunc='mean'
    ).reindex(day_order)
    
    # Generate heatmap
    fig = px.imshow(
        pivot_data,
        labels=dict(x="Hour of Day", y="Day of Week", color="Visitor Count"),
        x=list(range(24)),
        y=day_order,
        aspect="auto",
        color_continuous_scale='Blues'
    )
    
    fig.update_layout(
        height=400,
        margin=dict(l=10, r=10, t=10, b=10),
        coloraxis_colorbar=dict(title="Count")
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Add insights
    st.info("📊 **Insights**: The heatmap shows when your stores are busiest throughout the week. Darker blues indicate higher visitor counts.")

    # Store selector for individual store analysis
    if len(st.session_state.selected_stores) > 1:
        selected_store = st.selectbox(
            "Select a store for individual analysis:",
            st.session_state.selected_stores
        )
    
        # Filter for selected store
        store_patterns = traffic_patterns[traffic_patterns['store'] == selected_store]
        
        # Create pivot table for store-specific heatmap
        store_pivot = store_patterns.pivot_table(
            index='day_of_week', 
            columns='hour', 
            values='visitor_count',
            aggfunc='mean'
        ).reindex(day_order)
        
        st.subheader(f"Traffic Patterns for {selected_store}")
        
        # Generate store-specific heatmap
        fig = px.imshow(
            store_pivot,
            labels=dict(x="Hour of Day", y="Day of Week", color="Visitor Count"),
            x=list(range(24)),
            y=day_order,
            aspect="auto",
            color_continuous_scale='Blues'
        )
        
        fig.update_layout(
            height=400,
            margin=dict(l=10, r=10, t=10, b=10),
            coloraxis_colorbar=dict(title="Count")
        )
        
        st.plotly_chart(fig, use_container_width=True)

def show_combined_analysis():
    """Show combined analysis of traffic patterns and theft incidents"""
    st.markdown("### Traffic and Theft Correlation Analysis")
    
    if 'theft_data' not in st.session_state:
        st.warning("Theft data is not available for comparison.")
        return
    
    # Get filtered data
    theft_data = st.session_state.theft_data.copy()
    traffic_patterns = st.session_state.traffic_patterns.copy()
    
    # Filter by selected stores
    if st.session_state.selected_stores:
        theft_data = theft_data[theft_data['store'].isin(st.session_state.selected_stores)]
        traffic_patterns = traffic_patterns[traffic_patterns['store'].isin(st.session_state.selected_stores)]
    
    if theft_data.empty or traffic_patterns.empty:
        st.warning("Insufficient data for correlation analysis.")
        return
    
    # Prepare theft data for heatmap
    theft_data['hour'] = theft_data['timestamp'].dt.hour
    theft_data['day_of_week'] = theft_data['timestamp'].dt.day_name()
    
    # Aggregate theft data by day and hour
    theft_heatmap = theft_data.groupby(['day_of_week', 'hour']).size().reset_index(name='incidents')
    
    # Day order for proper sorting
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    
    # Create pivot tables for both heatmaps
    theft_pivot = theft_heatmap.pivot_table(
        index='day_of_week', 
        columns='hour', 
        values='incidents',
        aggfunc='sum'
    ).reindex(day_order).fillna(0)
    
    traffic_pivot = traffic_patterns.pivot_table(
        index='day_of_week', 
        columns='hour', 
        values='visitor_count',
        aggfunc='mean'
    ).reindex(day_order)
    
    # Create tabs for different views
    tab1, tab2 = st.tabs(["Heatmap Comparison", "Correlation Analysis"])
    
    with tab1:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Traffic Pattern")
            
            # Traffic heatmap
            fig = px.imshow(
                traffic_pivot,
                labels=dict(x="Hour", y="Day", color="Visitors"),
                x=list(range(24)),
                y=day_order,
                aspect="auto",
                color_continuous_scale='Blues'
            )
            
            fig.update_layout(
                height=350,
                margin=dict(l=10, r=10, t=10, b=10),
                coloraxis_colorbar=dict(title="Visitors")
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("#### Theft Pattern")
            
            # Theft heatmap
            fig = px.imshow(
                theft_pivot,
                labels=dict(x="Hour", y="Day", color="Incidents"),
                x=list(range(24)),
                y=day_order,
                aspect="auto",
                color_continuous_scale='Reds'
            )
            
            fig.update_layout(
                height=350,
                margin=dict(l=10, r=10, t=10, b=10),
                coloraxis_colorbar=dict(title="Incidents")
            )
            
            st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        st.markdown("#### Traffic vs. Theft Correlation")
        
        # Prepare data for correlation analysis
        traffic_flat = traffic_pivot.stack().reset_index()
        traffic_flat.columns = ['day_of_week', 'hour', 'visitors']
        
        theft_flat = theft_pivot.stack().reset_index()
        theft_flat.columns = ['day_of_week', 'hour', 'thefts']
        
        # Merge data
        correlation_data = pd.merge(
            traffic_flat, 
            theft_flat, 
            on=['day_of_week', 'hour'],
            how='outer'
        ).fillna(0)
        
        # Create scatter plot
        fig = px.scatter(
            correlation_data,
            x='visitors',
            y='thefts',
            labels={'visitors': 'Average Visitor Count', 'thefts': 'Theft Incidents'},
            hover_data=['day_of_week', 'hour'],
            height=400,
            trendline='ols'
        )
        
        fig.update_layout(
            margin=dict(l=10, r=10, t=10, b=10)
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Calculate correlation
        correlation = correlation_data['visitors'].corr(correlation_data['thefts'])
        
        # Display correlation insight
        if correlation > 0.3:
            st.warning(f"📈 There appears to be a positive correlation ({correlation:.2f}) between visitor traffic and theft incidents. Higher traffic periods may need additional security measures.")
        elif correlation < -0.3:
            st.info(f"📉 There appears to be a negative correlation ({correlation:.2f}) between visitor traffic and theft incidents. Theft tends to occur during lower traffic periods.")
        else:
            st.success(f"🔄 There is minimal correlation ({correlation:.2f}) between visitor traffic and theft incidents.")
