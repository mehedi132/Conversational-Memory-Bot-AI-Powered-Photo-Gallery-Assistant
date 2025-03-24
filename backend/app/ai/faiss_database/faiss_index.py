import sys
import os
import json
# Get the current directory of this file (image_embedding.py)
current_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the path to "data/upload images/"
Image_databse_path = os.path.join(current_dir,  "database","image_faiss_index.faiss")
Text_databse_path = os.path.join(current_dir,  "database","text_faiss_index.faiss")
Tag_databse_path = os.path.join(current_dir,  "database","tag_faiss_index.faiss")
METADATA_PATH = os.path.join(current_dir,  "database","image_metadata.json")


UPLOAD_DIR = os.path.join(os.getcwd(), '../../Data/upload_images')

import faiss
import numpy as np
dimension = 1024  # CLIP embeddings are 1024-dimensional for laion/CLIP-ViT-H-14-laion2B-s32B-b79K




image_index = faiss.IndexFlatIP(dimension)  # L2 distance for image embeddings
text_index = faiss.IndexFlatIP(dimension)  # L2 distance for text embeddings
tag_index = faiss.IndexFlatIP(dimension)
# print(type(image_index.ntotal))
# Store image embeddings and their IDs
image_embeddings = []
image_ids = []
text_embeddings = []
text_ids = []
image_descriptions = {}
global image_tags
image_tags = {}
tag_embeddings = []
tag_ids = []


def normalize_embedding(embedding):
    """ Normalize embedding to unit length for cosine similarity """
    return embedding / np.linalg.norm(embedding)

def store_image_embedding(image_id, embedding,):

    image_embeddings.append(embedding)
    image_ids.append(image_id)
    print ("store in id: ", image_ids)
    embedding=normalize_embedding(embedding)   
    image_index.add(embedding)  # Add to FAISS 
    os.makedirs(os.path.dirname(Image_databse_path), exist_ok=True)
    faiss.write_index(image_index, Image_databse_path)
    #save_metadata()

def save_metadata():
    metadata = {
        "image_ids": image_ids,
        "image_descriptions": image_descriptions,
        "image_tags": image_tags
    }
    
    with open(METADATA_PATH, "w") as f:
        json.dump(metadata, f)





def store_text_embedding(image_id, embedding):

    text_embeddings.append(embedding)
    text_ids.append(image_id)
    embedding=normalize_embedding(embedding)
    text_index.add(embedding)  # Add to FAISS
    os.makedirs(os.path.dirname(Text_databse_path), exist_ok=True)
    faiss.write_index(text_index, Text_databse_path)


def store_tag_embedding(image_id, embedding):

    tag_embeddings.append(embedding)
    tag_ids.append(image_id)
    embedding=normalize_embedding(embedding)
    tag_index.add(embedding)  # Add to FAISS
    os.makedirs(os.path.dirname(Tag_databse_path), exist_ok=True)
    faiss.write_index(tag_index, Tag_databse_path)

def load_faiss_index(index_path):
    """Load FAISS index"""
    if os.path.exists(index_path):
            return faiss.read_index(index_path)
    else:
            print(f"Index file not found at {index_path}. Creating new index...")

def load_metadata():
    if os.path.exists(METADATA_PATH):  #  Check if metadata file exists
        try:
            with open(METADATA_PATH, "r") as f:
                metadata = json.load(f)
                
                #  Clear existing data to avoid duplication
                image_ids.clear()
                image_descriptions.clear()
                image_tags.clear()

                #  Iterate over the list and extract values
                for item in metadata:
                    # Check if keys exist and append/update accordingly
                    if "image_ids" in item:
                        image_ids.append(item["image_ids"])
                    
                    if "image_descriptions" in item:
                        image_descriptions[item["image_ids"]] = item["image_descriptions"]
                    
                    if "image_tags" in item:
                        image_tags[item["image_ids"]] = item["image_tags"]

                # print("Metadata loaded successfully!")  #  Debugging print

        except FileNotFoundError:
            print("Metadata file not found. Skipping loading step.")
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {str(e)}")
        except Exception as e:
            print(f"Error loading metadata: {str(e)}")
    # else:
    #     # print("Metadata file does not exist.")

#print("faiss")


