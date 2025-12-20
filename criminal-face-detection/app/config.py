import os

# Base Directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Data Paths
DATA_DIR = os.path.join(BASE_DIR, "data")
IMAGES_DIR = os.path.join(DATA_DIR, "images")
EMBEDDINGS_DIR = os.path.join(DATA_DIR, "embeddings")
LOGS_DIR = os.path.join(DATA_DIR, "logs")

# Database Path
DB_PATH = os.path.join(BASE_DIR, "database", "criminals.db")

# Face Recognition Settings
THRESHOLD = 0.5  # Stricter for criminal matching
MODEL_TYPE = "hog" # Use "cnn" if you have a GPU