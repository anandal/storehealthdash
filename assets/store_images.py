"""
Store images display component
"""

import streamlit as st

def show_store_images():
    """Display store images in a gallery format"""
    st.subheader("Store Location Images")
    
    # Using stock photos
    store_images = [
        "https://pixabay.com/get/g3b121891cfec688ecfc7c61f54b9adbbef5bc8d0d8e7553bfef5dc534d6f97931bf829bfe01e1fe3024d80185babdec345e1130a3c101cc0f2fc0ca259671ed4_1280.jpg",
        "https://pixabay.com/get/g90723936824fdf1103ce3ea32b8217dce9cde401d15e668dcc8235d9c1977cf22b4a7cb076b57b53ee4e81f279567477c205255b8481853c53e4f944ca773315_1280.jpg",
        "https://pixabay.com/get/g6eec510558dfa25600ff6660297034967d54f1947969e767b9be106b148e0400f769740e189a96ced3f80e9d3d6e9db1792b2425682f4f180c2103d453ce3d38_1280.jpg",
        "https://pixabay.com/get/g4276a293fd4cecc93e9c2a24fc7cca4b10c18b1bb8306de938969a706b37af16bc8a69186560e61652b23bbee6f1ca46e40362a68bcca96809f5403540809c49_1280.jpg"
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
