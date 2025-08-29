# create_tables.py
from app.models import Base
from sqlalchemy import create_engine
from app.settings import DATABASE_URL

engine = create_engine(DATABASE_URL)
Base.metadata.create_all(bind=engine)
print("Tables created!")