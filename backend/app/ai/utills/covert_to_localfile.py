
import os

# Define the base directory


# Base directory
BASE_DIR = os.path.join( "data", "upload_images")
def convert_to_local_path(url):
    """
    Convert a URL to a local file path and check if it exists in the dictionary.
    Returns the local path if found, None if not.
    """
    # Extract the filename from the URL
    filename = os.path.basename(url)  # e.g., "1740617503135-pexels-elgiganto-978629.jpg"
    # Construct the full local path
    local_path = os.path.join(BASE_DIR, filename).replace("/", "\\")  # Ensure Windows-style slashes
    # Check if it exists in the dictionary
    print("i m local ",local_path)
  
    return local_path 


print("hi")