"""
SceneIQ Premium Chart Styles
This module provides state-of-the-art visualization styles for the dashboard charts
"""

import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import colorsys

# SceneIQ brand color palette
SCENEIQ_COLORS = {
    'primary': '#4285F4',    # Google Blue
    'secondary': '#DB4437',  # Google Red
    'tertiary': '#F4B400',   # Google Yellow
    'success': '#0F9D58',    # Google Green
    'info': '#9334E6',       # Purple
    'warning': '#FF6D01',    # Orange
    'neutral': '#202124',    # Dark Gray
    'light': '#F2F2F2',      # Light Gray
}

# Extended color palette for multiple series
EXTENDED_PALETTE = [
    '#4285F4', '#DB4437', '#F4B400', '#0F9D58', '#9334E6', 
    '#FF6D01', '#1A73E8', '#EA4335', '#FBBC04', '#34A853', 
    '#7248B9', '#FF5722', '#2962FF', '#D50000', '#FFD600'
]

# Modern chart templates
CHART_TEMPLATES = {
    'light': {
        'bgcolor': '#FFFFFF',
        'gridcolor': '#F0F0F0',
        'linecolor': '#DDDDDD',
        'zerolinecolor': '#CCCCCC',
        'paper_bgcolor': 'rgba(0,0,0,0)',
        'plot_bgcolor': 'rgba(0,0,0,0)',
        'font': {
            'family': 'Roboto, Arial, sans-serif',
            'color': '#202124'
        }
    },
    'dark': {
        'bgcolor': '#202124',
        'gridcolor': '#3C4043',
        'linecolor': '#5F6368',
        'zerolinecolor': '#3C4043',
        'paper_bgcolor': 'rgba(0,0,0,0)',
        'plot_bgcolor': 'rgba(0,0,0,0)',
        'font': {
            'family': 'Roboto, Arial, sans-serif',
            'color': '#E8EAED'
        }
    }
}

def generate_gradient_colors(base_color, num_colors):
    """Generate a gradient of colors based on a base color"""
    # Convert hex to HSV
    r, g, b = int(base_color[1:3], 16)/255, int(base_color[3:5], 16)/255, int(base_color[5:7], 16)/255
    h, s, v = colorsys.rgb_to_hsv(r, g, b)
    
    colors = []
    for i in range(num_colors):
        # Vary saturation and value
        new_s = max(0.2, s - (i * 0.5 / num_colors))
        new_v = min(0.9, v + (i * 0.5 / num_colors))
        
        # Convert back to RGB
        r, g, b = colorsys.hsv_to_rgb(h, new_s, new_v)
        r, g, b = int(r*255), int(g*255), int(b*255)
        
        # Convert to hex
        colors.append(f'#{r:02x}{g:02x}{b:02x}')
    
    return colors

def apply_premium_styling(fig, title=None, template='light', gradient=False, height=None):
    """Apply premium styling to a plotly figure"""
    
    # Set base template
    tpl = CHART_TEMPLATES[template]
    
    # Update layout with premium styling
    fig.update_layout(
        title=title,
        font=tpl['font'],
        paper_bgcolor=tpl['paper_bgcolor'],
        plot_bgcolor=tpl['plot_bgcolor'],
        margin=dict(l=20, r=20, t=40, b=20),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="center",
            x=0.5,
            bgcolor='rgba(255,255,255,0.8)' if template == 'light' else 'rgba(32,33,36,0.8)',
            bordercolor='rgba(0,0,0,0)'
        ),
        height=height
    )
    
    # Add drop shadow effect
    fig.update_layout(
        shapes=[
            dict(
                type="rect",
                xref="paper", yref="paper",
                x0=0, y0=0, x1=1, y1=1,
                line=dict(width=0),
                fillcolor="rgba(0,0,0,0)",
                layer="below"
            )
        ]
    )
    
    # Update axes
    fig.update_xaxes(
        showgrid=True,
        gridwidth=1,
        gridcolor=tpl['gridcolor'],
        zeroline=True,
        zerolinewidth=1,
        zerolinecolor=tpl['zerolinecolor'],
        showline=True,
        linewidth=1,
        linecolor=tpl['linecolor']
    )
    
    fig.update_yaxes(
        showgrid=True,
        gridwidth=1,
        gridcolor=tpl['gridcolor'],
        zeroline=True,
        zerolinewidth=1,
        zerolinecolor=tpl['zerolinecolor'],
        showline=True,
        linewidth=1,
        linecolor=tpl['linecolor']
    )
    
    # Apply gradient colors if requested
    if gradient:
        # Get first non-black color in the figure
        first_color = None
        for trace in fig.data:
            if hasattr(trace, 'marker') and hasattr(trace.marker, 'color'):
                if trace.marker.color and trace.marker.color != '#000000':
                    first_color = trace.marker.color
                    break
            elif hasattr(trace, 'line') and hasattr(trace.line, 'color'):
                if trace.line.color and trace.line.color != '#000000':
                    first_color = trace.line.color
                    break
        
        if first_color:
            gradient_colors = generate_gradient_colors(first_color, len(fig.data))
            for i, trace in enumerate(fig.data):
                if hasattr(trace, 'marker'):
                    trace.marker.color = gradient_colors[i % len(gradient_colors)]
                if hasattr(trace, 'line'):
                    trace.line.color = gradient_colors[i % len(gradient_colors)]
    
    return fig

