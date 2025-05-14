from sentence_transformers import SentenceTransformer
from langchain.schema import Document
from qdrant_client import QdrantClient,models
from qdrant_client.models import PointStruct
import os
import re
import uuid
from dotenv import load_dotenv
from GenerateImageDes.Gemini_Image_description import CheckImageDescriber
from cloudinary.utils import cloudinary_url
import cloudinary.uploader


load_dotenv()

MODEL_EMBEDDING=os.getenv("MODEL_EMBEDDING")
qdrant_url = os.getenv("qdrant_url")
qdrant_apikey = os.getenv("qdrant_apikey")
GEMINI_API_LIST = os.getenv("GEMINI_API_LIST")
GEMINI_MODEL = os.getenv("GEMINI_MODEL")

CLOUD_NAME = os.getenv("CLOUD_NAME")
CLOUDINARY_API_KEY = os.getenv("CLOUDINARY_API_KEY")
CLOUDINARY_API_SECRETKEY = os.getenv("CLOUDINARY_API_SECRETKEY")

cloudinary.config(
  cloud_name = CLOUD_NAME,
  api_key = CLOUDINARY_API_KEY,
  api_secret = CLOUDINARY_API_SECRETKEY
)

getDescriptionImg = CheckImageDescriber(GEMINI_API_LIST,GEMINI_MODEL)

def embedding(image_description):
    model = SentenceTransformer(MODEL_EMBEDDING)
    vector_hlembedding = model.encode(image_description)
    return vector_hlembedding

def add_img_to_collection(img_path, collection_name):

    img_description = getDescriptionImg.describe_image(img_path)
    vector_hlembedding= embedding(img_description) 
    print(img_description)
    new_image_name = str(uuid.uuid4()) #generate id for each image
    point = PointStruct(id=new_image_name, vector=vector_hlembedding, payload={"image_description": img_description})
    

    client = QdrantClient(url=qdrant_url, api_key=qdrant_apikey)
    client.upsert(collection_name=collection_name, points=[point])
    cloudinary.uploader.upload(
        img_path,
        public_id=new_image_name,
    )
    
    
    print(f"✅ Đã thêm image description vào collection '{collection_name}' và cloudinary thành công!")