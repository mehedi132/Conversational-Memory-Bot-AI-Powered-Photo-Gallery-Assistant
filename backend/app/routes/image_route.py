import os,re,json,sys
from fastapi import APIRouter, UploadFile, File
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import aiofiles
from fastapi import APIRouter, Response
from typing import List
from ai.config.setting import IMAGES_DIR
from ai.models.model import ImageResponse
from ai.services.image_service import get_images_metadata

router = APIRouter(prefix="/api", tags=["images"])

@router.get("/images/{filename}")
async def serve_image(filename: str):
    file_path = os.path.join(IMAGES_DIR, filename)
    if not os.path.exists(file_path):
        return {"error": "Image not found"}, 404
    
    async with aiofiles.open(file_path, "rb") as f:
        content = await f.read()
    
    return Response(
        content=content,
        media_type="image/jpeg",
        headers={
            "Access-Control-Allow-Origin": "http://localhost:3000",
            "Access-Control-Allow-Methods": "GET",
            "Access-Control-Allow-Headers": "*",
        }
    )

@router.get("/images", response_model=List[ImageResponse])
async def get_images():
    return await get_images_metadata()