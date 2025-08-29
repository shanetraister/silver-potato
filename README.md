# Another Image Processor

The purpose of this project is to learn and practice FastAPI, Celery, and SQLAlchemy. My goal is to build a simple photo processing app that starts with resizing, cropping, rotating, and converting colors and/or file types. Eventually I plan to build out other features like adding filters, beautification, and ML-based features like smart background removal and object detection.

## TODO
Phase 1:
- [X] Build database models (use SQLAlchemy)
    - [X] Image
    - [X] Job
    - [X] Session
- [X] File upload handling (local to start, then some cloud storage like S3)
- [X] Base FastAPI app with upload, jobs/job_id, and download/job_id endpoints
- [IP] Status tracking (pending, processing, completed, failed)

Phase 2:
- [ ] Build at least one image processor from (resize, crop, rotate, change color space, convert to file type)
- [ ] Add error handling for invalid images or parameters
- [ ] File cleanup logic (remove original file, ttl on processed file)

Phase 3:
- [ ] Redis connection for queues
- [ ] Celery configuration
- [ ] Move processing logic to Celery tasks
- [ ] Get job status updates from Celery tasks

Phase 4:
- [ ] Add the rest of the image processors (resize, crop, rotate, change color space, convert to file type)
- [ ] Add filters (blur, sharpen, etc...)

Phase 5:
- [ ] Build a Jinja2 HTML template for UI
- [ ] File upload form
- [ ] Results display page
- [ ] Job status polling with JavaScript

Phase 6 (ML features):
- [ ] Background removal
- [ ] NSFW detection
- [ ] Face detection
- [ ] Object detection
- [ ] Smart redaction/face bluring
- [ ] Model caching
- [ ] GPU/CPU worker separations