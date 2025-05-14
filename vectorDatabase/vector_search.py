from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient,models
import os
from dotenv import load_dotenv



load_dotenv()

MODEL_EMBEDDING=os.getenv("MODEL_EMBEDDING")
qdrant_url = os.getenv("qdrant_url")
qdrant_apikey = os.getenv("qdrant_apikey")
GEMINI_API_LIST = os.getenv("GEMINI_API_LIST")
GEMINI_MODEL = os.getenv("GEMINI_MODEL")



def description_search(query:str, collection_name:str, top_k:int):
    model = SentenceTransformer(MODEL_EMBEDDING)
    query_vector = model.encode(query)
    client = QdrantClient(url=qdrant_url, api_key=qdrant_apikey)
    search_results = client.search(
    collection_name=collection_name,
    query_vector=query_vector,
    limit=top_k,
    )
    return search_results

def top_image(query:str, collection_name:str,top_k:int):
    search_results= description_search(query,collection_name,top_k)
    return search_results