"""
Main Streamlit application for Criminal Face Database
"""
import streamlit as st
import os
from pathlib import Path
from datetime import datetime
from PIL import Image
import sys

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from app.utils import load_css, resize_image, format_confidence
from app.config import STATIC_DIR, IMAGES_DIR, EMBEDDINGS_DIR, DB_PATH, IMAGE_MAX_SIZE
from database.db_connector import (
    add_criminal, get_all_criminals, search_criminals, 
    get_criminal_by_id, add_match_record
)

# Page configuration
st.set_page_config(
    page_title="Criminal Face Database",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load custom CSS
css_file = STATIC_DIR / "style.css"
if css_file.exists():
    load_css(str(css_file))

# Title
st.title("🔍 Criminal Face Database System")
st.markdown("---")

# Sidebar Navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Select Page",
    ["🏠 Home", "➕ Add Criminal", "🔎 Search & Match", "📋 View Database"]
)

# HOME PAGE
if page == "🏠 Home":
    st.header("Welcome to the Criminal Face Database")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Records", len(get_all_criminals()))
    
    with col2:
        st.metric("Database Status", "✅ Active")
    
    with col3:
        st.metric("System", "Online")
    
    st.markdown("---")
    st.subheader("System Features")
    
    st.markdown("""
    - **Add Criminal Records**: Store criminal information with photos and biometric data
    - **Face Recognition**: Match faces against the criminal database
    - **Search Functionality**: Search by name or case number
    - **Database Management**: View and manage all criminal records
    """)
    
    st.info("Select an option from the sidebar to get started.")

