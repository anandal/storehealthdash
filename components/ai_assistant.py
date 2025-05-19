"""
AI Assistant Module - Provides intelligent assistance through voice and chat
"""

import streamlit as st
import google.generativeai as genai
import os
import pandas as pd
import base64
import io
from datetime import datetime
import time
import plotly.express as px
import plotly.graph_objects as go

# Initialize Gemini API with API key
api_key = os.environ.get("GOOGLE_API_KEY")
if api_key:
    genai.configure(api_key=api_key)

def show_ai_assistant():
    """Display AI assistant interface with both voice and chat options"""
    st.header("AI Store Assistant")
    
    st.markdown("""
    Ask questions about your store data and get instant insights.
    The assistant can analyze trends, compare metrics, and provide
    recommendations based on your data.
    """)
    
    # Initialize conversation history in session state if not already
    if "assistant_messages" not in st.session_state:
        st.session_state.assistant_messages = []
    
    # Tab for different interaction modes
    chat_tab, voice_tab = st.tabs(["💬 Chat", "🎤 Voice"])
    
    with chat_tab:
        show_chat_interface()
    
    with voice_tab:
        show_voice_interface()

def show_chat_interface():
    """Display chat interface for text-based queries"""
    # Display conversation history
    for message in st.session_state.assistant_messages:
        if message["role"] == "user":
            st.chat_message("user").write(message["content"])
        else:
            st.chat_message("assistant").write(message["content"])
            
            # Display chart if available
            if "chart" in message and message["chart"] is not None:
                st.plotly_chart(message["chart"], use_container_width=True)
    
    # Chat input
    if prompt := st.chat_input("Ask about your store data..."):
        # Add user message to history
        st.session_state.assistant_messages.append({"role": "user", "content": prompt})
        
        # Display user message
        st.chat_message("user").write(prompt)
        
        # Get AI response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response, chart = get_ai_response(prompt)
                
                # Display text response
                st.write(response)
                
                # Display chart if available
                if chart is not None:
                    st.plotly_chart(chart, use_container_width=True)
                
        # Add assistant message to history
        st.session_state.assistant_messages.append({
            "role": "assistant", 
            "content": response,
            "chart": chart
        })

def show_voice_interface():
    """Display voice interface for spoken queries"""
    st.markdown("### Voice Assistant")
    
    # Record audio from microphone
    audio_bytes = audio_recorder()
    
    if audio_bytes:
        # Display audio playback
        st.audio(audio_bytes, format="audio/wav")
        
        # Process voice input (simulate for now)
        with st.spinner("Processing voice..."):
            time.sleep(1)  # Simulate processing time
            prompt = simulate_voice_transcription()
            
            st.success(f"Transcribed: {prompt}")
            
            # Process the query
            if prompt:
                # Add user message to history
                st.session_state.assistant_messages.append({"role": "user", "content": prompt})
                
                # Get AI response
                with st.spinner("Generating response..."):
                    response, chart = get_ai_response(prompt)
                    
                    # Display text response
                    st.markdown(f"**Assistant:** {response}")
                    
                    # Display chart if available
                    if chart is not None:
                        st.plotly_chart(chart, use_container_width=True)
                    
                # Add assistant message to history
                st.session_state.assistant_messages.append({
                    "role": "assistant", 
                    "content": response,
                    "chart": chart
                })

def audio_recorder():
    """Simulate audio recording functionality"""
    if st.button("🎤 Click to Record"):
        with st.spinner("Recording... (speak clearly)"):
            # Simulate recording for 3 seconds
            time.sleep(3)
        st.success("Recording complete!")
        
        # Return simulated audio bytes (empty in this case)
        return b"simulated audio data"
    return None

def simulate_voice_transcription():
    """Simulate voice transcription - returns a plausible query"""
    sample_queries = [
        "Show me theft incidents for Downtown Mart in the past week",
        "Which store has the highest rewards program engagement?",
        "Compare traffic patterns between Riverside and Oakwood stores",
        "What are the peak hours for mobile phone usage at Sunset Shop?",
        "Show me the correlation between traffic and theft incidents"
    ]
    return sample_queries[int(time.time()) % len(sample_queries)]

def get_ai_response(prompt):
    """Get response from Gemini AI model and generate visual if needed"""
    try:
        # Prepare context from session state
        context = prepare_context_from_state()
        
        # Determine if the query might need a visualization
        needs_visualization = any(keyword in prompt.lower() for keyword in 
                                 ["show", "graph", "chart", "plot", "visualize", "compare", "trend"])
        
        # Modify prompt to include context
        enhanced_prompt = f"""As an AI assistant for a convenience store dashboard, please help with the following query:
        
{prompt}

Here's some context about the stores and data:
{context}

Reply in a helpful, concise manner focusing on insights rather than raw numbers.
"""

        # Add visualization instructions if needed
        if needs_visualization:
            enhanced_prompt += "\nInclude a JSON description of a visualization that would help answer this query. Format: <VISUALIZATION>{{json}}</VISUALIZATION>"
        
        # Get response from Gemini
        model = genai.GenerativeModel(model_name='gemini-1.5-pro')
        response = model.generate_content(enhanced_prompt)
        response_text = response.text
        
        # Check for visualization JSON
        chart = None
        if "<VISUALIZATION>" in response_text and "</VISUALIZATION>" in response_text:
            # Extract visualization JSON
            viz_start = response_text.find("<VISUALIZATION>") + len("<VISUALIZATION>")
            viz_end = response_text.find("</VISUALIZATION>")
            viz_json = response_text[viz_start:viz_end].strip()
            
            # Remove the visualization data from response text
            response_text = response_text.replace(response_text[viz_start-len("<VISUALIZATION>"):viz_end+len("</VISUALIZATION>")], "")
            
            # Generate chart based on the type
            chart = generate_chart_from_description(viz_json)
        
        return response_text, chart
    
    except Exception as e:
        st.error(f"Error generating AI response: {str(e)}")
        fallback_response = (
            "I'm sorry, I encountered an issue while processing your request. "
            "This could be due to API limits or connectivity issues. "
            "Could you try again with a more specific question about your store data?"
        )
        return fallback_response, None

