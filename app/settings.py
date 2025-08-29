import os

DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "postgresql://imageuser:imagepass@localhost:5432/imageprocessor"
)

UPLOAD_DIR = os.getenv("UPLOAD_DIR", "uploads")