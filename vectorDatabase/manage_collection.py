from qdrant_client import QdrantClient,models
from dotenv import load_dotenv
import os

load_dotenv()

qdrant_apikey = os.getenv("qdrant_apikey")
qdrant_url = os.getenv("qdrant_url")

def create_collection(collection_name):
    try:
        client = QdrantClient(url=qdrant_url, api_key=qdrant_apikey)
        client.recreate_collection(
        collection_name=collection_name,
        vectors_config=models.VectorParams(size=768, distance=models.Distance.COSINE),)
        print(f"Collection '{collection_name}' đã được tạo thành công!")
    except Exception as e:
        print(f"Error: {e}")

def remove_collection(collection_name : str):
    try:
        client = QdrantClient(url=qdrant_url, api_key=qdrant_apikey)
        client.delete_collection(collection_name=collection_name)
        print(f"Collection '{collection_name}' đã được xóa thành công!")
    except Exception as e:
        print(f"Error: {e}")
        
def get_collection():
    try:
        client = QdrantClient(url=qdrant_url, api_key=qdrant_apikey)
        collection = client.get_collections()
        return collection
    except Exception as e:
        print(f"Error: {e}")