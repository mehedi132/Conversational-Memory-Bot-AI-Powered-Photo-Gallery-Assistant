import os,re,json,sys
import json
import re
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
import json
from fastapi import HTTPException
from ai.config.setting import METADATA_FILE, UPLOAD_DIR
from ai.utills.metadata_dict import create_metadata_dict

async def get_images_metadata():
    try:
        if os.path.exists(METADATA_FILE):
            with open(METADATA_FILE, "r") as f:
                metadata = json.load(f)
                metadata_dict = create_metadata_dict(metadata)
        else:
            return []

        metadata = dict(reversed(list(metadata_dict.items())))
        images = []
        for file_path, details in metadata.items():
            filename = os.path.basename(file_path)
            src = f"/images/{filename}"
            description = details['description']
            tag_value = details['tag']
            
            if isinstance(tag_value, str):
                tags = tag_value.split(",") if tag_value else []
            elif isinstance(tag_value, list):
                tags = tag_value
            else:
                tags = []
                
            images.append({
                "id": filename,
                "src": src,
                "description": description,
                "tags": tags
            })
        return images
    except json.JSONDecodeError as e:
        raise HTTPException(status_code=500, detail=f"Error decoding JSON: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading metadata: {str(e)}")