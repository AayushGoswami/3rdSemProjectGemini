-- 1. CRIMINALS TABLE
-- Stores the permanent records and links to the biometric data.
CREATE TABLE IF NOT EXISTS criminals (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    dob DATE,
    nationality TEXT,
    
    -- Case Details
    crime_category TEXT,  -- e.g., 'Theft', 'Assault', 'Fraud'
    risk_level TEXT CHECK(risk_level IN ('Low', 'Medium', 'High', 'Critical')),
    status TEXT DEFAULT 'Wanted', -- e.g., 'Wanted', 'In Custody', 'Released'
    last_known_location TEXT,
    
    -- Biometric Data Links
    photo_path TEXT,      -- Path to the visual mugshot (data/images/filename.jpg)
    embedding_path TEXT,  -- Path to the serialized vector (data/embeddings/filename.pkl)
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. SEARCH_LOGS TABLE
-- Functions as the 'Chain of Custody'. It records every time the system is used.
CREATE TABLE IF NOT EXISTS search_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    search_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Input Data
    input_image_name TEXT, -- Name of the uploaded image used for search
    
    -- Result Data
    match_found BOOLEAN CHECK (match_found IN (0, 1)),
    matched_criminal_id INTEGER, -- NULL if no match was found
    confidence_score REAL,       -- The distance score (lower is usually better in face_rec)
    
    -- Link back to the criminal profile if a match occurred
    FOREIGN KEY (matched_criminal_id) REFERENCES criminals (id)
);

-- 3. INDEXING
-- Speeds up searches by ID and Name
CREATE INDEX IF NOT EXISTS idx_lastname ON criminals(last_name);
CREATE INDEX IF NOT EXISTS idx_status ON criminals(status);

-- 4. AUDIT TRAIL TABLE
-- Records changes made to criminal records for accountability.
CREATE TABLE IF NOT EXISTS audit_trail (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    criminal_id INTEGER,
    changed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    changed_by TEXT, -- User who made the change
    change_description TEXT,
    FOREIGN KEY (criminal_id) REFERENCES criminals (id)
); 
-- 5. SYSTEM SETTINGS TABLE
-- Stores configuration settings for the face detection system.
CREATE TABLE IF NOT EXISTS system_settings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    setting_name TEXT UNIQUE NOT NULL,
    setting_value TEXT NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
-- 6. USER ACCOUNTS TABLE
-- Manages user access to the system.
CREATE TABLE IF NOT EXISTS user_accounts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    role TEXT CHECK(role IN ('Admin', 'Investigator', 'Viewer')) DEFAULT 'Viewer',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP
);
-- 7. ROLES AND PERMISSIONS TABLE
-- Defines roles and their permissions within the system.
CREATE TABLE IF NOT EXISTS roles_permissions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    role TEXT UNIQUE NOT NULL,
    permissions TEXT NOT NULL -- Comma-separated list of permissions
);
-- 8. NOTIFICATIONS TABLE
-- Stores notifications related to criminal status changes or system alerts.
CREATE TABLE IF NOT EXISTS notifications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    criminal_id INTEGER,
    notification_type TEXT, -- e.g., 'Status Change', 'New Match Found'
    message TEXT,
    is_read BOOLEAN CHECK (is_read IN (0, 1)) DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (criminal_id) REFERENCES criminals (id)
);
-- 9. BACKUP LOGS TABLE
-- Records details of database backups for recovery purposes.
CREATE TABLE IF NOT EXISTS backup_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    backup_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    backup_path TEXT,
    performed_by TEXT -- User who performed the backup
);
-- 10. SYSTEM AUDIT LOGS TABLE
-- Logs system-level events for security and monitoring.
CREATE TABLE IF NOT EXISTS system_audit_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    event_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    event_type TEXT, -- e.g., 'Login', 'Data Access', 'Error'
    event_description TEXT,
    performed_by TEXT -- User who triggered the event
); 
-- End of schema.sql