def generate_chart_from_description(viz_json):
    """Generate a Plotly chart based on visualization description"""
    try:
        # For this demo, we'll create sample charts based on the type of visualization needed
        # In a full implementation, this would parse the JSON and create the exact chart
        
        # Sample data for visualizations
        dates = pd.date_range(start='2025-04-19', end='2025-05-19')
        stores = ["Downtown Mart", "Riverside Convenience", "Oakwood Express", "Sunset Shop & Go"]
        
        # Create different chart types based on what might be in the query
        if "bar" in viz_json.lower():
            # Bar chart of sample store metrics
            data = {
                'Store': stores,
                'Value': [85, 72, 63, 79]
            }
            df = pd.DataFrame(data)
            fig = px.bar(df, x='Store', y='Value', title="Store Comparison")
            return fig
            
        elif "line" in viz_json.lower() or "trend" in viz_json.lower():
            # Line chart showing trend over time
            data = {
                'Date': dates,
                'Value': [50 + i*0.5 + 5*np.sin(i/3) for i in range(len(dates))]
            }
            df = pd.DataFrame(data)
            fig = px.line(df, x='Date', y='Value', title="Trend Analysis")
            return fig
            
        elif "pie" in viz_json.lower():
            # Pie chart of distribution
            data = {
                'Category': ["Category A", "Category B", "Category C", "Category D"],
                'Value': [35, 25, 20, 20]
            }
            df = pd.DataFrame(data)
            fig = px.pie(df, names='Category', values='Value', title="Distribution Analysis")
            return fig
            
        elif "scatter" in viz_json.lower() or "correlation" in viz_json.lower():
            # Scatter plot showing correlation
            x_values = np.random.normal(50, 15, 50)
            y_values = x_values * 0.8 + np.random.normal(0, 10, 50)
            data = {
                'X': x_values,
                'Y': y_values
            }
            df = pd.DataFrame(data)
            fig = px.scatter(df, x='X', y='Y', trendline="ols", 
                           title="Correlation Analysis")
            return fig
            
        elif "heatmap" in viz_json.lower():
            # Heatmap of patterns
            days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
            hours = list(range(24))
            
            # Create a random heatmap matrix
            z = np.random.randint(5, 30, size=(len(days), len(hours)))
            
            fig = go.Figure(data=go.Heatmap(
                z=z,
                x=hours,
                y=days,
                colorscale='Blues'
            ))
            
            fig.update_layout(
                title='Pattern Analysis Heatmap',
                xaxis_title='Hour of Day',
                yaxis_title='Day of Week',
            )
            return fig
        
        # Fallback to a simple bar chart if no specific type is detected
        data = {
            'Category': ['A', 'B', 'C', 'D', 'E'],
            'Value': [23, 45, 56, 78, 42]
        }
        df = pd.DataFrame(data)
        fig = px.bar(df, x='Category', y='Value', title="Data Visualization")
        return fig
        
    except Exception as e:
        st.error(f"Error generating chart: {str(e)}")
        return None

def prepare_context_from_state():
    """Prepare context information from session state data"""
    context = []
    
    # Add store information
    if 'store_info' in st.session_state:
        stores = st.session_state.store_info['store_name'].tolist()
        context.append(f"Stores: {', '.join(stores)}")
    else:
        # Fallback store information
        context.append("Stores: Downtown Mart, Riverside Convenience, Oakwood Express, Sunset Shop & Go, Hillside Corner Store")
    
    # Add selected time period
    if 'date_range' in st.session_state:
        start_date, end_date = st.session_state.date_range
        context.append(f"Date Range: {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}")
    
    # Add information about available data
    available_data = []
    if 'theft_data' in st.session_state:
        available_data.append("theft incidents")
    if 'rewards_data' in st.session_state:
        available_data.append("rewards program metrics")
    if 'daily_traffic' in st.session_state:
        available_data.append("store traffic patterns")
    if 'shift_usage_data' in st.session_state:
        available_data.append("employee mobile usage statistics")
    if 'business_health' in st.session_state:
        available_data.append("overall business health indicators")
    
    if available_data:
        context.append(f"Available Data: {', '.join(available_data)}")
    
    # Return formatted context
    return "\n".join(context)

# Add numpy import needed for sample data generation
import numpy as np