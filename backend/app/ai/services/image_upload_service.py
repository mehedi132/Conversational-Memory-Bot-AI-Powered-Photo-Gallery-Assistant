import os,re,json,sys

import json
import shutil
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from fastapi import HTTPException, UploadFile
from dotenv import load_dotenv
from ai.embeddings.image_embedding import get_image_embedding
from ai.embeddings.text_embedding import get_text_embedding
from ai.utills.generate_description import generate_description_with_retry
from ai.utills.generate_image_tag import generate_image_tag_with_retry
from ai.faiss_database.faiss_index import store_image_embedding
from ai.config.setting import METADATA_FILE, UPLOAD_DIR

load_dotenv()

# Get the directory containing the current script (project root)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Define paths relative to the project root, with environment variable overrides
UPLOAD_DIR = os.getenv("UPLOAD_DIR", default=os.path.join("data", "upload_images"))
METADATA_FILE = os.getenv("METADATA_FILE", default=os.path.join( "backend", "app", "ai", "faiss_database", "database", "image_metadata.json"))

# Normalize paths to use forward slashes for consistency
UPLOAD_DIR = UPLOAD_DIR.replace("\\", "/")
METADATA_FILE = METADATA_FILE.replace("\\", "/")

# Ensure directories exist
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(os.path.dirname(METADATA_FILE), exist_ok=True)


async def process_images(file: UploadFile):
    try:
        print("Received Filename:", file.filename)

        # Extract original filename
        match = re.search(r'(\d+)-(.*)', file.filename)
        if match:
            original_filename = match.group(2)
        else:
            original_filename = file.filename
        print("Original Filename (parsed):", original_filename)

        # Handle duplicates with a counter
        base_name, ext = os.path.splitext(original_filename)
        counter = 0
        file_path = os.path.abspath(os.path.join(UPLOAD_DIR, original_filename))
        while os.path.exists(file_path):
            counter += 1
            file_path = os.path.abspath(os.path.join(UPLOAD_DIR, f"{base_name}_{counter}{ext}"))

        print("File path:", file_path)
        relative_file_path = os.path.relpath(file_path, UPLOAD_DIR)

        # Save the file
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        if not os.path.exists(file_path):
            raise HTTPException(status_code=500, detail="File saving failed!")
        print("File saved at:", file_path)

        # Generate embeddings, description, tags (placeholders)
        embeddings = get_image_embedding(file_path)
        description = generate_description_with_retry(file_path)
        print("Description generated:", description)
        text_embeddings = get_text_embedding(description)
        tags = generate_image_tag_with_retry(file_path)

        # Store embeddings
        store_image_embedding(file_path, embeddings)

        # Prepare metadata
        image_metadata = {
            "image_ids": relative_file_path,
            "image_descriptions": description,
            "image_tags": tags
        }
        print("Generated Metadata:", image_metadata)

        # Update metadata JSON
        metadata = []
        if os.path.exists(METADATA_FILE):
            try:
                with open(METADATA_FILE, "r") as f:
                    metadata = json.load(f)
                    if not isinstance(metadata, list):
                        metadata = [metadata]
            except json.JSONDecodeError:
                metadata = []

        metadata.append(image_metadata)
        with open(METADATA_FILE, "w") as f:
            json.dump(metadata, f, indent=2)
            print("Metadata updated successfully!")

        return {
            "message": "Image processed successfully",
            "image_metadata": image_metadata
        }

    except Exception as e:
        print("Error processing image:", str(e))
        raise HTTPException(status_code=500, detail=str(e))


# async def  process_images(file: UploadFile):
#     try:
#         #  Generate full absolute path for the image
#         print("File:", file.filename)  # ✅ Debugging print
#         file_path = os.path.abspath(os.path.join(UPLOAD_DIR, file.filename))
#         print("File path:", file_path)  # ✅ Debugging print    
#         # Generate relative path for metadata (relative to UPLOAD_DIR)
#         relative_file_path = os.path.relpath(file_path, UPLOAD_DIR)

#         #  Save the uploaded image
#         with open(file_path, "wb") as buffer:
#             shutil.copyfileobj(file.file, buffer)

#         #  Check if file was actually saved
#         if not os.path.exists(file_path):
#             raise HTTPException(status_code=500, detail="File saving failed!")

#         print("File saved at:", file_path)  # ✅ Debugging print

#         #  Generate embeddings, description, and tags
#         try:
#             embeddings = get_image_embedding(file_path)

#         except Exception as e:
#             raise HTTPException(status_code=500, detail=f"Embedding generation failed: {str(e)}")

#         try:
#             description = generate_description_with_retry(file_path)
#             print("Description generated:", file_path)  # ✅ Debugging print
#             text_embeddings = get_text_embedding(description)
#         except Exception as e:
#             raise HTTPException(status_code=500, detail=f"Description generation failed: {str(e)}")

#         try:
#             tags = generate_image_tag_with_retry(file_path)
#         except Exception as e:
#             raise HTTPException(status_code=500, detail=f"Tag generation failed: {str(e)}")

#         #  Store embeddings in FAISS
#         try:
#             store_image_embedding(file_path, embeddings)
           
#         except Exception as e:
#             raise HTTPException(status_code=500, detail=f"Storing embedding failed: {str(e)}")

#         #  Prepare metadata
#         image_metadata = {
#             "image_ids": relative_file_path,
#             "image_descriptions": description,
#             "image_tags": tags
#         }

#         print("Generated Metadata:", image_metadata)  #  Debugging print

#         #  Read and Update Metadata JSON File
#         metadata = []

#         if os.path.exists(METADATA_FILE):
#             try:
#                 with open(METADATA_FILE, "r") as f:
#                     metadata = json.load(f)
#                     if not isinstance(metadata, list):  #  Fix: Convert dict to list
#                         metadata = [metadata]
#             except json.JSONDecodeError:
#                 metadata = []  # Reset if JSON is invalid

#         #  Append new metadata correctly
#         if isinstance(metadata, list):
#             metadata.append(image_metadata)  #  Append if it's a list
#         else:
#             metadata = [metadata, image_metadata]  #  Convert to list if it's a dict

#         #  Save updated metadata
#         try:
#             with open(METADATA_FILE, "w") as f:
#                 json.dump(metadata, f, indent=2)
#                 print("Metadata updated successfullyyyy!")
#         except Exception as e:
#             raise HTTPException(status_code=500, detail=f"Metadata saving failed: {str(e)}")

#         print("Metadata updated successfully!")  #  Debugging print

#         return {
#             "message": "Image processed successfully",
#             "image_metadata": image_metadata
#         }

#     except Exception as e:
#         print("Error processing image:", str(e))  #  Debugging error message
#         raise HTTPException(status_code=500, detail=str(e))