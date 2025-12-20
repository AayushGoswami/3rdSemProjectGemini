import streamlit as st
import time
import os
import sys
from datetime import datetime

# Adjust path to allow imports from sibling directories
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# --- LOCAL IMPORTS ---
from database.db_connector import (
    add_criminal, 
    get_criminal_by_id, 
    log_search, 
    verify_user, 
    log_audit_event
)
from models.encoder import get_face_embedding, save_embedding
from app.face_matcher import find_match
import app.config as cfg
from app.utils import load_css, resize_image, render_risk_badge

# --- PAGE CONFIG ---
st.set_page_config(page_title="Criminal Face DB", page_icon="👮", layout="wide")

# --- SESSION STATE INITIALIZATION ---
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'user_role' not in st.session_state:
    st.session_state['user_role'] = None
if 'username' not in st.session_state:
    st.session_state['username'] = None

# --- LOAD STYLES ---
css_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static", "style.css")
if os.path.exists(css_path):
    load_css(css_path)

# ==========================================
# 🔐 AUTHENTICATION LOGIC
# ==========================================
def login_page():
    st.markdown("<h1 style='text-align: center; color: #ff4b4b;'>👮 CENTRAL DATABASE ACCESS</h1>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with st.form("login_form"):
            st.info("Authorized Personnel Only")
            username = st.text_input("Officer ID / Username")
            password = st.text_input("Password", type="password")
            submitted = st.form_submit_button("Login")
            
            if submitted:
                role = verify_user(username, password)
                if role:
                    st.session_state['logged_in'] = True
                    st.session_state['user_role'] = role
                    st.session_state['username'] = username
                    st.success(f"✅ Welcome, {role} {username}")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("❌ Invalid Credentials")

def logout():
    st.session_state['logged_in'] = False
    st.session_state['user_role'] = None
    st.session_state['username'] = None
    st.rerun()

# ==========================================
# 🖥️ MAIN DASHBOARD
# ==========================================
def main_dashboard():
    # Sidebar Info
    st.sidebar.title(f"👮 Officer: {st.session_state['username']}")
    st.sidebar.caption(f"Role: {st.session_state['user_role']}")
    
    if st.sidebar.button("Log Out"):
        logout()
    
    st.sidebar.divider()
    
    # Navigation Options based on Role
    nav_options = ["Home", "Face Recognition"]
    
    # Only Admins/Investigators can register new criminals
    if st.session_state['user_role'] in ['Admin', 'Investigator']:
        nav_options.append("Register Criminal")
        
    choice = st.sidebar.radio("Navigation", nav_options)

    # --- HOME TAB ---
    if choice == "Home":
        st.title("🎛️ Command Center")
        st.markdown(f"""
        ### Welcome, {st.session_state['username']}.
        
        **System Integrity Check:**
        * Database Connection: ✅ Active
        * Audit Logging: ✅ Enabled
        * User Permissions: ✅ {st.session_state['user_role']} Level
        """)
        
        if st.session_state['user_role'] == 'Viewer':
            st.warning("⚠️ Restricted Mode: You have Read-Only access.")

    # --- REGISTER TAB (Protected) ---
    elif choice == "Register Criminal":
        st.title("📂 Register New Criminal")
        
        c1, c2 = st.columns(2)
        with c1:
            fname = st.text_input("First Name")
            lname = st.text_input("Last Name")
            dob = st.date_input("DOB")
            nat = st.text_input("Nationality")
        with c2:
            crime = st.selectbox("Crime", ["Theft", "Assault", "Fraud", "Murder", "Cybercrime", "Drug Trafficking"])
            risk = st.selectbox("Risk Level", ["Low", "Medium", "High", "Critical"])
            status = st.selectbox("Status", ["Wanted", "In Custody", "Released"])
            loc = st.text_input("Last Known Location")
            
        uploaded = st.file_uploader("Upload Mugshot", type=["jpg", "png", "jpeg"])
        
        if st.button("Save Record", type="primary"):
            if uploaded and fname and lname:
                # File Logic
                ext = uploaded.name.split('.')[-1]
                filename = f"{fname}_{lname}_{datetime.now().strftime('%Y%m%d%H%M%S')}.{ext}"
                img_path = os.path.join(cfg.IMAGES_DIR, filename)
                
                with open(img_path, "wb") as f:
                    f.write(uploaded.getbuffer())
                
                resize_image(img_path)
                
                # Embedding Logic
                with st.spinner("Processing Biometrics..."):
                    emb = get_face_embedding(img_path)
                    
                if emb is not None:
                    emb_filename = filename.replace(f".{ext}", ".pkl")
                    emb_path = os.path.join(cfg.EMBEDDINGS_DIR, emb_filename)
                    save_embedding(emb, emb_path)
                    
                    # Database Entry
                    new_id = add_criminal(fname, lname, crime, risk, status, loc, img_path, emb_path, dob, nat)
                    
                    if new_id:
                        # AUDIT LOGGING: Record WHO added this criminal
                        log_audit_event(
                            new_id, 
                            st.session_state['username'], 
                            "Created new criminal profile"
                        )
                        st.success(f"✅ Record created for {fname} {lname} (ID: {new_id})")
                else:
                    st.error("❌ No face detected.")
                    os.remove(img_path)
            else:
                st.warning("⚠️ Missing data.")

    # --- RECOGNITION TAB ---
    elif choice == "Face Recognition":
        st.title("🔍 Face Scanner")
        
        scan = st.file_uploader("Upload Surveillance Image", type=["jpg", "png"])
        
        if scan:
            st.image(scan, width=250)
            if st.button("Identify Target", type="primary"):
                # Temp file
                tpath = os.path.join(cfg.DATA_DIR, "temp.jpg")
                with open(tpath, "wb") as f:
                    f.write(scan.getbuffer())
                resize_image(tpath)
                
                with st.spinner("Running Facial Recognition..."):
                    emb = get_face_embedding(tpath)
                    if emb is not None:
                        found, crim_id, conf = find_match(emb)
                        
                        # LOG SEARCH
                        log_search(scan.name, found, crim_id, conf)
                        
                        if found:
                            crim = get_criminal_by_id(crim_id)
                            st.markdown(f"""
                            <div class="match-alert">
                            🚨 MATCH FOUND ({round((1-conf)*100, 1)}%)
                            </div>
                            """, unsafe_allow_html=True)
                            
                            c1, c2 = st.columns([1, 2])
                            with c1:
                                if os.path.exists(crim['photo_path']):
                                    st.image(crim['photo_path'])
                            with c2:
                                st.subheader(f"{crim['first_name']} {crim['last_name']}")
                                st.write(f"**Status:** {crim['status']}")
                                st.write(f"**Risk:** {render_risk_badge(crim['risk_level'])}")
                        else:
                            st.info("✅ No Match Found.")
                    else:
                        st.error("❌ No face detected in scan.")
                
                if os.path.exists(tpath):
                    os.remove(tpath)

# ==========================================
# 🚀 APP ENTRY POINT
# ==========================================
if __name__ == "__main__":
    if st.session_state['logged_in']:
        main_dashboard()
    else:
        login_page()