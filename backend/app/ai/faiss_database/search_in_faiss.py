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
def multimodal_search(image_query, text_query, image_index, image_ids, alpha=0.2):
    """
    Perform late fusion search combining image and text similarity scores.
    :param image_query: Image input for similarity search.
    :param text_query: Text input for similarity search.
    :param alpha: Weight for combining similarities.
    :return: List of tuples (image_id, similarity_score, description)
    """

    # Ensure FAISS indexes are not empty
    if image_index.ntotal == 0:
        print("Warning: FAISS index is empty! Make sure embeddings are added before searching.")
        return []

    # Get embeddings for query and normalize them for cosine similarity
    image_embedding = normalize_embedding(get_image_embedding(image_query))
    text_embedding = normalize_embedding(get_text_embedding(text_query))

    # Perform FAISS search
    image_similarities, image_indices = image_index.search(image_embedding, k=10)  # Top-10 results
    text_similarities, text_indices = image_index.search(text_embedding, k=10)  # Top-10 results

    # Retrieve actual image IDs from FAISS indices
    retrieved_image_ids = [image_ids[idx] for idx in image_indices[0] if idx < len(image_ids)]
    retrieved_text_ids = [image_ids[idx] for idx in text_indices[0] if idx < len(image_ids)]

    # Merge image and text search results (Use UNION | instead of INTERSECTION &)
    all_ids = list(set(retrieved_image_ids) | set(retrieved_text_ids))

    # Store similarity scores (since FAISS already returns cosine similarity, no need for extra transformation)
    image_scores = {image_ids[idx]: max(0, image_similarities[0][i]) for i, idx in enumerate(image_indices[0]) if idx < len(image_ids)}
    text_scores = {image_ids[idx]: max(0, text_similarities[0][i]) for i, idx in enumerate(text_indices[0]) if idx < len(image_ids)}

    # Perform weighted fusion for all retrieved IDs
    fused_scores = {}
    for image_id in all_ids:
        image_sim = image_scores.get(image_id, 0)  # Default to 0 if missing
        text_sim = text_scores.get(image_id, 0)  # Default to 0 if missing
        fused_scores[image_id] = alpha * image_sim + (1 - alpha) * text_sim

    # Rank final results by highest similarity score
    sorted_results = sorted(fused_scores.items(), key=lambda item: item[1], reverse=True)
    
    # Limit to top-10 results
    sorted_results = sorted_results[:10]  # Add this line to enforce the limit
    
    # print("multimodal search", sorted_results)
    
    # Return only the image IDs (or modify to return whatever format you need)
    final_results = [(image_id) for image_id, _ in sorted_results]
    # print("multimodal image")
    return final_results  # Returns list of image_ids, limited to 10

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