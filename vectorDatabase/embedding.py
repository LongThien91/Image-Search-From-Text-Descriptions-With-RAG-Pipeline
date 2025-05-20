from sentence_transformers import SentenceTransformer
from langchain.schema import Document
from qdrant_client import QdrantClient,models
from qdrant_client.models import PointStruct
import os
import re
import uuid
from dotenv import load_dotenv
from LLM.Gemini_Image_description_for_clothes import CheckImageDescriber
from cloudinary.utils import cloudinary_url
import cloudinary.uploader
from LLM.api_list_manager import APIKeyManager


load_dotenv()

MODEL_EMBEDDING=os.getenv("MODEL_EMBEDDING")
qdrant_url = os.getenv("qdrant_url")
qdrant_apikey = os.getenv("qdrant_apikey")

GEMINI_API_LIST = os.getenv('GEMINI_API_LIST').split(',')
KEY_MANAGER_GEMINI = APIKeyManager(GEMINI_API_LIST)
GEMINI_MODEL = os.getenv("GEMINI_MODEL")

CLOUD_NAME = os.getenv("CLOUD_NAME")
CLOUDINARY_API_KEY = os.getenv("CLOUDINARY_API_KEY")
CLOUDINARY_API_SECRETKEY = os.getenv("CLOUDINARY_API_SECRETKEY")

cloudinary.config(
  cloud_name = CLOUD_NAME,
  api_key = CLOUDINARY_API_KEY,
  api_secret = CLOUDINARY_API_SECRETKEY
)

getDescriptionImg = CheckImageDescriber(KEY_MANAGER_GEMINI,GEMINI_MODEL)
model_embedding = SentenceTransformer(MODEL_EMBEDDING)
def embedding(image_description):
    vector_hlembedding = model_embedding.encode(image_description)
    return vector_hlembedding

def add_img_to_collection(img_path, collection_name):
    try:
        img_description = getDescriptionImg.describe_image(img_path)
        des_list= img_description.split('---')
        vector_hlembedding=[]
        print("Có" ,len(des_list) , "Vật thể ở trong ảnh")
        for i in range(0,len(des_list)):
            print(des_list[i])
            vector_hlembedding.append(embedding(des_list[i]) )
        new_image_name = str(uuid.uuid4()) #generate id for each image
        points = [
        models.PointStruct(
            id=str(uuid.uuid4()),
            payload={"image_description": image_description,"id_image":new_image_name,} ,
            vector=vector_hlembedding[idx],
        )
        for idx,image_description in enumerate(des_list)
    ]
        client = QdrantClient(url=qdrant_url, api_key=qdrant_apikey)
        client.upsert(collection_name=collection_name, points=points)
        cloudinary.uploader.upload(
            img_path,
            public_id=new_image_name,
        )
        
        print(f"✅ Đã thêm image description vào collection '{collection_name}' và cloudinary thành công!")
    except Exception as e:
        print(f"add image to collection fail: {e}")

def add_img_to_collection_with_description(img_path, collection_name,description):
    try:
        des_list= description.split('---')
        vector_hlembedding=[]
        print("Có" ,len(des_list) , "Vật thể ở trong ảnh")
        for i in range(0,len(des_list)):
            print(des_list[i])
            vector_hlembedding.append(embedding(des_list[i]) )
        new_image_name = str(uuid.uuid4()) #generate id for each image
        points = [
        models.PointStruct(
            id=str(uuid.uuid4()),
            payload={"image_description": image_description,"id_image":new_image_name,} ,
            vector=vector_hlembedding[idx],
        )
        for idx,image_description in enumerate(des_list)
    ]
        client = QdrantClient(url=qdrant_url, api_key=qdrant_apikey)
        client.upsert(collection_name=collection_name, points=points)
        cloudinary.uploader.upload(
            img_path,
            public_id=new_image_name,
        )
        
        print(f"✅ Đã thêm image description vào collection '{collection_name}' và cloudinary thành công!")
    except Exception as e:
        print(f"add image to collection fail: {e}")