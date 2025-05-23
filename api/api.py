from fastapi import FastAPI, HTTPException, Form, File, UploadFile
from vectorDatabase.manage_collection import get_collection, create_collection,remove_collection,is_collection_available
from vectorDatabase.embedding import add_img_to_collection, add_img_to_collection_with_description
from vectorDatabase.vector_search import top_image_description,top_image_by_llm
from ImageDatabase.cloudinary_image import get_image_url
import os
import shutil
import os, zipfile, uuid
import json
import requests

# 1. Khởi tạo ứng dụng FastAPI
app = FastAPI()


@app.get("/") 
async def read_root():
    return {"message": "Hãy truy cập http://127.0.0.1:8000/docs để sử dụng api của project"}

@app.get("/get_collections") 
async def get_collections():
    try:
        ls_collection = get_collection()
        return str(ls_collection)
    except Exception as e:
        # Log lỗi (nếu có hệ thống log thì dùng logging.error)
        print(f"Error in get_collections: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
 
@app.post("/create_collections") 
async def create_collections(collection_name: str = Form(...)):
    """
    Tạo một collection mới trong Qdrant DB.

    Args:
        request (CollectionRequest): Yêu cầu tạo collection, bao gồm tên collection.

    Returns:
        dict: Thông báo thành công hoặc lỗi.
    """
    try:
        create_collection(collection_name)
        print(collection_name)
        return  {"message": "Collection created successfully"}
    except Exception as e:
        print(f"Error in get_collections: {e}")
        raise HTTPException(status_code=500, detail="False to create collection")
    
@app.post("/remove_collections") 
async def remove_collections(collection_name: str = Form(...)):
    try:
        remove_collection(collection_name)
        print(collection_name)
        return  {"message": "Collection removed successfully"}
    except Exception as e:
        print(f"Error in get_collections: {e}")
        raise HTTPException(status_code=500, detail="False to remove collection")
@app.post("/add_by_file")
async def add_by_file(collection_name: str = Form(...), file: UploadFile = File(...)):

    if is_collection_available(collection_name)==0:
        return f"Collection {collection_name} is not available"
    UPLOAD_DIR = "uploads"
    if os.path.exists(UPLOAD_DIR):
        shutil.rmtree(UPLOAD_DIR)
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    destination_path = os.path.join(UPLOAD_DIR, file.filename)
    try:
        if not destination_path.lower().endswith(('.jpg', '.jpeg', '.png','.webp')):
            raise ValueError("Unsupported file format. Only .jpg, .jpeg, .png, .webp are allowed.")
        
        with open(destination_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        add_img_to_collection(destination_path,collection_name)
        print(f"File saved to: {destination_path}")
        
        if os.path.exists(UPLOAD_DIR):
            shutil.rmtree(UPLOAD_DIR)
        return  {f"File saved successfully"}
    except Exception as e:
        print(f"Error saving file: {e}")
        raise HTTPException(status_code=500, detail="Could not save file.")

@app.post("/add_by_file_with_description")
async def add_by_file_with_description(collection_name: str = Form(...), file: UploadFile = File(...),description: str = Form(...)):
    """
    Lưu ý, khi đưa ảnh có 2 vật thể trở lên, hãy phân tách phần mô tả của từng vật thể bằng dấu:---

    
    Ví dụ: Áo sơ mi ngắn tay có màu trắng, bên vai phải in huy hiệu J97 --- Quần âu màu đen kẻ sọc, chất liệu bằng vải
    """
    if is_collection_available(collection_name)==0:
        return f"Collection {collection_name} is not available"
    UPLOAD_DIR = "uploads"
    if os.path.exists(UPLOAD_DIR):
        shutil.rmtree(UPLOAD_DIR)
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    destination_path = os.path.join(UPLOAD_DIR, file.filename)
    try:
        if not destination_path.lower().endswith(('.jpg', '.jpeg', '.png','.webp')):
            raise ValueError("Unsupported file format. Only .jpg, .jpeg, .png, .webp are allowed.")
        
        with open(destination_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        add_img_to_collection_with_description(destination_path,collection_name, description)
        print(f"File saved to: {destination_path}")
        
        if os.path.exists(UPLOAD_DIR):
            shutil.rmtree(UPLOAD_DIR)
        return  {f"File saved successfully"}
    except Exception as e:
        print(f"Error saving file: {e}")
        raise HTTPException(status_code=500, detail="Could not save file.")

@app.post("/add_by_zip")
async def add_by_zip(collection_name: str = Form(...), zip_file: UploadFile = File(...)):

    if is_collection_available(collection_name)==0:
        return "Collection not available"
    UPLOAD_DIR = "uploads"
    TEMP_EXTRACT_DIR = f"extract_dir"
    if os.path.exists(UPLOAD_DIR):
        shutil.rmtree(UPLOAD_DIR)
    if os.path.exists(TEMP_EXTRACT_DIR):
        shutil.rmtree(TEMP_EXTRACT_DIR)
    os.makedirs(UPLOAD_DIR, exist_ok=True)

    # Tạo thư mục tạm để giải nén
    os.makedirs(TEMP_EXTRACT_DIR, exist_ok=True)

    zip_path = os.path.join(TEMP_EXTRACT_DIR, zip_file.filename)
    try:
        # Lưu file zip
        with open(zip_path, "wb") as buffer:
            shutil.copyfileobj(zip_file.file, buffer)

        # Giải nén file zip
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(TEMP_EXTRACT_DIR)
        for filename in os.listdir(TEMP_EXTRACT_DIR):
            print('process', filename)
            full_path = os.path.join(TEMP_EXTRACT_DIR, filename)
    
            if os.path.isfile(full_path) and filename.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')):
                dst_path = os.path.join(UPLOAD_DIR, filename)
                shutil.move(full_path, dst_path)
                
                try:
                    add_img_to_collection(dst_path, collection_name)
                    #asyncio.sleep(1.5)
                except Exception as e:
                        print(e)
        if os.path.exists(UPLOAD_DIR):
            shutil.rmtree(UPLOAD_DIR)
        return "File đã được thêm thành công"

    except Exception as e:
        print(f"Error handling zip file: {e}")
        raise HTTPException(status_code=500, detail="Error processing zip file.")

    finally:
        if os.path.exists(TEMP_EXTRACT_DIR):
            shutil.rmtree(TEMP_EXTRACT_DIR)

@app.post("/get_matching_image")
async def get_matching_image(collection_name: str = Form(...), query: str = Form(...)):

    try:
        results=top_image_description(query,collection_name,20)
        query_list=[]
        for result in results:
            print(result.payload["image_description"])
            query_list.append(result.payload["image_description"])
        query_list_to_prompt= top_image_by_llm(query,query_list,5)
        lst = json.loads(query_list_to_prompt) 
        url_list=[]
        for i in lst:
            result=results[int(i)]
            print(result.payload["image_description"])
            uuid = (result.payload["id_image"])
            url = get_image_url(uuid)+':    '+(result.payload["image_description"])+'\n'
            url_list.append(url)  
        if len(url_list)==0:
            return "their is no result match at all"
        return url_list
    except Exception as e:
        print(f"Error to get matching image url: {e}")