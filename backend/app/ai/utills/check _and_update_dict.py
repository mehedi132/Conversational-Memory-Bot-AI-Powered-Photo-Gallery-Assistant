import os
import time
import json

last_modified = 0


image_dict = {}
def check_and_update_dict(file_path):
    """Reload dictionary if JSON file has changed."""
    global image_dict, last_modified
    current_modified = os.path.getmtime(file_path)
    if current_modified > last_modified:
        with open(file_path, 'r') as file:
            data = json.load(file)
        image_dict = {item["image_ids"]: {"tag": item["image_tags"], "description": item["image_descriptions"]} for item in data}

        last_modified = current_modified
    return image_dict