# ADD CRIMINAL PAGE
elif page == "➕ Add Criminal":
    st.header("Add New Criminal Record")
    
    with st.form("add_criminal_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("Full Name *", placeholder="Enter full name")
            case_number = st.text_input("Case Number *", placeholder="e.g., CR-2024-001")
            age = st.number_input("Age", min_value=0, max_value=120, value=0)
            gender = st.selectbox("Gender", ["", "Male", "Female", "Other"])
            crime_type = st.text_input("Crime Type", placeholder="e.g., Theft, Assault")
        
        with col2:
            arrest_date = st.date_input("Arrest Date")
            location = st.text_input("Location", placeholder="City, State")
            description = st.text_area("Description", placeholder="Additional details...")
            image_file = st.file_uploader("Upload Photo *", type=["jpg", "jpeg", "png"])
        
        submitted = st.form_submit_button("Add Criminal Record")
        
        if submitted:
            if not name or not case_number or not image_file:
                st.error("Please fill in all required fields (marked with *)")
            else:
                try:
                    # Save image
                    image = Image.open(image_file)
                    image = resize_image(image, IMAGE_MAX_SIZE)
                    
                    # Create unique filename
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    image_filename = f"{case_number}_{timestamp}.jpg"
                    image_path = IMAGES_DIR / image_filename
                    image.save(image_path)
                    
                    # Placeholder for embedding path
                    embedding_filename = f"{case_number}_{timestamp}.npy"
                    embedding_path = EMBEDDINGS_DIR / embedding_filename
                    
                    # Add to database
                    criminal_id = add_criminal(
                        name=name,
                        case_number=case_number,
                        image_path=str(image_path),
                        embedding_path=str(embedding_path),
                        age=age if age > 0 else None,
                        gender=gender if gender else None,
                        crime_type=crime_type if crime_type else None,
                        arrest_date=arrest_date.strftime("%Y-%m-%d"),
                        location=location if location else None,
                        description=description if description else None
                    )
                    
                    st.success(f"✅ Criminal record added successfully! ID: {criminal_id}")
                    st.balloons()
                    
                except Exception as e:
                    st.error(f"Error adding record: {str(e)}")

# SEARCH & MATCH PAGE
elif page == "🔎 Search & Match":
    st.header("Search & Face Matching")
    
    tab1, tab2 = st.tabs(["📝 Search by Details", "👤 Face Match"])
    
    with tab1:
        st.subheader("Search Criminal Database")
        search_query = st.text_input("Search by Name or Case Number", placeholder="Enter search term...")
        
        if st.button("Search"):
            if search_query:
                results = search_criminals(search_query)
                
                if results:
                    st.success(f"Found {len(results)} result(s)")
                    
                    for criminal in results:
                        with st.expander(f"👤 {criminal['name']} - {criminal['case_number']}"):
                            col1, col2 = st.columns([1, 2])
                            
                            with col1:
                                if criminal['image_path'] and os.path.exists(criminal['image_path']):
                                    st.image(criminal['image_path'], caption=criminal['name'])
                                else:
                                    st.warning("Image not found")
                            
                            with col2:
                                st.write(f"**Name:** {criminal['name']}")
                                st.write(f"**Case Number:** {criminal['case_number']}")
                                if criminal['age']:
                                    st.write(f"**Age:** {criminal['age']}")
                                if criminal['gender']:
                                    st.write(f"**Gender:** {criminal['gender']}")
                                if criminal['crime_type']:
                                    st.write(f"**Crime Type:** {criminal['crime_type']}")
                                if criminal['arrest_date']:
                                    st.write(f"**Arrest Date:** {criminal['arrest_date']}")
                                if criminal['location']:
                                    st.write(f"**Location:** {criminal['location']}")
                                if criminal['description']:
                                    st.write(f"**Description:** {criminal['description']}")
                else:
                    st.warning("No results found")
            else:
                st.info("Enter a search term to begin")
    
    with tab2:
        st.subheader("Face Matching (Coming Soon)")
        st.info("Face matching functionality will be implemented with face recognition models.")
        
        uploaded_face = st.file_uploader("Upload Face to Match", type=["jpg", "jpeg", "png"])
        
        if uploaded_face:
            image = Image.open(uploaded_face)
            st.image(image, caption="Uploaded Image", width=300)
            
            if st.button("Find Matches"):
                st.warning("Face recognition model integration pending. This feature will compare the uploaded face against all criminal records.")

# VIEW DATABASE PAGE
elif page == "📋 View Database":
    st.header("Criminal Database Records")
    
    criminals = get_all_criminals()
    
    if criminals:
        st.success(f"Total Records: {len(criminals)}")
        
        # Display options
        view_mode = st.radio("View Mode", ["Table", "Cards"], horizontal=True)
        
        if view_mode == "Table":
            # Create table data
            import pandas as pd
            
            table_data = []
            for c in criminals:
                table_data.append({
                    "ID": c['id'],
                    "Name": c['name'],
                    "Case Number": c['case_number'],
                    "Age": c['age'] or "N/A",
                    "Gender": c['gender'] or "N/A",
                    "Crime Type": c['crime_type'] or "N/A",
                    "Arrest Date": c['arrest_date'] or "N/A",
                    "Location": c['location'] or "N/A"
                })
            
            df = pd.DataFrame(table_data)
            st.dataframe(df, use_container_width=True)
        
        else:  # Cards view
            cols_per_row = 3
            for i in range(0, len(criminals), cols_per_row):
                cols = st.columns(cols_per_row)
                for j, col in enumerate(cols):
                    if i + j < len(criminals):
                        criminal = criminals[i + j]
                        with col:
                            with st.container():
                                if criminal['image_path'] and os.path.exists(criminal['image_path']):
                                    st.image(criminal['image_path'], use_column_width=True)
                                else:
                                    st.warning("No Image")
                                
                                st.write(f"**{criminal['name']}**")
                                st.write(f"Case: {criminal['case_number']}")
                                if criminal['crime_type']:
                                    st.write(f"Crime: {criminal['crime_type']}")
                                st.markdown("---")
    else:
        st.info("No records in database. Add criminals using the 'Add Criminal' page.")

# Footer
st.sidebar.markdown("---")
st.sidebar.info("Criminal Face Database System v1.0")

