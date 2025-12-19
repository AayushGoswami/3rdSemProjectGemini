"""
Functions to add/get criminals from database
"""
import sqlite3
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from datetime import datetime

DB_PATH = Path(__file__).parent / "criminals.db"

def get_connection():
    """Get database connection"""
    return sqlite3.connect(DB_PATH)

def add_criminal(
    name: str,
    case_number: str,
    image_path: str,
    embedding_path: str,
    age: Optional[int] = None,
    gender: Optional[str] = None,
    crime_type: Optional[str] = None,
    arrest_date: Optional[str] = None,
    location: Optional[str] = None,
    description: Optional[str] = None
) -> int:
    """
    Add a new criminal record to database
    
    Returns:
        ID of the inserted record
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO criminals (
            name, age, gender, crime_type, case_number,
            arrest_date, location, image_path, embedding_path, description
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (name, age, gender, crime_type, case_number, arrest_date, 
          location, image_path, embedding_path, description))
    
    criminal_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    return criminal_id

def get_criminal_by_id(criminal_id: int) -> Optional[Dict]:
    """Get criminal record by ID"""
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM criminals WHERE id = ?", (criminal_id,))
    row = cursor.fetchone()
    conn.close()
    
    return dict(row) if row else None

def get_all_criminals() -> List[Dict]:
    """Get all criminal records"""
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM criminals ORDER BY created_at DESC")
    rows = cursor.fetchall()
    conn.close()
    
    return [dict(row) for row in rows]

def search_criminals(query: str) -> List[Dict]:
    """Search criminals by name or case number"""
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    search_pattern = f"%{query}%"
    cursor.execute("""
        SELECT * FROM criminals 
        WHERE name LIKE ? OR case_number LIKE ?
        ORDER BY created_at DESC
    """, (search_pattern, search_pattern))
    
    rows = cursor.fetchall()
    conn.close()
    
    return [dict(row) for row in rows]

def add_match_record(criminal_id: int, query_image_path: str, confidence_score: float):
    """Record a face match"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO matches (criminal_id, query_image_path, confidence_score)
        VALUES (?, ?, ?)
    """, (criminal_id, query_image_path, confidence_score))
    
    conn.commit()
    conn.close()

def get_matches_for_criminal(criminal_id: int) -> List[Dict]:
    """Get all matches for a specific criminal"""
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT * FROM matches 
        WHERE criminal_id = ?
        ORDER BY match_date DESC
    """, (criminal_id,))
    
    rows = cursor.fetchall()
    conn.close()
    
    return [dict(row) for row in rows]
