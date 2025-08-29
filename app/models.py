from sqlalchemy import Column, String, DateTime, UUID, JSON, Float, ForeignKey, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from app.settings import DATABASE_URL
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi import HTTPException

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class BaseModel(Base):
    __abstract__ = True
    @classmethod
    def get(cls, id):
        db = SessionLocal()
        try:
            return db.query(cls).filter(cls.id == id).first()
        except Exception as e:
            raise HTTPException(status_code=404, detail="Record not found")
        finally:
            db.close()

class Job(BaseModel):
    __tablename__ = "jobs"
    
    id = Column(UUID(as_uuid=True), primary_key=True, index=True)
    # session_id = Column(UUID(as_uuid=True), ForeignKey("sessions.id"))  # Add this
    task = Column(String, index=True)
    task_params = Column(JSON)
    status = Column(String, index=True)
    started_at = Column(DateTime, default=datetime.now())  # Use UTC
    completed_at = Column(DateTime)
    input_image_id = Column(UUID(as_uuid=True), ForeignKey("images.id"))
    output_image_id = Column(UUID(as_uuid=True), ForeignKey("images.id"))
    
    # Relationships
    # session = relationship("Session", back_populates="jobs")
    input_image = relationship("Image", foreign_keys=[input_image_id])
    output_image = relationship("Image", foreign_keys=[output_image_id])

class Image(BaseModel):
    __tablename__ = "images"
    
    id = Column(UUID(as_uuid=True), primary_key=True, index=True)
    storage_path = Column(String)  # Specify the type
    uploaded_at = Column(DateTime, default=datetime.now())
    # Remove image_type - you can determine this from created_by_job_id
    created_by_job_id = Column(UUID(as_uuid=True), ForeignKey("jobs.id"))
    
    # Image metadata
    width = Column(Float)
    height = Column(Float)  
    channels = Column(Integer)  # 3 for RGB, 4 for RGBA
    format = Column(String)  # "JPEG", "PNG", etc.
    file_size = Column(Integer)  # bytes
    
class Session(BaseModel):
    __tablename__ = "sessions"
    
    id = Column(UUID(as_uuid=True), primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.now())
    last_activity = Column(DateTime, default=datetime.now())
    
    # Relationship instead of storing IDs
    # jobs = relationship("Job", back_populates="session")