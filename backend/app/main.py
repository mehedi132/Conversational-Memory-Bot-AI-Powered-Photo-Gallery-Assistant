import os
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from ai.config.setting import CORS_ORIGINS, UPLOAD_DIR, IMAGES_DIR
from routes.image_route import router as image_router
from routes.upload_route import router as upload_router
from routes.search_route import router as search_router

# Set environment variable
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

# FastAPI app setup
app = FastAPI()

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/images", StaticFiles(directory=UPLOAD_DIR), name="images")
app.mount("/uploads", StaticFiles(directory=IMAGES_DIR), name="uploads")

# Include API routes
app.include_router(image_router)
app.include_router(upload_router)
app.include_router(search_router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)