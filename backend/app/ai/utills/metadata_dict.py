import json
import os
# Load JSON file
def load_metadata(json_file=r"backend\app\ai\faiss_database\database\image_metadata.json"):
    # Check if file exists and is not empty
    if not os.path.exists(json_file) or os.stat(json_file).st_size == 0:
        print(" Warning: Metadata file is missing or empty. Returning an empty list.")
        return []  # Return an empty list instead of crashing

    try:
        with open(json_file, "r", encoding="utf-8") as f:
            return json.load(f)  # Load JSON
    except json.JSONDecodeError:
        print(" Error: JSON file is corrupted or empty. Returning an empty list.")
        return []  # Return empty list if JSON is invalid
# Convert list to a dictionary for fast lookup
def create_metadata_dict(data):
    return {item["image_ids"]: {"description": item["image_descriptions"],"tag": item["image_tags"] } for item in data}

# Function to get metadata by image path
def get_metadata_by_image_path(image_path, metadata_dict):
    return metadata_dict.get(image_path, None)  # Returns None if not found

# Load and process metadata
data = load_metadata()
metadata_dictionay = create_metadata_dict(data)
# Loop through the dictionary