def create_bar_chart(df, x, y, title=None, color=None, barmode='group', height=400):
    """Create a premium styled bar chart"""
    if color:
        fig = px.bar(df, x=x, y=y, color=color, barmode=barmode, 
                     color_discrete_sequence=EXTENDED_PALETTE)
    else:
        fig = px.bar(df, x=x, y=y, barmode=barmode, 
                     color_discrete_sequence=[SCENEIQ_COLORS['primary']])
    
    # Apply premium styling
    return apply_premium_styling(fig, title=title, height=height)

def create_line_chart(df, x, y, title=None, color=None, height=400):
    """Create a premium styled line chart"""
    if color:
        fig = px.line(df, x=x, y=y, color=color, 
                      color_discrete_sequence=EXTENDED_PALETTE)
    else:
        fig = px.line(df, x=x, y=y, 
                      color_discrete_sequence=[SCENEIQ_COLORS['primary']])
    
    # Add markers and make lines smoother
    for trace in fig.data:
        trace.mode = 'lines+markers'
        trace.line.shape = 'spline'
        trace.line.smoothing = 1.3
        trace.marker.size = 8
    
    # Apply premium styling
    return apply_premium_styling(fig, title=title, height=height)

def create_area_chart(df, x, y, title=None, color=None, height=400):
    """Create a premium styled area chart"""
    if color:
        fig = px.area(df, x=x, y=y, color=color, 
                      color_discrete_sequence=EXTENDED_PALETTE)
    else:
        fig = px.area(df, x=x, y=y, 
                      color_discrete_sequence=[SCENEIQ_COLORS['primary']])
    
    # Make lines smoother
    for trace in fig.data:
        trace.line.shape = 'spline'
        trace.line.smoothing = 1.3
    
    # Apply premium styling
    return apply_premium_styling(fig, title=title, height=height)

def create_pie_chart(df, names, values, title=None, height=400):
    """Create a premium styled pie chart"""
    fig = px.pie(df, names=names, values=values,
                 color_discrete_sequence=EXTENDED_PALETTE)
    
    # Add styling specific to pie charts
    fig.update_traces(
        textposition='inside',
        textinfo='percent+label',
        hole=0.4,
        marker=dict(line=dict(color='#FFFFFF', width=2))
    )
    
    # Apply premium styling
    return apply_premium_styling(fig, title=title, height=height)

def create_donut_chart(df, names, values, title=None, height=400):
    """Create a premium styled donut chart"""
    fig = px.pie(df, names=names, values=values,
                 color_discrete_sequence=EXTENDED_PALETTE)
    
    # Add styling specific to donut charts
    fig.update_traces(
        textposition='inside',
        textinfo='percent+label',
        hole=0.65,
        marker=dict(line=dict(color='#FFFFFF', width=2))
    )
    
    # Apply premium styling
    return apply_premium_styling(fig, title=title, height=height)

def create_scatter_chart(df, x, y, title=None, color=None, size=None, height=400):
    """Create a premium styled scatter chart"""
    fig = px.scatter(df, x=x, y=y, color=color, size=size,
                    color_discrete_sequence=EXTENDED_PALETTE)
    
    # Add styling specific to scatter plots
    fig.update_traces(
        marker=dict(
            line=dict(width=1, color='white'),
            opacity=0.8
        )
    )
    
    # Apply premium styling
    return apply_premium_styling(fig, title=title, height=height)

def create_heatmap(data, x=None, y=None, title=None, height=500):
    """Create a premium styled heatmap"""
    fig = go.Figure(data=go.Heatmap(
        z=data,
        x=x,
        y=y,
        colorscale='Blues',
        hovertemplate='%{y}: %{x}<br>Value: %{z}<extra></extra>'
    ))
    
    # Apply premium styling with heatmap specifics
    fig = apply_premium_styling(fig, title=title, height=height)
    
    # Additional heatmap styling
    fig.update_layout(
        margin=dict(l=40, r=30, t=50, b=40),
    )
    
    return fig

