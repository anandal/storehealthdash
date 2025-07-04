"""
Employee Productivity & Compliance Module - Visualizes mobile phone usage patterns
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from components.chart_styles import (
    apply_premium_styling,
    create_bar_chart, 
    create_line_chart,
    create_pie_chart,
    create_heatmap,
    SCENEIQ_COLORS
)

def show_employee_analytics():
    """Display employee productivity and compliance dashboard"""
    st.header("SceneIQ™ Employee Productivity & Compliance")
    
    # Get filtered data based on selected stores and date range
    mobile_patterns = get_filtered_mobile_patterns()
    shift_data = get_filtered_shift_data()
    
    if mobile_patterns.empty or shift_data.empty:
        st.warning("No employee data available for the selected stores and time period.")
        return
    
    # Add privacy notice
    st.info(
        "📱 **Privacy Notice**: This data focuses on operational patterns rather than individual "
        "employee monitoring. It helps identify understaffing, policy clarity needs, and "
        "training opportunities."
    )
    
    # Dashboard layout
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Mobile Usage Overview")
        show_mobile_usage_kpis(shift_data)
    
    with col2:
        st.subheader("Usage by Shift")
        show_usage_by_shift(shift_data)
    
    # Usage trends
    st.subheader("Mobile Usage Trends")
    show_usage_trends(shift_data)
    
    # Store comparison
    st.subheader("Mobile Usage Comparison Across Stores")
    show_store_comparison(shift_data)
    
    # Heatmap analysis
    st.subheader("Mobile Usage Patterns Heatmap")
    show_heatmap_analysis(mobile_patterns)
    
    # Recommendations
    st.subheader("Recommendations & Insights")
    show_recommendations(shift_data, mobile_patterns)

def get_filtered_mobile_patterns():
    """Get mobile usage pattern data filtered by selected stores"""
    if 'mobile_usage_patterns' not in st.session_state:
        return pd.DataFrame()
    
    mobile_data = st.session_state.mobile_usage_patterns.copy()
    
    # Filter by selected stores
    if st.session_state.selected_stores:
        mobile_data = mobile_data[mobile_data['store'].isin(st.session_state.selected_stores)]
    
    return mobile_data

def get_filtered_shift_data():
    """Get shift-based mobile usage data filtered by selected stores and date range"""
    if 'shift_usage_data' not in st.session_state:
        return pd.DataFrame()
    
    shift_data = st.session_state.shift_usage_data.copy()
    
    # Filter by selected stores
    if st.session_state.selected_stores:
        shift_data = shift_data[shift_data['store'].isin(st.session_state.selected_stores)]
    
    # Filter by date range
    if st.session_state.date_range:
        start_date, end_date = st.session_state.date_range
        shift_data = shift_data[(shift_data['date'] >= pd.Timestamp(start_date)) & 
                               (shift_data['date'] <= pd.Timestamp(end_date))]
    
    return shift_data

def show_mobile_usage_kpis(shift_data):
    """Display key performance indicators for mobile phone usage"""
    # Calculate KPIs
    total_incidents = shift_data['mobile_usage_incidents'].sum()
    avg_incidents_per_day = shift_data.groupby('date')['mobile_usage_incidents'].sum().mean()
    avg_duration = shift_data['avg_duration_minutes'].mean()
    total_usage_time = shift_data['total_usage_minutes'].sum()
    
    # Display metrics
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Total Usage Incidents", f"{int(total_incidents):,}")
        st.metric("Avg. Duration", f"{avg_duration:.1f} min")
    
    with col2:
        st.metric("Daily Incidents", f"{avg_incidents_per_day:.1f}")
        st.metric("Total Usage Time", f"{int(total_usage_time):,} min")

def show_usage_by_shift(shift_data):
    """Show mobile usage breakdown by shift"""
    # Aggregate by shift
    shift_summary = shift_data.groupby('shift').agg(
        incidents=('mobile_usage_incidents', 'sum'),
        avg_duration=('avg_duration_minutes', 'mean')
    ).reset_index()
    
    # Sort by incidents descending
    shift_summary = shift_summary.sort_values('incidents', ascending=False)
    
    # Create bar chart
    fig = px.bar(
        shift_summary,
        x='shift',
        y='incidents',
        color='avg_duration',
        color_continuous_scale='Reds',
        labels={'shift': 'Shift', 'incidents': 'Total Incidents', 'avg_duration': 'Avg. Duration (min)'},
        height=250
    )
    
    fig.update_layout(
        margin=dict(l=0, r=0, t=10, b=0),
        xaxis_title="",
        yaxis_title="Incidents"
    )
    
    st.plotly_chart(fig, use_container_width=True)

def show_usage_trends(shift_data):
    """Display mobile usage trends over time"""
    # Aggregate by date across all stores
    daily_usage = shift_data.groupby('date').agg(
        incidents=('mobile_usage_incidents', 'sum'),
        avg_duration=('avg_duration_minutes', 'mean')
    ).reset_index()
    
    # Create premium styled figure with dual y-axis
    fig = go.Figure()
    
    # Add incidents line with premium styling
    fig.add_trace(go.Scatter(
        x=daily_usage['date'],
        y=daily_usage['incidents'],
        name='Total Incidents',
        line=dict(
            color=SCENEIQ_COLORS['secondary'],
            width=3,
            shape='spline',
            smoothing=1.3
        ),
        mode='lines+markers',
        marker=dict(
            size=8,
            color=SCENEIQ_COLORS['secondary'],
            line=dict(width=1, color='white')
        )
    ))
    
    # Add duration line with premium styling
    fig.add_trace(go.Scatter(
        x=daily_usage['date'],
        y=daily_usage['avg_duration'],
        name='Avg. Duration (min)',
        line=dict(
            color=SCENEIQ_COLORS['primary'],
            width=3,
            shape='spline',
            smoothing=1.3
        ),
        mode='lines+markers',
        marker=dict(
            size=8,
            color=SCENEIQ_COLORS['primary'],
            line=dict(width=1, color='white')
        ),
        yaxis='y2'
    ))
    
    # Apply premium styling
    fig = apply_premium_styling(
        fig,
        title="Mobile Usage Trends Over Time",
        height=370
    )
    
    # Add range selector for interactive time filtering
    fig.update_layout(
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=7, label="1w", step="day", stepmode="backward"),
                    dict(count=1, label="1m", step="month", stepmode="backward"),
                    dict(count=3, label="3m", step="month", stepmode="backward"),
                    dict(step="all")
                ]),
                bgcolor="#F9F9F9",
                font=dict(color="#666666"),
                borderwidth=1,
                bordercolor="#DDDDDD",
                y=-0.15,
            ),
            rangeslider=dict(visible=True, thickness=0.05),
            type="date"
        ),
        yaxis=dict(
            title="Total Incidents",
            title_font=dict(color=SCENEIQ_COLORS['secondary']),
            tickfont=dict(color=SCENEIQ_COLORS['secondary']),
            gridcolor='rgba(220, 220, 220, 0.5)'
        ),
        yaxis2=dict(
            title="Avg. Duration (min)",
            title_font=dict(color=SCENEIQ_COLORS['primary']),
            tickfont=dict(color=SCENEIQ_COLORS['primary']),
            anchor="x",
            overlaying="y",
            side="right",
            gridcolor='rgba(220, 220, 220, 0.5)'
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    # Mark weekends with different background if we have enough data
    if len(daily_usage) > 7:
        for date in daily_usage['date']:
            if pd.to_datetime(date).weekday() >= 5:  # Weekend (5=Saturday, 6=Sunday)
                fig.add_vrect(
                    x0=date, x1=date,
                    fillcolor="rgba(230, 230, 230, 0.3)",
                    layer="below", line_width=0,
                )
    
    # Add annotations for highest and lowest points
    if not daily_usage.empty and len(daily_usage) > 1:
        max_incidents = daily_usage.loc[daily_usage['incidents'].idxmax()]
        min_incidents = daily_usage.loc[daily_usage['incidents'].idxmin()]
        
        # Annotate max point
        fig.add_annotation(
            x=max_incidents['date'],
            y=max_incidents['incidents'],
            text=f"Peak: {int(max_incidents['incidents'])}",
            showarrow=True,
            arrowhead=2,
            arrowsize=1,
            arrowwidth=2,
            arrowcolor=SCENEIQ_COLORS['secondary'],
            ax=-30,
            ay=-30
        )
        
        # Annotate min point
        fig.add_annotation(
            x=min_incidents['date'],
            y=min_incidents['incidents'],
            text=f"Low: {int(min_incidents['incidents'])}",
            showarrow=True,
            arrowhead=2,
            arrowsize=1,
            arrowwidth=2,
            arrowcolor=SCENEIQ_COLORS['secondary'],
            ax=30,
            ay=-30
        )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Day of week analysis
    st.subheader("Day of Week Analysis")
    
    # Add day of week
    shift_data['day_of_week'] = shift_data['date'].dt.day_name()
    
    # Order days properly
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    
    # Aggregate by day of week
    day_usage = shift_data.groupby('day_of_week')['mobile_usage_incidents'].mean().reindex(day_order).reset_index()
    
    # Create premium styled bar chart
    fig = create_bar_chart(
        df=day_usage,
        x='day_of_week',
        y='mobile_usage_incidents',
        title="Mobile Usage by Day of Week",
        height=320
    )
    
    # Highlight weekends with different colors
    bar_colors = []
    for day in day_order:
        if day in ['Saturday', 'Sunday']:
            bar_colors.append(SCENEIQ_COLORS['secondary'])  # Weekend color
        else:
            bar_colors.append(SCENEIQ_COLORS['primary'])    # Weekday color
    
    fig.update_traces(
        marker_color=bar_colors,
        width=0.6  # Thinner bars
    )
    
    # Add value labels on top of each bar
    for i, value in enumerate(day_usage['mobile_usage_incidents']):
        fig.add_annotation(
            x=i,
            y=value + (max(day_usage['mobile_usage_incidents']) * 0.03),  # Slightly above bar
            text=f"{value:.1f}",
            showarrow=False,
            font=dict(color="#555555", size=11)
        )
    
    # Add weekend/weekday shading
    fig.add_vrect(
        x0=-0.5, x1=4.5,  # Monday-Friday
        fillcolor="rgba(240, 240, 255, 0.2)",
        layer="below", line_width=0,
        annotation_text="Weekdays",
        annotation_position="top left"
    )
    
    fig.add_vrect(
        x0=4.5, x1=6.5,  # Saturday-Sunday
        fillcolor="rgba(255, 230, 230, 0.2)",
        layer="below", line_width=0,
        annotation_text="Weekend",
        annotation_position="top right"
    )
    
    # Add insights about patterns
    weekday_avg = day_usage[day_usage['day_of_week'].isin(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'])]['mobile_usage_incidents'].mean()
    weekend_avg = day_usage[day_usage['day_of_week'].isin(['Saturday', 'Sunday'])]['mobile_usage_incidents'].mean()
    
    if weekend_avg > weekday_avg:
        st.info("📱 **Insight**: Mobile usage is higher on weekends compared to weekdays. Consider adjusting staffing or policies accordingly.")
    else:
        st.info("📱 **Insight**: Mobile usage is higher on weekdays. Focus compliance training on your busiest days.")
    
    st.plotly_chart(fig, use_container_width=True)

def show_store_comparison(shift_data):
    """Compare mobile usage across stores"""
    # Aggregate by store
    store_summary = shift_data.groupby('store').agg(
        total_incidents=('mobile_usage_incidents', 'sum'),
        avg_incidents=('mobile_usage_incidents', 'mean'),
        avg_duration=('avg_duration_minutes', 'mean'),
        total_minutes=('total_usage_minutes', 'sum')
    ).reset_index()
    
    # Sort by total incidents
    store_summary = store_summary.sort_values('total_incidents', ascending=True)
    
    # Create horizontal bar chart
    fig = px.bar(
        store_summary,
        x='avg_incidents',
        y='store',
        orientation='h',
        color='avg_duration',
        color_continuous_scale='Reds',
        labels={'avg_incidents': 'Avg. Incidents per Shift', 'store': 'Store', 'avg_duration': 'Avg. Duration (min)'},
        height=300
    )
    
    fig.update_layout(
        margin=dict(l=0, r=0, t=10, b=0)
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Display detailed stats
    with st.expander("View Detailed Usage Statistics"):
        # Format for display
        display_data = store_summary.copy()
        display_data['total_incidents'] = display_data['total_incidents'].apply(lambda x: f"{int(x):,}")
        display_data['avg_incidents'] = display_data['avg_incidents'].apply(lambda x: f"{x:.1f}")
        display_data['avg_duration'] = display_data['avg_duration'].apply(lambda x: f"{x:.1f} min")
        display_data['total_minutes'] = display_data['total_minutes'].apply(lambda x: f"{int(x):,} min")
        
        display_data.columns = ['Store', 'Total Incidents', 'Avg. Incidents per Shift', 'Avg. Duration', 'Total Usage Time']
        
        st.dataframe(display_data, use_container_width=True)

def show_heatmap_analysis(mobile_patterns):
    """Display heatmap analysis of mobile usage patterns by time and day"""
    try:
        # Get day order for proper sorting
        day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        
        # Create pivot table for heatmap
        pivot_data = mobile_patterns.pivot_table(
            index='day_of_week', 
            columns='hour', 
            values='mobile_usage_incidents',
            aggfunc='mean'
        ).reindex(day_order)
        
        # Ensure all hours are represented (0-23)
        for hour in range(24):
            if hour not in pivot_data.columns:
                pivot_data[hour] = 0
                
        # Sort columns to ensure they're in correct order
        pivot_data = pivot_data.sort_index(axis=1)
        
        # Generate heatmap
        fig = px.imshow(
            pivot_data,
            labels=dict(x="Hour of Day", y="Day of Week", color="Incidents"),
            x=list(range(24)),
            y=day_order,
            aspect="auto",
            color_continuous_scale='Reds'
        )
    except Exception as e:
        st.error(f"Error creating mobile usage heatmap: {str(e)}")
        # Create an empty figure as fallback
        fig = go.Figure()
        st.warning("Could not display mobile usage heatmap. Please check your selected stores and date range.")
    
    fig.update_layout(
        height=400,
        margin=dict(l=10, r=10, t=10, b=10),
        coloraxis_colorbar=dict(title="Count")
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Add insights
    st.info("📱 **Insights**: The heatmap shows when mobile phone usage is most frequent. Darker reds indicate higher usage.")

    # Store selector for individual store analysis
    if len(st.session_state.selected_stores) > 1:
        selected_store = st.selectbox(
            "Select a store for individual analysis:",
            st.session_state.selected_stores
        )
    
        # Filter for selected store
        store_patterns = mobile_patterns[mobile_patterns['store'] == selected_store]
        
        # Create pivot table for store-specific heatmap
        store_pivot = store_patterns.pivot_table(
            index='day_of_week', 
            columns='hour', 
            values='mobile_usage_incidents',
            aggfunc='mean'
        ).reindex(day_order)
        
        st.subheader(f"Mobile Usage Patterns for {selected_store}")
        
        # Generate store-specific heatmap
        fig = px.imshow(
            store_pivot,
            labels=dict(x="Hour of Day", y="Day of Week", color="Incidents"),
            x=list(range(24)),
            y=day_order,
            aspect="auto",
            color_continuous_scale='Reds'
        )
        
        fig.update_layout(
            height=400,
            margin=dict(l=10, r=10, t=10, b=10),
            coloraxis_colorbar=dict(title="Count")
        )
        
        st.plotly_chart(fig, use_container_width=True)

def show_recommendations(shift_data, mobile_patterns):
    """Display recommendations based on the data analysis"""
    # Calculate some insights
    store_performance = shift_data.groupby('store')['mobile_usage_incidents'].mean().sort_values()
    best_store = store_performance.index[0]
    worst_store = store_performance.index[-1]
    
    # Identify problematic shifts
    shift_performance = shift_data.groupby('shift')['mobile_usage_incidents'].mean().sort_values(ascending=False)
    problem_shift = shift_performance.index[0]
    
    # Generate recommendations
    recommendations = [
        f"🏆 **Best Practice Model**: Consider studying the operational model of **{best_store}**, which has the lowest mobile phone usage.",
        f"📉 **Focus Area**: **{worst_store}** shows the highest mobile usage and may benefit from additional training or staffing review.",
        f"⏰ **Shift Attention**: The **{problem_shift}** shift consistently shows higher mobile usage across stores, suggesting possible understaffing or policy review needs.",
        "👥 **Staff Engagement**: Consider implementing a 'phone-free incentive program' to encourage compliance during busy hours.",
        "📊 **Regular Reviews**: Schedule monthly review sessions with store managers to discuss mobile usage patterns and improvement strategies."
    ]
    
    # Display recommendations
    col1, col2 = st.columns([3, 2])
    
    with col1:
        for rec in recommendations:
            st.markdown(rec)
    
    with col2:
        # Display a quick high-level compliance score
        store_scores = shift_data.groupby('store').agg({
            'mobile_usage_incidents': 'mean',
            'avg_duration_minutes': 'mean'
        })
        
        # Normalize and invert scores (lower usage = higher compliance)
        max_incidents = store_scores['mobile_usage_incidents'].max()
        max_duration = store_scores['avg_duration_minutes'].max()
        
        if max_incidents > 0 and max_duration > 0:
            store_scores['incident_score'] = 1 - (store_scores['mobile_usage_incidents'] / max_incidents)
            store_scores['duration_score'] = 1 - (store_scores['avg_duration_minutes'] / max_duration)
            store_scores['compliance_score'] = (store_scores['incident_score'] * 0.6 + store_scores['duration_score'] * 0.4) * 100
            
            # Highlight best and worst stores
            store_scores = store_scores.sort_values('compliance_score', ascending=False)
            
            st.markdown("### Compliance Scores")
            
            for store, row in store_scores.iterrows():
                score = row['compliance_score']
                color = "green" if score >= 70 else "orange" if score >= 50 else "red"
                st.markdown(f"**{store}**: <span style='color:{color}'>{score:.1f}%</span>", unsafe_allow_html=True)
        
        # Add action items
        st.markdown("### Suggested Actions")
        st.write("1. Schedule staff training session")
        st.write("2. Review peak hour staffing levels")
        st.write("3. Update mobile usage policy")
