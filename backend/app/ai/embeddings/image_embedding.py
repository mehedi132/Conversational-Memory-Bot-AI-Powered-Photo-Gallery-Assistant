import sys
import os

# Adjust this path as needed
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))) 

import torch
import requests
import time
from io import BytesIO

import numpy as np
from PIL import Image
from ai.models.CLIP_model import model, processor
images_dir = r"Data\upload_images"

def get_image_embedding(image_path_or_url: str) -> torch.Tensor:
    # Handle both local paths and URLs
    if image_path_or_url.startswith("http://localhost:8000/images/"):
        # Convert URL to local path
        filename = image_path_or_url.split("/")[-1]
        local_path = os.path.join(images_dir, filename)
        if os.path.exists(local_path):
            # print(f"Using local file: {local_path}")
            image = Image.open(local_path).convert("RGB")
        else:
            # print(f"Fetching image from URL: {image_path_or_url}")
            response = requests.get(image_path_or_url, timeout=60)
            image = Image.open(BytesIO(response.content)).convert("RGB")
    else:
        image = Image.open(image_path_or_url).convert("RGB")
    embed_start = time.time()
    inputs = processor(images=image, return_tensors="pt")
    with torch.no_grad():
        embedding = model.get_image_features(**inputs)
    # print(f"Embedding generated in {time.time() - embed_start:.2f} seconds")
    return embedding.numpy().astype("float32") 

