from qdrant_client import QdrantClient,models
from dotenv import load_dotenv
import os
import cloudinary.uploader
from ImageDatabase.cloudinary_image import delete_image

load_dotenv()

qdrant_apikey = os.getenv("qdrant_apikey")
qdrant_url = os.getenv("qdrant_url")

CLOUD_NAME = os.getenv("CLOUD_NAME")
CLOUDINARY_API_KEY = os.getenv("CLOUDINARY_API_KEY")
CLOUDINARY_API_SECRETKEY = os.getenv("CLOUDINARY_API_SECRETKEY")

cloudinary.config(
  cloud_name = CLOUD_NAME,
  api_key = CLOUDINARY_API_KEY,
  api_secret = CLOUDINARY_API_SECRETKEY
)

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
        all_ids= get_all_id_in_collection(collection_name)
        for id in all_ids:
            delete_image(id)
            print(f"xóa {id} thành công")
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

def get_all_id_in_collection(collection_name : str):
    all_ids = []
    try:
        client = QdrantClient(url=qdrant_url, api_key=qdrant_apikey)
        offset = None

        while True:
            points, offset = client.scroll(
                collection_name=collection_name,
                limit=100000,            
                offset=offset,
                with_payload=True,
                with_vectors=False    
            )
            all_ids.extend([point.payload["id_image"] for point in points])
            if offset is None:
                break

        return all_ids
    except:
        return all_ids
def is_collection_available(collection_name:str):
    client = QdrantClient(url=qdrant_url, api_key=qdrant_apikey)
    collections = client.get_collections().collections
    collection_names = [col.name for col in collections]
    return int(collection_name in collection_names)