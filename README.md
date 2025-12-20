# Criminal Face Detection (Streamlit)

Prototype Streamlit app for enrolling reference faces and matching probe images against a local gallery using `face_recognition` embeddings.

## Features
- Enroll new reference faces and persist embeddings to disk
- Match probe uploads against the gallery with tunable tolerance and top-k results
- SQLite-backed match logs and simple recent-activity table
- Minimal theming via Streamlit and a small CSS override

## Project Layout
```
criminal-face-detection/
├── app/                # Streamlit entry + helpers
├── models/             # Embedding encoder wrapper
├── data/               # Images, embeddings, logs (gitkept)
├── database/           # SQLite helpers and schema
├── static/             # CSS overrides
├── tests/              # Pytest suite
├── requirements.txt    # Runtime + dev deps
└── .streamlit/         # Streamlit theme
```

## Setup
1) Install Python 3.10+ and system build tools (needed for `face_recognition`/`dlib`). On Debian/Ubuntu: `sudo apt-get install build-essential cmake libopenblas-dev liblapack-dev libx11-dev libgtk-3-dev`.
2) Install Python deps from the project root:
```
cd criminal-face-detection
pip install -r requirements.txt
```
3) Initialize the SQLite database (creates `database/criminals.db`):
```
python -m database.init_db
```
4) Run the Streamlit app:
```
streamlit run app/main.py
```

## Testing
Run the lightweight unit tests from inside `criminal-face-detection`:
```
pytest
```

## Notes
- The `face_recognition` package pulls in `dlib`; ensure native build tools are present before installing dependencies.
- Default tolerance/backends are configurable in `app/config.py`.