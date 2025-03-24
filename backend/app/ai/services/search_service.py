import os,re,json,sys
import json
import re
import faiss

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from typing import List, Optional
from fastapi import Request, UploadFile

from ai.utills.chat_langchain import chatbot, image_match_with_text_prompt
from ai.faiss_database.search_in_faiss import search_using_text, multimodal_search
from ai.faiss_database.faiss_index import load_faiss_index, Image_databse_path
from ai.utills.metadata_dict import create_metadata_dict
from ai.utills.similar_images_descripton_tag import similar_images_description_tag
from ai.utills.extract_imagepath_fromJson import extract_image_paths
from ai.utills.generate_description import generate_description_with_retry
from ai.utills.metadata_dict import  load_metadata, create_metadata_dict
from ai.utills.similar_images_descripton_tag import similar_images_description_tag
from ai.utills.covert_to_localfile import convert_to_local_path
from ai.utills.chat_langchain import process_input_langchain,chatbot,image_match_with_text_prompt,similar_image_by_image_prompt,gallery_image_match_with_text_prompt,image_analysis_prompt
from ai.utills.upload_path import find_path_in_database
from ai.utills.call_llm import generate_query_answer,call_llm_with_prompt_image_text,call_llm_with_prompt_text
from ai.utills.chat_langchain import chatbot,basic_text_prompt
from ai.utills.generate_image_tag import generate_image_tag_with_retry
from ai.utills.find_image_in_database import find_image_in_database
from fastapi import FastAPI, UploadFile, File, Request, Form
from ai.faiss_database.search_in_faiss import search_using_text,search_using_image,multimodal_search
from ai.faiss_database.faiss_index import load_faiss_index
from ai.faiss_database.faiss_index import Image_databse_path

from ai.utills.metadata_dict import  load_metadata, create_metadata_dict
from ai.utills.similar_images_descripton_tag import similar_images_description_tag
from ai.config.setting import METADATA_FILE, UPLOAD_DIR
from dotenv import load_dotenv
load_dotenv()
UPLOAD_DIR = os.getenv("UPLOAD_DIR", default=os.path.join("data", "upload_images"))




