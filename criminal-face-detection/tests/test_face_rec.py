import unittest
import os
import sys
import numpy as np
import pickle
import sqlite3

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import database.init_db as init_script
import database.db_connector as db
import app.config as cfg
from app.face_matcher import find_match

class TestFaceRecognitionLogic(unittest.TestCase):
    
    def setUp(self):
        """
        Set up a complete sandbox environment:
        1. Temporary Database
        2. Temporary Embedding Folder
        """
        # --- 1. Setup Test Config ---
        self.test_db_path = "tests/test_criminals_ai.db"
        self.test_emb_dir = "tests/temp_embeddings"
        
        # Override the app's config to point to our test sandbox
        db.DB_PATH = self.test_db_path
        cfg.DB_PATH = self.test_db_path
        init_script.DB_PATH = self.test_db_path
        
        # Create directories
        os.makedirs(self.test_emb_dir, exist_ok=True)
        
        # Initialize DB Schema
        init_script.initialize_database()

        # --- 2. Create a "Known" Face Vector ---
        # We simulate a face by creating a random list of 128 numbers
        self.known_vector = np.random.rand(128)
        self.known_pickle_path = os.path.join(self.test_emb_dir, "known_face.pkl")
        
        # Save this "fake face" to a pickle file
        with open(self.known_pickle_path, 'wb') as f:
            pickle.dump(self.known_vector, f)
            
        # Register it in the DB
        db.add_criminal(
            "Target", "Subject", "Testing", "High", "Wanted", "Lab",
            "dummy_image.jpg", self.known_pickle_path
        )

    def tearDown(self):
        """Cleanup files after tests."""
        if os.path.exists(self.test_db_path):
            os.remove(self.test_db_path)
        
        # Remove the temp embedding file and folder
        if os.path.exists(self.known_pickle_path):
            os.remove(self.known_pickle_path)
        if os.path.exists(self.test_emb_dir):
            os.rmdir(self.test_emb_dir)

    def test_positive_match(self):
        """Test Case A: The suspect IS the criminal."""
        print("\nTesting Positive Match (Target Found)...")
        
        # 1. Simulate a camera scanning the exact same face
        # (In real life, there would be slight variance, but this tests the pipeline)
        unknown_vector = self.known_vector 
        
        # 2. Ask the system: "Do you know this person?"
        found, crim_id, distance = find_match(unknown_vector)
        
        # 3. Assertions
        self.assertTrue(found, "System failed to match an identical face vector!")
        self.assertIsNotNone(crim_id, "System matched but returned no ID.")
        self.assertLess(distance, 0.1, "Distance should be near 0 for identical vectors.")
        
        print(f"   ✅ Success! Matched ID: {crim_id} with Distance: {distance}")

    def test_negative_match(self):
        """Test Case B: The suspect is an innocent stranger."""
        print("Testing Negative Match (Stranger Ignored)...")
        
        # 1. Generate a completely different random vector
        stranger_vector = np.random.rand(128)
        
        # 2. Ask the system
        found, crim_id, distance = find_match(stranger_vector)
        
        # 3. Assertions
        self.assertFalse(found, "System falsely identified a random stranger!")
        self.assertIsNone(crim_id, "ID should be None for non-matches.")
        self.assertGreater(distance, 0.6, "Distance should be high for strangers.")
        
        print(f"   ✅ Success! Stranger ignored. Distance: {distance}")

if __name__ == '__main__':
    unittest.main()