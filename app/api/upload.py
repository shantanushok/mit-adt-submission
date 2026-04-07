from fastapi import APIRouter, UploadFile, File, HTTPException
import base64
import logging

try:
    from app.services.imagekit_service import imagekit_client
except ImportError:
    imagekit_client = None

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/images", response_description="Upload an image to ImageKit")
async def upload_image(file: UploadFile = File(...)):
    if not imagekit_client:
        raise HTTPException(status_code=500, detail="ImageKit is not configured.")
    
    try:
        contents = await file.read()
        encoded_file = base64.b64encode(contents).decode("utf-8")
        
        # Uploading via ImageKit Python SDK
        upload_info = imagekit_client.upload(
            file=encoded_file,
            file_name=file.filename,
            options={
                "folder": "/amd_uploads/",
                "is_private_file": False,
                "use_unique_file_name": True
            }
        )
        return {"status": "success", "url": upload_info.url, "file_id": upload_info.file_id}
    except Exception as e:
        logger.error(f"Image upload failed: {e}")
        raise HTTPException(status_code=500, detail="Failed to upload image")
