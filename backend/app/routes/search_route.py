import os,re,json,sys
from fastapi import APIRouter, UploadFile, File
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from fastapi import APIRouter, Request, Form, UploadFile, File
from typing import List, Optional
from ai.services.search_service import search

router = APIRouter(prefix="/api", tags=["search"])

@router.post("/search")
async def search_endpoint(
    request: Request,
    text: Optional[str] = Form(None),
    imageFiles: List[UploadFile] = File(default=[]),
    imagePaths: Optional[str] = Form(None),
):
    return await search(request, text, imageFiles, imagePaths)