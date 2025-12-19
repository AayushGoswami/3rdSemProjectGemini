-- SQL table definitions for Criminal Face Database

CREATE TABLE IF NOT EXISTS criminals (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    age INTEGER,
    gender TEXT,
    crime_type TEXT,
    case_number TEXT UNIQUE,
    arrest_date DATE,
    location TEXT,
    image_path TEXT,
    embedding_path TEXT,
    description TEXT,
    status TEXT DEFAULT 'Active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS matches (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    criminal_id INTEGER,
    query_image_path TEXT,
    confidence_score REAL,
    match_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (criminal_id) REFERENCES criminals(id)
);

CREATE INDEX IF NOT EXISTS idx_case_number ON criminals(case_number);
CREATE INDEX IF NOT EXISTS idx_status ON criminals(status);
CREATE INDEX IF NOT EXISTS idx_criminal_id ON matches(criminal_id);