def create_gauge_chart(value, title=None, min_val=0, max_val=100, threshold=None, height=300):
    """Create a premium styled gauge chart"""
    # Calculate color based on threshold
    if threshold:
        if value <= threshold[0]:
            color = SCENEIQ_COLORS['secondary']  # Red for below first threshold
        elif value <= threshold[1]:
            color = SCENEIQ_COLORS['tertiary']   # Yellow for between thresholds
        else:
            color = SCENEIQ_COLORS['success']    # Green for above second threshold
    else:
        color = SCENEIQ_COLORS['primary']  # Default color
    
    # Create the gauge
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        domain={'x': [0, 1], 'y': [0, 1]},
        gauge={
            'axis': {'range': [min_val, max_val], 'tickwidth': 1, 'tickcolor': "#FFFFFF"},
            'bar': {'color': color},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "lightgray",
            'steps': [
                {'range': [min_val, max_val], 'color': '#F5F5F5'}
            ],
            'threshold': {
                'line': {'color': "black", 'width': 4},
                'thickness': 0.75,
                'value': value
            }
        },
        number={'suffix': "%", 'font': {'size': 26}}
    ))
    
    # Apply premium styling
    return apply_premium_styling(fig, title=title, height=height)

def create_radar_chart(categories, values, title=None, height=400):
    """Create a premium styled radar chart"""
    # Close the polygon by appending first value
    values_closed = values + [values[0]]
    categories_closed = categories + [categories[0]]
    
    fig = go.Figure()
    
    # Add radar chart
    fig.add_trace(go.Scatterpolar(
        r=values_closed,
        theta=categories_closed,
        fill='toself',
        fillcolor=f'rgba({int(SCENEIQ_COLORS["primary"][1:3], 16)}, {int(SCENEIQ_COLORS["primary"][3:5], 16)}, {int(SCENEIQ_COLORS["primary"][5:7], 16)}, 0.2)',
        line=dict(color=SCENEIQ_COLORS["primary"], width=2)
    ))
    
    # Set radar chart layout
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, max(values) * 1.1]
            )
        ),
        showlegend=False
    )
    
    # Apply premium styling
    return apply_premium_styling(fig, title=title, height=height)

def create_bubble_chart(df, x, y, size, title=None, color=None, height=450):
    """Create a premium styled bubble chart"""
    fig = px.scatter(df, x=x, y=y, size=size, color=color,
                    color_discrete_sequence=EXTENDED_PALETTE,
                    size_max=50, opacity=0.7)
    
    # Apply premium styling
    return apply_premium_styling(fig, title=title, height=height)

def create_box_plot(df, x, y, title=None, color=None, height=400):
    """Create a premium styled box plot"""
    fig = px.box(df, x=x, y=y, color=color,
                color_discrete_sequence=EXTENDED_PALETTE)
    
    # Apply styling specific to box plots
    fig.update_traces(
        boxmean=True,  # Add mean markers
        marker=dict(
            opacity=0.7,
            size=6,
            line=dict(width=1, color='white')
        )
    )
    
    # Apply premium styling
    return apply_premium_styling(fig, title=title, height=height)

def create_violin_plot(df, x, y, title=None, color=None, height=400):
    """Create a premium styled violin plot"""
    fig = px.violin(df, x=x, y=y, color=color,
                   color_discrete_sequence=EXTENDED_PALETTE,
                   box=True, points="all")
    
    # Apply styling specific to violin plots
    fig.update_traces(
        points='all',
        jitter=0.3,
        pointpos=-0.9,
        marker=dict(
            opacity=0.7,
            size=6,
            line=dict(width=1, color='white')
        )
    )
    
    # Apply premium styling
    return apply_premium_styling(fig, title=title, height=height)

def create_waterfall_chart(names, values, title=None, height=400):
    """Create a premium styled waterfall chart"""
    # Create lists for increasing, decreasing, and total values
    measure = []
    for i in range(len(values)):
        if i == 0:
            measure.append('absolute')  # First value is absolute
        elif i == len(values) - 1:
            measure.append('total')     # Last value is total
        elif values[i] >= 0:
            measure.append('relative')  # Increasing value
        else:
            measure.append('relative')  # Decreasing value
    
    # Set colors based on value
    colors = []
    for i in range(len(values)):
        if i == 0:
            colors.append(SCENEIQ_COLORS['primary'])  # First value
        elif i == len(values) - 1:
            colors.append(SCENEIQ_COLORS['neutral'])  # Total
        elif values[i] >= 0:
            colors.append(SCENEIQ_COLORS['success'])  # Positive value
        else:
            colors.append(SCENEIQ_COLORS['secondary'])  # Negative value
    
    fig = go.Figure(go.Waterfall(
        name="Waterfall",
        orientation="v",
        measure=measure,
        x=names,
        y=values,
        text=values,
        textposition="outside",
        connector={"line": {"color": "rgb(63, 63, 63)"}},
        marker={"color": colors}
    ))
    
    # Apply premium styling
    return apply_premium_styling(fig, title=title, height=height)