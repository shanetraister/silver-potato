import os
import io
import uuid
from pathlib import Path
from typing import Dict, Optional
from PIL import Image as PILImage
from fastapi import UploadFile, HTTPException

from app.models import Image
from app.settings import UPLOAD_DIR  # Your storage config

ALLOWED_TYPES = {"image/jpeg", "image/png", "image/gif", "image/webp"}
UPLOAD_DIR = Path("uploads")

class UploadHandler:
    def __init__(self, file: UploadFile):
        self.file = file
        self.contents = None
        self.pil_image = None
        self.metadata = {}
        self.storage_path = None
        
    async def process(self) -> Dict:
        """Main method - does everything and returns metadata"""
        await self._validate_and_load()
        self._extract_metadata()
        await self._save_file()
        
        return {
            "id": self.file_id,
            "storage_path": str(self.storage_path),
            "width": self.metadata["width"],
            "height": self.metadata["height"],
            "format": self.metadata["format"],
            "channels": self.metadata["channels"],
            "file_size": self.metadata["file_size"]
        }
    
    async def _validate_and_load(self):
        if self.file.content_type not in ALLOWED_TYPES:
            raise HTTPException(400, f"Unsupported file type: {self.file.content_type}")
        
        self.contents = await self.file.read()
        try:
            self.pil_image = PILImage.open(io.BytesIO(self.contents))
        except Exception as e:
            raise HTTPException(400, f"Invalid image file: {str(e)}")
    
    def _extract_metadata(self):
        width, height = self.pil_image.size
        self.metadata = {
            "width": width,
            "height": height,
            "format": self.pil_image.format,
            "channels": len(self.pil_image.getbands()),
            "file_size": len(self.contents)
        }
    
    async def _save_file(self):
        self.file_id = uuid.uuid4()
        file_extension = Path(self.file.filename).suffix
        self.storage_path = UPLOAD_DIR / f"{self.file_id}{file_extension}"
        
        # Actually write the file
        with open(self.storage_path, "wb") as f:
            f.write(self.contents)