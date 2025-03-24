
import os,re,json,sys


import google.generativeai as genai

from PIL import Image
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from ai.utills.chat_langchain import chatbot
from dotenv import load_dotenv
# Get the current directory of this file (image_embedding.py)
current_dir = os.path.dirname(os.path.abspath(__file__))

# Move up TWO levels to reach the project root
project_root = os.path.abspath(os.path.join(current_dir, ".."))


# Construct the path to "data/upload images/"
data_path = os.path.join(project_root, "config", "api_key.txt")

# Load environment variables from .env file
load_dotenv()
# Function to load API key from config file
def load_api_key():
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        raise ValueError("GEMINI_API_KEY not found in environment variables. Please add it to your .env file.")
    return api_key

# Load API Key
API_KEY = load_api_key()

# Configure Gemini API
genai.configure(api_key=API_KEY)

# Initialize the model
modelg = genai.GenerativeModel('gemini-2.0-flash')

response_text = ""
response_images = []


def generate_query_answer(image_path: str, user_query: str,prompt: str) -> str:
    try:
        # Open the image
        absolute_path = os.path.abspath(image_path)
        img = Image.open(absolute_path)
        # print("Generating description for image with query:", user_query)
        
        # Format the prompt with the user query
        formatted_prompt = prompt.format(user_query=user_query)
        
        # Generate description using Gemini
        response = modelg.generate_content([formatted_prompt, img])
        
        # Return the generated description
        return response.text if response else "No response from API."
    
    except FileNotFoundError:
        return "Error: Image file not found."
    except Exception as e:
        return f"Error: {str(e)}. Unable to analyze the image fully, so no detailed description or answer can be provided. Please ensure the image is valid and try again."




def call_llm_with_prompt_image_text(formatted_prompt):
    try:
        user_message = f"{formatted_prompt}"       
        # Invoke the chatbot with the formatted prompt
        match_response = chatbot.invoke(
            {"input": user_message},
            config={"configurable": {"session_id": "default_session"}}
        )

        # Debugging prints
        # print("\nResponse from chatbot:", match_response)
        # print("\nResponse type:", type(match_response))
        # print("\n")

        # Since match_response is a string (from StrOutputParser), use it directly as raw_response
        raw_response = match_response

        # Use regex to extract the JSON part from the response
        json_match = re.search(r'\{.*\}', raw_response, re.DOTALL)
        if json_match:
            json_str = json_match.group(0)

            try:
                # Parse the JSON string into a dictionary
                output_data = json.loads(json_str)
            except json.JSONDecodeError:
                return [], "Error: Invalid JSON response in LLM output."
            
            # Ensure values are not None
            matched_images = output_data.get("matched_images", [])  # Ensure it's a list
            summary = output_data.get("summary", "")

            print("Matched images:", matched_images)
            print("Summary:", summary)

            # Initialize response_text
            response_text = summary

            # Construct image URLs safely
            response_images = [f"http://localhost:8000/images/{os.path.basename(path)}" for path in matched_images]

            return response_images, response_text  # Returns 2 values: list of URLs and a string

        else:
            response_images = []
            response_text = "No image found."
            # print("No valid JSON found in response.")
            return response_images, response_text  # Returns 2 values: empty list and a string

    except json.JSONDecodeError as e:
        # Fallback if JSON parsing fails entirely
        print(f"JSON parsing failed: {str(e)}. Falling back to no-match response.")
        return [], "No image found."  # Returns 2 values: empty list and a string
    except Exception as e:
        # General error fallback
        print(f"Error processing LLM response: {str(e)}")
        return [], f"Error processing LLM response: {str(e)}"  # Returns 2 values: empty list and a string
def call_llm_with_prompt_text(formatted_prompt):
    try:
        response_text = ""
        user_message = f"{formatted_prompt}"
        match_response = chatbot.invoke({"input": user_message}, 
                         config={"configurable": {"session_id": "default_session"}}
        )
        # print("llm res ", match_response)
        # Check the structure of match_response
        #print("Response type:", type(match_response))
        # print("\n")
        # print("\n")

        # Get the raw LLM response string from the dictionary.
        raw_response = match_response
        json_match = re.search(r'\{.*\}', raw_response, re.DOTALL)
        if json_match:
            json_str = json_match.group(0)
            # Parse the JSON string into a Python dictionary
            data = json.loads(json_str)
            response_text+=data.get("answer")
            
        else:
            print("No valid JSON found.")
        
        print("\n" * 2)
        return response_text           


    except json.JSONDecodeError as e:
        print(f"JSON parsing failed: {str(e)}. Using fallback response.")
        return {"answer": "Failed to parse LLM response; no valid answer available."}
    except Exception as e:
        error_msg = f"Error processing LLM response: {str(e)}"
        print(error_msg)
        return error_msg

    
# print("hii")

