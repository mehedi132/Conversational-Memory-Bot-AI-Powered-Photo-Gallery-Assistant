import os

# Base directory
BASE_DIR = os.path.join("backend", "app", "ai", "faiss_database", "database")

# File paths
METADATA_FILE = os.path.join(BASE_DIR, "image_metadata.json")
FAISS_INDEX_FILE = os.path.join(BASE_DIR, "image_faiss_index.bin")
UPLOAD_DIR = os.path.join("data", "upload_images")
IMAGES_DIR = os.path.join("data", "upload_images")

# CORS settings
CORS_ORIGINS = ["http://localhost:3000"]

# Database settings
