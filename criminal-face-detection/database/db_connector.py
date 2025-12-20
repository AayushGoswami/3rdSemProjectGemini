import sqlite3
import os
import hashlib
from datetime import datetime

# Define path to the database file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "criminals.db")

def get_connection():
    """Establishes a connection to the SQLite database."""
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        return conn
    except sqlite3.Error as e:
        print(f"❌ Database Connection Error: {e}")
        return None

# --- AUTHENTICATION FUNCTIONS (New) ---

def hash_password(password):
    """Simple SHA-256 hashing for storage."""
    return hashlib.sha256(password.encode()).hexdigest()

def create_user(username, password, role='Viewer'):
    """Creates a new system user."""
    conn = get_connection()
    if not conn: return False
    
    pwd_hash = hash_password(password)
    
    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO user_accounts (username, password_hash, role) VALUES (?, ?, ?)",
            (username, pwd_hash, role)
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        print(f"⚠️ User {username} already exists.")
        return False
    finally:
        conn.close()

def verify_user(username, password):
    """Checks credentials and returns User Role if valid."""
    conn = get_connection()
    if not conn: return None
    
    pwd_hash = hash_password(password)
    
    try:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT role FROM user_accounts WHERE username = ? AND password_hash = ?",
            (username, pwd_hash)
        )
        row = cursor.fetchone()
        if row:
            return row['role'] # Return the role (Admin/Investigator/Viewer)
        return None
    finally:
        conn.close()

# --- LOGGING FUNCTIONS (Updated) ---

def log_audit_event(criminal_id, changed_by, description):
    """Records changes to criminal records (Table 4)."""
    conn = get_connection()
    if not conn: return
    try:
        conn.execute(
            "INSERT INTO audit_trail (criminal_id, changed_by, change_description) VALUES (?, ?, ?)",
            (criminal_id, changed_by, description)
        )
        conn.commit()
    finally:
        conn.close()

def log_system_event(event_type, description, performed_by="System"):
    """Records system-level events (Table 10)."""
    conn = get_connection()
    if not conn: return
    try:
        conn.execute(
            "INSERT INTO system_audit_logs (event_type, event_description, performed_by) VALUES (?, ?, ?)",
            (event_type, description, performed_by)
        )
        conn.commit()
    finally:
        conn.close()

# --- CORE FUNCTIONS (Existing) ---

def add_criminal(first_name, last_name, crime_category, risk_level, status, last_known_location, photo_path, embedding_path, dob=None, nationality=None):
    conn = get_connection()
    if not conn: return None

    query = """
    INSERT INTO criminals (
        first_name, last_name, dob, nationality,
        crime_category, risk_level, status, last_known_location,
        photo_path, embedding_path
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """
    try:
        cursor = conn.cursor()
        cursor.execute(query, (
            first_name, last_name, dob, nationality,
            crime_category, risk_level, status, last_known_location,
            photo_path, embedding_path
        ))
        conn.commit()
        new_id = cursor.lastrowid
        return new_id
    except sqlite3.Error as e:
        print(f"❌ Error adding criminal: {e}")
        return None
    finally:
        conn.close()

def log_search(input_image_name, match_found, matched_criminal_id=None, confidence_score=None):
    conn = get_connection()
    if not conn: return

    query = """
    INSERT INTO search_logs (
        input_image_name, match_found, matched_criminal_id, confidence_score
    ) VALUES (?, ?, ?, ?)
    """
    try:
        cursor = conn.cursor()
        match_int = 1 if match_found else 0
        cursor.execute(query, (input_image_name, match_int, matched_criminal_id, confidence_score))
        conn.commit()
    except sqlite3.Error as e:
        print(f"❌ Error logging search: {e}")
    finally:
        conn.close()

def get_criminal_by_id(criminal_id):
    conn = get_connection()
    if not conn: return None
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM criminals WHERE id = ?", (criminal_id,))
        row = cursor.fetchone()
        return dict(row) if row else None
    finally:
        conn.close()

# --- INITIALIZATION ---
# Automatically create a default Admin user if none exists
if __name__ == "__main__":
    print("--- Updating User Table ---")
    if create_user("admin", "admin123", "Admin"):
        print("✅ Default Admin user created: (admin / admin123)")
    else:
        print("ℹ️ Admin user already exists.")