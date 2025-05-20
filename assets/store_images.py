"""
Store images display component
"""

import streamlit as st

def show_store_images():
    """Display store images in a gallery format"""
    st.subheader("Store Location Images")
    
    # Using more reliable image placeholder URLs
    store_images = [
        "https://via.placeholder.com/400x300/4285F4/FFFFFF?text=Downtown+Mart",
        "https://via.placeholder.com/400x300/DB4437/FFFFFF?text=Riverside+Convenience",
        "https://via.placeholder.com/400x300/F4B400/FFFFFF?text=Oakwood+Express",
        "https://via.placeholder.com/400x300/0F9D58/FFFFFF?text=Sunset+Shop+%26+Go"
    ]
    
    # Store names from session state
    store_names = st.session_state.get('selected_stores', [])
    if not store_names:
        # Fallback if no stores are selected
        store_names = ["Downtown Mart", "Riverside Convenience", "Oakwood Express", "Sunset Shop & Go"]
    
    # Limit to available images
    num_images = min(len(store_images), len(store_names))
    
    # Create image gallery with store names
    cols = st.columns(num_images)
    
    for i in range(num_images):
        with cols[i]:
            st.image(store_images[i], caption=store_names[i])
            
    st.caption("Store location images for reference")
