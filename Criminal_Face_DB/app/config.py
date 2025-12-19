"""
Configuration file for paths and constants
"""
from pathlib import Path

# Base paths
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
DATABASE_DIR = BASE_DIR / "database"
STATIC_DIR = BASE_DIR / "static"

# Data subdirectories
IMAGES_DIR = DATA_DIR / "images"
EMBEDDINGS_DIR = DATA_DIR / "embeddings"
LOGS_DIR = DATA_DIR / "logs"

# Database
DB_PATH = DATABASE_DIR / "criminals.db"

# Model settings
FACE_RECOGNITION_THRESHOLD = 0.6
IMAGE_MAX_SIZE = (800, 800)

# Create directories if they don't exist
for directory in [IMAGES_DIR, EMBEDDINGS_DIR, LOGS_DIR]:
    directory.mkdir(parents=True, exist_ok=True)
