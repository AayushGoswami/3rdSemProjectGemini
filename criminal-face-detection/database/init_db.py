import sqlite3
import os
import hashlib

# Define paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "criminals.db")
SCHEMA_PATH = os.path.join(BASE_DIR, "schema.sql")

def hash_password(password):
    """Generates SHA-256 hash for the default admin password."""
    return hashlib.sha256(password.encode()).hexdigest()

def initialize_database():
    """
    1. Creates/Resets the database file.
    2. Runs the 10-table schema.
    3. Creates the default Admin user.
    """
    print(f"⚡ Initializing Database at: {DB_PATH}")

    # Check for schema file
    if not os.path.exists(SCHEMA_PATH):
        print(f"❌ Error: Schema file not found at {SCHEMA_PATH}")
        return

    try:
        # Connect to SQLite
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # 1. EXECUTE SCHEMA
        print("📜 Applying Schema...")
        with open(SCHEMA_PATH, 'r') as f:
            schema_script = f.read()
        cursor.executescript(schema_script)
        
        # 2. CREATE DEFAULT ADMIN USER
        # We insert manually here to ensure the system is usable immediately
        print("🔐 Configuring Security...")
        admin_user = "admin"
        admin_pass = "admin123"
        admin_hash = hash_password(admin_pass)
        
        # Check if admin exists to avoid duplicate errors or overwrites
        cursor.execute("SELECT id FROM user_accounts WHERE username = ?", (admin_user,))
        if cursor.fetchone() is None:
            cursor.execute(
                "INSERT INTO user_accounts (username, password_hash, role) VALUES (?, ?, ?)",
                (admin_user, admin_hash, 'Admin')
            )
            print(f"   ✅ Default Admin created: User='{admin_user}', Pass='{admin_pass}'")
        else:
            print("   ℹ️ Admin account already exists. Skipping creation.")

        # 3. VERIFY TABLES
        # Get list of all tables created to confirm success
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        table_names = [t[0] for t in tables]
        
        print(f"✅ Database Setup Complete! Created {len(table_names)} tables:")
        print(f"   📂 {', '.join(table_names)}")

        conn.commit()
        conn.close()

    except sqlite3.Error as e:
        print(f"❌ SQLite Error: {e}")
    except Exception as e:
        print(f"❌ Unexpected Error: {e}")

if __name__ == "__main__":
    # Optional: Delete old DB to ensure a fresh start with the new schema
    # if os.path.exists(DB_PATH):
    #     os.remove(DB_PATH)
    
    initialize_database()