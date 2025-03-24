
import time
import google.generativeai as genai
import os,sys
from PIL import Image
from tenacity import retry, stop_after_attempt, wait_exponential



# Adjust this path as needed
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))) 
from ai.utills.generate_description import data_path



# Function to load API key from config file
def load_api_key():
    config_path = data_path  # Adjust if needed
    try:
        with open(config_path, "r") as file:
            return file.read().strip()
    except FileNotFoundError:
        raise FileNotFoundError(f"API key file not found at {config_path}. Please create it.")

# Load API Key
API_KEY = load_api_key()

# Configure Gemini API
genai.configure(api_key=API_KEY)

# Initialize the model
modeltag = genai.GenerativeModel('gemini-2.0-flash')




#  Retry mechanism with exponential backoff


def generate_image_tag(image_path: str):
    """
    Generate a clean list of tags from an image using Gemini API, handling various response formats.
    
    Args:
        image_path (str): Path to the image file
        
    Returns:
        List[str]: Clean list of extracted tags
    """
    try:
        # Open the image
        with Image.open(image_path) as img:
            # Generate Image Caption & Objects using Gemini
            prompt = ("List specific objects, colors, and key scene elements in the image. "
                     "Return only tags, one per line, no extra text.")
            response = modeltag .generate_content([prompt, img])

            # Check for response and process tags
            if response and hasattr(response, "text") and response.text:
                # Split the response into lines
                lines = response.text.split("\n")
                clean_tags = []
                
                # If we only get an intro line, try to parse the description directly
                if len(lines) <= 1 or "Here's" in lines[0]:
                    # Fallback: extract tags from a single descriptive paragraph
                    description = response.text.replace("Here's a breakdown of the image:", "").replace("Here's an analysis of the image:", "").strip()
                  
                    
                else:
                    # Normal processing for structured response
                    in_descriptive_section = False
                    
                    for line in lines:
                        line = line.strip().replace('*', '').strip()
                        if not line:
                            continue
                        
                        if line.startswith(('Objects:', 'Scene:', 'Dominant Colors:', 
                                          'Year:', 'Location:')):
                            in_descriptive_section = True if line in ['Scene:', 'Year:', 'Location:'] else False
                            continue
                        
                        if in_descriptive_section:
                            if not line.startswith(('The ', 'It ', 'Impossible')) and len(line.split()) <= 5:
                                clean_tags.append(line)
                        else:
                            clean_tags.append(line)
                
                return clean_tags if clean_tags else ["No meaningful tags extracted"]
            else:
                return ["Unknown Tags"]

    except FileNotFoundError:
        return ["Error: Image file not found"]
    except Exception as e:
        return [f"Error: {str(e)}"]



def generate_image_tag_with_retry(image_path, retries=5, backoff_factor=1):
    for attempt in range(retries):
        try:
            return generate_image_tag(image_path)
        except Exception as e:
            if "429" in str(e):
                wait_time = backoff_factor * (2 ** attempt)
                print(f"Rate limit exceeded. Retrying in {wait_time} seconds...")
                time.sleep(wait_time)
            else:
                raise e
    raise Exception("Failed to generate image tag after multiple retries")