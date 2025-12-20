import face_recognition
import numpy as np
import pickle
import os
import sqlite3
import app.config as cfg  # <--- IMPORT CONFIGURATION
from database.db_connector import DB_PATH

def get_known_faces_from_db():
    """
    Connects to the database to retrieve the list of valid criminals
    and their embedding file paths. 
    """
    known_ids = []
    known_encodings = []

    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Only fetch criminals who have a valid embedding file path
        cursor.execute("SELECT id, embedding_path FROM criminals WHERE embedding_path IS NOT NULL")
        rows = cursor.fetchall()
        
        for row in rows:
            criminal_id, pickle_path = row
            
            # Verify file exists
            if os.path.exists(pickle_path):
                try:
                    with open(pickle_path, 'rb') as f:
                        encoding = pickle.load(f)
                        
                        # Verify integrity
                        if encoding is not None and len(encoding) == 128:
                            known_ids.append(criminal_id)
                            known_encodings.append(encoding)
                except Exception as e:
                    print(f"⚠️ Corrupt embedding file for ID {criminal_id}: {e}")
        
        conn.close()
        
    except sqlite3.Error as e:
        print(f"❌ Database error in matcher: {e}")
        
    return known_ids, known_encodings

def find_match(unknown_encoding):
    """
    Compares the unknown encoding against all known encodings.
    Uses strictness defined in app/config.py.
    """
    known_ids, known_encodings = get_known_faces_from_db()
    
    if not known_encodings:
        return False, None, 0.0

    # Calculate Euclidean distance (0.0 is perfect match)
    distances = face_recognition.face_distance(known_encodings, unknown_encoding)
    
    best_match_index = np.argmin(distances)
    best_distance = distances[best_match_index]
    
    # USE CONFIG THRESHOLD
    if best_distance <= cfg.THRESHOLD:
        matched_id = known_ids[best_match_index]
        return True, matched_id, best_distance
    else:
        return False, None, best_distance