#  Mount Static Files for Serving Images via HTTP
images_dir = r"data\upload_images"
# Example usage:
file_path = r"backend\app\ai\faiss_database\database\image_metadata.json"  # Replace with your JSON file path
async def search(
    request: Request,
    text: Optional[str],
    imageFiles: List[UploadFile],
    imagePaths: Optional[str]
):
   

    print("Starting /search processing...")
    form_data = await request.form()
    print("Raw form data:", form_data)
    print("Raw form data:", await request.form())
    print(f"Received request method: {request.method}")
    print(f"Received text: {text}")
    print(f"Received imageFiles count: {len(imageFiles)}")
    print(f"Received imagePaths: {imagePaths}")

    

    if not text and not imageFiles and not imagePaths:
        print("No text, images, or URLs provided")
        return {"text": "Please provide text or images", "images": []}

    response_text = ""
    response_images = []
    try:
        image_index = load_faiss_index(Image_databse_path)
        has_image_index = True
    except Exception as e:
        print(f"Error loading FAISS index: {str(e)}")
        has_image_index = False
   
    image_paths = extract_image_paths(file_path)
    metadata = []

    if os.path.exists(METADATA_FILE):
        try:
            with open(METADATA_FILE, "r") as f:
                metadata = json.load(f)
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {str(e)}")
        except Exception as e:
            print(f"Error loading metadata: {str(e)}")

    metadata_dictionay = create_metadata_dict(metadata)
    c = 0

    # Multimodal search: Text + Image
    if text and (imageFiles or imagePaths):
        if not has_image_index:
            response_text = "Image similarity search is currently unavailable, but I can still analyze your image and text."
        
        if imageFiles:
            for file in imageFiles:
                c=1
                print("image from file")
                print("-" * 50)
               
                temp_path = os.path.join(images_dir, file.filename)
                
                with open(temp_path, "wb") as f:
                    f.write(await file.read())
                               
                local_path=os.path.basename(temp_path)
                # print("TEMP LOCAL ",temp_path)
                # print("local file pathii: ",local_path)
                # print("-" * 50)
                temp_path= os.path.abspath(os.path.join(UPLOAD_DIR, local_path))
                # print("fTEMP LOCAL ",temp_path)
                 
                
                image_metatag=find_image_in_database(local_path, metadata_dictionay)
                # print("file path data: ",image_metatag)
                # print("-" * 50)
        elif imagePaths:
            c=2
            print("image from gallery")
            print("-" * 50)
            paths = json.loads(imagePaths)
           
            for path in paths:
                # print(f"Searching with gallery image: {path}")
                local_path=os.path.basename(path)
                # print("image local path: ",local_path)
                final_path2=os.path.abspath(os.path.join(UPLOAD_DIR, local_path))
                image_metatag=find_image_in_database(local_path, metadata_dictionay)        
            # print("final path: ",final_path2)        
       
        try:
            result=process_input_langchain(text)
            # print("Resultt: ",result)      

            if result == "image":
               
                print("Image found in database")                
                
                print("-" * 50)
                # print("c= ",c)
                if c==1 :
                     similar_images = multimodal_search( temp_path,text,image_index, image_paths, alpha=0.2)
                else: 
                    similar_images = multimodal_search( final_path2,text,image_index, image_paths, alpha=0.2)

               
                print("similar images uploaded files: ",similar_images)
               
                    
                # print("-" * 50)
                description_tag_list=similar_images_description_tag(metadata_dictionay,similar_images)                
                description_tag_json = json.dumps(description_tag_list)
                print("description_tag_json: ",description_tag_json)   
                print("-" * 50)          
            
                try:
                    # print("Prompt input variables: ", image_match_with_text_prompt.input_variables)
                    #print("Imported prompt template: ", image_match_prompt.template)
                    formatted_prompt =image_match_with_text_prompt.format(
                        image_data=description_tag_json,
                        user_query=text)  # Use text as the value
                    #print("Formatted prompt: ", formatted_prompt)
                except KeyError as e:
                    return f"Prompt formatting error: {str(e)} (check prompt variables)"
               
                except Exception as e:
                    return f"Unexpected error in messages creation: {str(e)} (traceback: {type(e).__name__})"
                # Step 4: Send to LLM and get response
                print("Searching for similar images using FAISS rext...")
                response_images,response_text=call_llm_with_prompt_image_text(formatted_prompt)  
                             
                    

            else:
                if image_metatag is not None:                             
                    found_image_metadata = json.dumps(image_metatag)
                    print("Image found in database" ,found_image_metadata)
                    # print("-" * 50)

                    # Prepare LLM prompt and messages
                    try:
                       
                        formatted_prompt = gallery_image_match_with_text_prompt.format(
                            user_query=text,
                            image_metadata=found_image_metadata
                        )
                       
                        #print("Formatted Prompt:\n", formatted_prompt)
                    except KeyError as e:
                        error_msg = f"Prompt formatting error: {str(e)} (check prompt variables)"
                        # print(error_msg)
                        return error_msg
                    except TypeError as e:
                        error_msg = f"Error with input data: {str(e)} (metadata = {found_image_metadata})"
                        # print(error_msg)
                        return error_msg
                    except Exception as e:
                        error_msg = f"Unexpected error creating messages: {str(e)} (type: {type(e).__name__})"
                        # print(error_msg)
                        return error_msg

                    # Send to LLM and process response
                    print("Analyzing image metadata with LLM...")
                    response_text=call_llm_with_prompt_text(formatted_prompt)
                    
                else:
                      ans=generate_query_answer(temp_path,text,image_analysis_prompt)
                    #   print("unknown image")
                      response_text+=ans
                    #   print("ans ",ans)                       


        except Exception as e:
            # print(f"Error in multimodal FAISS search: {str(e)}")
            response_text = f"Error in multimodal search: {str(e)}"
    
    elif text:

        print("Text search only", text)
        
        try:
            # print("Searching")
            result=process_input_langchain(text)
            print("Result: ",result)
           

            
            if result == "image":
                # print("Searching for similar images ")
                similar_images = search_using_text(text, image_index ,  image_paths, threshold=0.4, top_k=10)
                
                print("similar images in txt: ",similar_images)
                description_tag_list=similar_images_description_tag(metadata_dictionay,similar_images)
                # print("description_tag_list: ",description_tag_list)
                description_tag_json = json.dumps(description_tag_list)
               
               
                # print("text= ",text)
                # print("image data: ")
  
                try:
                    #print("Prompt input variables: ", image_match_with_text_prompt.input_variables)
                    #print("Imported prompt template: ", image_match_prompt.template)
                    formatted_prompt =image_match_with_text_prompt.format(
                        image_data=description_tag_json,
                        user_query=text)  # Use text as the value
                    #print("Formatted prompt: ", formatted_prompt)
                   
                except KeyError as e:
                    return f"Prompt formatting error: {str(e)} (check prompt variables)"
                
                except Exception as e:
                    return f"Unexpected error in messages creation: {str(e)} (traceback: {type(e).__name__})"
                # Step 4: Send to LLM and get response
                # print("Searching for similar images using FAISS rext...")
               
                response_images,response_text=call_llm_with_prompt_image_text(formatted_prompt) 

                # print("done")

            elif result == "text":
                print("Text found in database")
                formatted_prompt = basic_text_prompt.format(
                            input_text=text)
                user_message = f"{formatted_prompt}"
                response = chatbot.invoke(
                {"input": user_message},
                 config={"configurable": {"session_id": "default_session"}})
                print("Response from chatbot:", response)
                
       
            
            #    # Extract plain text
            #     json_str = response.strip().removeprefix("```json\n").rstrip("```")
            #     print("json_str: ",json_str)

            #     # Parse the JSON string into a Python dictionary
            #     response_dict = json.loads(json_str)
            #     print("response_dict: ",response_dict)

            #     # Extract the "answer" field
                response_text = response
                print("response_text: ",response_text)
            else:
                response_text = "I'm not sure what you mean. Want to chat or see images?"

           
        except Exception as e:
            # print(f"Error in FAISS search: {str(e)}")
            response_text = f"Error searching for '{text}': {str(e)}"
       

    
    
    return {"text": response_text, "images": response_images}
