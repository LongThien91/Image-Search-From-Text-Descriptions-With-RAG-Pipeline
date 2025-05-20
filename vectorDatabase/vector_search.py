from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient,models
import os
from dotenv import load_dotenv
from LLM.Top_Query_matches import CheckQuerySimilar
from LLM.api_list_manager import APIKeyManager



load_dotenv()

MODEL_EMBEDDING=os.getenv("MODEL_EMBEDDING")
qdrant_url = os.getenv("qdrant_url")
qdrant_apikey = os.getenv("qdrant_apikey")
GEMINI_API_LIST = os.getenv('GEMINI_API_LIST').split(',')
KEY_MANAGER_GEMINI = APIKeyManager(GEMINI_API_LIST)
GEMINI_MODEL = os.getenv("GEMINI_MODEL")

model_embedding = SentenceTransformer(MODEL_EMBEDDING)
client = QdrantClient(url=qdrant_url, api_key=qdrant_apikey)
top_query = CheckQuerySimilar(KEY_MANAGER_GEMINI,GEMINI_MODEL)

def description_search(query:str, collection_name:str, top_k:int):
    query_vector = model_embedding.encode(query)
    search_results = client.search(
    collection_name=collection_name,
    query_vector=query_vector,
    limit=top_k,
    )
    return search_results

def top_image_description(query:str, collection_name:str,top_k:int):
    search_results= description_search(query,collection_name,top_k)
    return search_results

def top_image_by_llm(user_query, query_list, top_k):
    query_list_to_prompt=""
    for i,query in enumerate(query_list):
        query_list_to_prompt+='('+str(i)+') '+query+'\n'
    print(query_list_to_prompt)
    return top_query.isSimilar(user_query, query_list_to_prompt,top_k)