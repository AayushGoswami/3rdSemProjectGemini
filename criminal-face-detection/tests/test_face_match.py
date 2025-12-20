import unittest
import os
import sys
import sqlite3

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import database.init_db as init_script
import database.db_connector as db
import app.config as cfg

class TestCriminalSystem(unittest.TestCase):
    
    def setUp(self):
        """
        Run before EVERY test.
        Sets up a temporary TEST database.
        """
        # 1. Point config to a test DB file
        self.test_db_path = "tests/test_criminals.db"
        db.DB_PATH = self.test_db_path
        init_script.DB_PATH = self.test_db_path
        
        # 2. Initialize the schema
        # We suppress the print statements to keep test output clean
        init_script.initialize_database()

    def tearDown(self):
        """
        Run after EVERY test.
        Deletes the test database to clean up.
        """
        if os.path.exists(self.test_db_path):
            os.remove(self.test_db_path)

    def test_1_admin_login(self):
        """Test if the default admin account is created and works."""
        print("\nTesting Admin Authentication...")
        
        # Try to login with correct credentials
        role = db.verify_user("admin", "admin123")
        self.assertEqual(role, "Admin", "Default admin should have Admin role")
        
        # Try to login with wrong password
        role_fail = db.verify_user("admin", "wrongpass")
        self.assertIsNone(role_fail, "Wrong password should return None")

    def test_2_add_criminal_and_audit(self):
        """Test adding a criminal and checking if it hits the Audit Log."""
        print("Testing Criminal Registration & Audit Trail...")
        
        # 1. Add a dummy criminal
        new_id = db.add_criminal(
            "Test", "Guy", "Theft", "Low", "Wanted", "Unknown", 
            "dummy.jpg", "dummy.pkl"
        )
        self.assertIsNotNone(new_id, "Should return a new ID")
        
        # 2. Check if he exists in DB
        criminal = db.get_criminal_by_id(new_id)
        self.assertEqual(criminal['first_name'], "Test")
        
        # 3. MANUALLY log an audit event (simulating the app)
        db.log_audit_event(new_id, "admin", "Created Profile")
        
        # 4. Verify Audit Trail
        conn = sqlite3.connect(self.test_db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM audit_trail WHERE criminal_id = ?", (new_id,))
        log = cursor.fetchone()
        conn.close()
        
        self.assertIsNotNone(log, "Audit log should exist")
        self.assertEqual(log[3], "admin", "Audit log should show 'admin' as the user")

    def test_3_database_integrity(self):
        """Test if all 10 tables exist."""
        print("Testing Schema Integrity...")
        conn = sqlite3.connect(self.test_db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [t[0] for t in cursor.fetchall()]
        conn.close()
        
        required_tables = ["criminals", "user_accounts", "audit_trail", "search_logs"]
        for t in required_tables:
            self.assertIn(t, tables, f"Table {t} is missing from database")

if __name__ == '__main__':
    unittest.main()