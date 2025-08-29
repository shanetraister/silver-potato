# test_db.py
from sqlalchemy import create_engine, text
from app.settings import DATABASE_URL

try:
    engine = create_engine(DATABASE_URL)
    with engine.connect() as conn:
        result = conn.execute(text("SELECT 1"))  # Wrap in text()
        print("Database connection successful!")
        print(f"Result: {result.fetchone()}")
except Exception as e:
    print(f"Database connection failed: {e}")