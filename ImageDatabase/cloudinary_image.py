import cloudinary.uploader
from cloudinary.utils import cloudinary_url
from dotenv import load_dotenv
import os

load_dotenv()

CLOUD_NAME = os.getenv("CLOUD_NAME")
CLOUDINARY_API_KEY = os.getenv("CLOUDINARY_API_KEY")
CLOUDINARY_API_SECRETKEY = os.getenv("CLOUDINARY_API_SECRETKEY")

cloudinary.config(
  cloud_name = CLOUD_NAME,
  api_key = CLOUDINARY_API_KEY,
  api_secret = CLOUDINARY_API_SECRETKEY
)

def upload_image(img_path,uuid):
    try:
        response = cloudinary.uploader.upload(img_path, public_id=uuid)
        return response
    except:
        return "fail to upload image"
def get_image_url(uuid):
    try:
        url, _ = cloudinary_url(uuid, crop="fit")
        return url
    except:
        return "fail to get image url"
def delete_image(uuid):
    try:
        result = cloudinary.uploader.destroy(uuid)
        return result
    except:
        return "fail to delete image"