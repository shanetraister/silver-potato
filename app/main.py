from fastapi import FastAPI, File, UploadFile, BackgroundTasks
from shared.file_handler import UploadHandler
from shared.storage import create_image_record, create_job_record
from app.models import Image, Job
from fastapi.responses import FileResponse
from fastapi import HTTPException
import os

app = FastAPI()

# Start with just these endpoints in main.py
@app.post("/upload")  # Just save file, return job_id
async def upload(file: UploadFile = File(...)):
    
    handler = UploadHandler(file)
    file_metadata = await handler.process()

    image = create_image_record(file_metadata)
    # now I need to return good html right?
    return {"image_id": image.id}

@app.post("/process/{image_id}")
async def process(image_id, request_data: dict):
    # validate image exists
    img = Image.get(image_id)
    processor = request_data.get("processor")
    params = request_data.get("params")
    if not img:
        raise HTTPException(status_code=404, detail="Image not found")
    if not os.path.exists(img.storage_path):
        raise HTTPException(status_code=404, detail="Image file not found")
    
    # validate processor exists
    if processor not in ["resize", "crop", "rotate", "convert"]:
        raise HTTPException(status_code=400, detail="Invalid processor")
    
    # validate params (we'll do this later. Use a dict with keys of processor and values of processor reqd params)
    # pseudo code
    # reqd_params = REQ_PARAMS.get(processor)
    # if not all(key in params for key in reqd_params):
    #     raise HTTPException(status_code=400, detail="Missing required parameters")
    # create job record with status = pending
    # since those all passed at this point, let's create the job and return job_id
    job = create_job_record(image_id, processor, params)

    return {"job_id": job.id, "status": job.status}

@app.get("/jobs/{job_id}")  # Return job status
async def get_job_status(job_id):
    job = Job.get(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return {"job_id": job.id, "status": job.status}

@app.get("/download/{job_id}")  # Serve processed file
async def download(job_id):
    job = Job.get(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    if not job.output_image:
        raise HTTPException(status_code=400, detail="Job has not been completed")
    if not os.path.exists(job.output_image.storage_path):
        raise HTTPException(status_code=404, detail="Processed file not found")
    return FileResponse(job.output_image.storage_path)
