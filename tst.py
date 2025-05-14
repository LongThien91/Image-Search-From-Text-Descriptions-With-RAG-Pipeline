import os
from GenerateImageDes.Gemini_Image_description import CheckImageDescriber
import cloudinary.uploader
from dotenv import load_dotenv
import matplotlib.pyplot as plt
import requests
from PIL import Image
from io import BytesIO
from cloudinary.utils import cloudinary_url

load_dotenv() 

#GEMINI_API_LIST = os.getenv("GEMINI_API_LIST")
#MODEL_GENERATOR = os.getenv("GEMINI_MODEL")

# get_img_des =CheckImageDescriber(GEMINI_API_LIST, MODEL_GENERATOR)
# img_path='D:\Desktop/food/non_la.jpg'
# imgDes= get_img_des.describe_image(img_path)
# print(imgDes)
CLOUD_NAME = os.getenv("CLOUD_NAME")
CLOUDINARY_API_KEY = os.getenv("CLOUDINARY_API_KEY")
CLOUDINARY_API_SECRETKEY = os.getenv("CLOUDINARY_API_SECRETKEY")

cloudinary.config(
  cloud_name = CLOUD_NAME,
  api_key = CLOUDINARY_API_KEY,
  api_secret = CLOUDINARY_API_SECRETKEY
)
# response = cloudinary.uploader.upload(r"D:\Desktop\food\mau-bang-hieu-sua-xe-bang-bat-hiflex-3.jpg", public_id="gtrfdvggd")
# print(response)

