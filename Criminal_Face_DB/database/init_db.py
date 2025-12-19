"""
Initialize the database - Run this once to create criminals.db
"""
import sqlite3
from pathlib import Path

def init_database():
    """
    Create the database and tables using schema.sql
    """
    # Get paths
    db_dir = Path(__file__).parent
    db_path = db_dir / "criminals.db"
    schema_path = db_dir / "schema.sql"
    
    # Read schema
    with open(schema_path, 'r') as f:
        schema_sql = f.read()
    
    # Create database and execute schema
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        cursor.executescript(schema_sql)
        conn.commit()
        print(f"✅ Database created successfully at: {db_path}")
        print("✅ Tables created: criminals, matches")
    except Exception as e:
        print(f"❌ Error creating database: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    init_database()
