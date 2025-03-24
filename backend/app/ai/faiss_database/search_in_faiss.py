#multimodal Search
import sys
import os
import torch

# Adjust this path as needed
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))) 

from torch.nn.functional import cosine_similarity

from ai.embeddings.image_embedding import get_image_embedding
from ai.embeddings.text_embedding import get_text_embedding
from ai.faiss_database.faiss_index import normalize_embedding
# from ai.faiss_database.faiss_index import  image_ids,normalize_embedding

def search_using_text(query, faiss_index, image_ids, threshold=0.85, top_k=5):
    # Step 1: Generate embedding for the query
    query_embedding = get_text_embedding(query)  # Get the embedding as a PyTorch tensor
    query_embedding = normalize_embedding(query_embedding)  # Normalize the embedding

    # Ensure query_embedding is a PyTorch tensor
    if not isinstance(query_embedding, torch.Tensor):
        query_embedding = torch.tensor(query_embedding)

    # Step 2: Retrieve top N similar images from the index
    D, I = faiss_index.search(query_embedding.detach().numpy(), k=top_k)  # Get top_k results

    # Step 3: Calculate cosine similarity for each image and filter based on threshold
    similar_images = []
    for idx in range(len(I[0])):
        # Get the actual image path using the returned index from FAISS
        image_path = image_ids[I[0][idx]]       
        similar_images.append((image_path))

    # Sort results by similarity (descending order)

    #print("search_using_text",similar_images)

    return similar_images



def search_using_image(image_path, faiss_index, image_ids, threshold=0.4, top_k=10):
    # Step 1: Generate embedding for the query
    image_embedding = normalize_embedding(get_image_embedding(image_path))
    
    # Step 2: Retrieve top N similar images from the index
    D, I = faiss_index.search(image_embedding, k=top_k)  # Get top_k results

    # Step 3: Calculate cosine similarity for each image and filter based on threshold
    similar_images = []
    
    for idx in range(len(I[0])):
        # Get the actual image path using the returned index from FAISS
        image_path = image_ids[I[0][idx]]       
        similar_images.append((image_path))
    return similar_images


# print ("imageID: ",image_ids)