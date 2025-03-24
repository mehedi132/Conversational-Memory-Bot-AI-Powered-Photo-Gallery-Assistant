import os,re,json,sys
from fastapi import APIRouter, UploadFile, File
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from ai.services.image_upload_service import  process_images
from pydantic import BaseModel
from typing import List

router = APIRouter(prefix="/api", tags=["images"])

class ImageResponse(BaseModel):
    id: str
    src: str
    description: str | None
    tags: List[str] | None

@router.post("/process-image/")
async def process_upload_image(file: UploadFile = File(...)):
    # return {"message": "Image processed successfully"}
     return await process_images(file)