# Criminal Face Database System

A Streamlit-based web application for managing criminal records with facial recognition capabilities.

## Features

- **Add Criminal Records**: Store criminal information with photos and metadata
- **Search Functionality**: Search by name or case number
- **Database Management**: View and manage all criminal records
- **Face Recognition**: (Placeholder for future face matching integration)
- **Custom Dark Theme**: Red/dark themed UI optimized for law enforcement

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Initialize the database:
```bash
cd Criminal_Face_DB
python database/init_db.py
```

## Running the Application

From the `Criminal_Face_DB` directory:

```bash
streamlit run app/main.py
```

The application will open in your browser at `http://localhost:8501`

## Project Structure

```
Criminal_Face_DB/
├── app/
│   ├── main.py           # Main Streamlit application
│   ├── config.py         # Configuration and paths
│   ├── utils.py          # Helper functions (CSS loading, image processing)
│   └── face_matcher.py   # Face matching logic (to be implemented)
├── database/
│   ├── init_db.py        # Database initialization script
│   ├── schema.sql        # Database schema
│   └── db_connector.py   # Database operations
├── models/
│   └── encoder.py        # Face encoding models (to be implemented)
├── static/
│   └── style.css         # Custom CSS styling
├── .streamlit/
│   └── config.toml       # Streamlit configuration
└── data/
    ├── images/           # Stored criminal photos
    ├── embeddings/       # Face embeddings
    └── logs/             # Application logs
```

## Usage

### Adding a Criminal Record

1. Navigate to "➕ Add Criminal" from the sidebar
2. Fill in required fields (Name, Case Number)
3. Upload a photo
4. Add optional details (age, gender, crime type, etc.)
5. Click "Add Criminal Record"

### Searching Records

1. Navigate to "🔎 Search & Match"
2. Use the "Search by Details" tab
3. Enter a name or case number
4. View matching results with full details

### Viewing Database

1. Navigate to "📋 View Database"
2. Choose between Table or Cards view
3. Browse all criminal records

## Configuration

- **Database Path**: `database/criminals.db`
- **Image Storage**: `data/images/`
- **Theme Colors**: Defined in `.streamlit/config.toml` and `static/style.css`
- **Face Recognition Threshold**: Set in `app/config.py`

## Future Enhancements

- Face recognition model integration (DeepFace or face-recognition)
- Real-time face matching against database
- Advanced search filters
- Export/import functionality
- User authentication and access control
- Audit logging for all operations

## Notes

- The database is stored locally in SQLite format
- Images are stored in the `data/images/` directory
- Face embeddings (when implemented) will be stored in `data/embeddings/`
