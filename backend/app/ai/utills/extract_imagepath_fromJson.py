import json

def extract_image_paths(json_file_path):
    """
    Extracts all image paths from a JSON file and returns them in a list.

    Args:
        json_file_path: The path to the JSON file.

    Returns:
        A list of image paths, or an empty list if there are no image paths 
        or if there's an error reading the file.  Returns None if the JSON
        is invalid.
    """
    try:
        with open(json_file_path, 'r', encoding='utf-8') as f: # Handle potential encoding issues
            data = json.load(f)

        image_paths = []
        if isinstance(data, list): # Check if the JSON data is a list of objects
            for item in data:
                if isinstance(item, dict) and "image_ids" in item:  # Check if it's a dictionary and contains image_ids
                    image_paths.append(item["image_ids"])
        elif isinstance(data, dict): # Handle the case where the JSON data is a single object
            if "image_ids" in data:
                image_paths.append(data["image_ids"])
            # If the dict contains a list of objects under a key, loop over it
            for key, value in data.items():
                if isinstance(value, list):
                    for item in value:
                        if isinstance(item, dict) and "image_ids" in item:
                            image_paths.append(item["image_ids"])
        else: # If it is not a list or dict, it is invalid
            return None

        return image_paths

    except FileNotFoundError:
        print(f"Error: File not found at {json_file_path}")
        return []
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in {json_file_path}")
        return None
    except Exception as e: # Catch other potential errors like UnicodeDecodeError
        print(f"An error occurred: {e}")
        return []
    

def extract_description_list(json_file_path):
    """
    Extracts all image paths from a JSON file and returns them in a list.

    Args:
        json_file_path: The path to the JSON file.

    Returns:
        A list of image paths, or an empty list if there are no image paths 
        or if there's an error reading the file.  Returns None if the JSON
        is invalid.
    """
    try:
        with open(json_file_path, 'r', encoding='utf-8') as f: # Handle potential encoding issues
            data = json.load(f)

        image_paths = []
        if isinstance(data, list): # Check if the JSON data is a list of objects
            for item in data:
                if isinstance(item, dict) and "image_descriptions" in item:  # Check if it's a dictionary and contains image_ids
                    image_paths.append(item["image_descriptions"])
        elif isinstance(data, dict): # Handle the case where the JSON data is a single object
            if "image_ids" in data:
                image_paths.append(data["image_descriptions"])
            # If the dict contains a list of objects under a key, loop over it
            for key, value in data.items():
                if isinstance(value, list):
                    for item in value:
                        if isinstance(item, dict) and "image_descriptions" in item:
                            image_paths.append(item["image_descriptions"])
        else: # If it is not a list or dict, it is invalid
            return None

        return image_paths

    except FileNotFoundError:
        print(f"Error: File not found at {json_file_path}")
        return []
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in {json_file_path}")
        return None
    except Exception as e: # Catch other potential errors like UnicodeDecodeError
        print(f"An error occurred: {e}")
        return []




