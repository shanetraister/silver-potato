# here's where I'll make calls to the DB like create_image_record and create_job_record
import os
from app.models import Image, Job, Session
from app.settings import DATABASE_URL
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import time
import uuid

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def create_image_record(image_metadata: dict, max_retries: int = 3):
    """
    Create an image record in the database.
    Retry on failure before cleaning up files and giving up.

    Args:
        image_metadata (dict): Metadata for the image to be stored.
        max_retries (int): Maximum number of retries before giving up.
    """
    for attempt in range(max_retries):
        try:
            db = SessionLocal()
            image = Image(**image_metadata)
            db.add(image)
            db.commit()
            db.refresh(image)
            return image
        except Exception as e:
            if attempt == max_retries - 1:
                if os.path.exists(image_metadata["storage_path"]):
                    os.remove(image_metadata["storage_path"])
                raise e
            time.sleep(0.5)
        finally:
            db.close()

def create_job_record(image_id: Image.id, processor: str, params: dict, max_retries: int = 3):
    """
    Create a job record in the database.
    Retry on failure before giving up.

    Args:
        image_id (Image.id): ID of the image to be processed.
        processor (str): Name of the processor to be used.
        params (dict): Parameters for the processor.
        max_retries (int): Maximum number of retries before giving up.
    """

    for attempt in range(max_retries):
        try:
            db = SessionLocal()
            job_record = {
                "id": uuid.uuid4(),
                "input_image_id": image_id,
                "task": processor,
                "task_params": params,
                "status": "pending"
                # "session_id": None, # to be implemented later
            }
            job = Job(**job_record)
            db.add(job)
            db.commit()
            db.refresh(job)
            return job
        except Exception as e:
            if attempt == max_retries - 1:
                raise e
            time.sleep(0.5)
        finally:
            db.close()