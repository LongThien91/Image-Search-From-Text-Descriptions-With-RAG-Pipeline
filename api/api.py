from fastapi import FastAPI, HTTPException, Form, File, UploadFile
from vectorDatabase.manage_collection import get_collection, create_collection,remove_collection
from vectorDatabase.embedding import add_img_to_collection
import os
import shutil
import os, zipfile, uuid

# 1. Khởi tạo ứng dụng FastAPI
app = FastAPI()


@app.get("/") 
async def read_root():
    return {"message": "Hãy truy cập http://127.0.0.1:8000/docs để sử dụng endpoint của project"}

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
    UPLOAD_DIR = "uploads"
    if os.path.exists(UPLOAD_DIR):
        shutil.rmtree(UPLOAD_DIR)
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    destination_path = os.path.join(UPLOAD_DIR, file.filename)
    try:
        if not destination_path.endswith(('.jpg', '.jpeg', '.png','.WebP')):
            raise ValueError("Unsupported file format. Only .jpg, .jpeg, .png, .webp are allowed.")
        
        with open(destination_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        add_img_to_collection(destination_path,collection_name)
        print(f"File saved to: {destination_path}")
        return  {f"File saved successfully"}
    except Exception as e:
        print(f"Error saving file: {e}")
        raise HTTPException(status_code=500, detail="Could not save file.")


@app.post("/add_by_zip")
async def add_by_zip(collection_name: str = Form(...), zip_file: UploadFile = File(...)):
    UPLOAD_DIR = "uploads"
    TEMP_EXTRACT_DIR = f"temp_extract_{uuid.uuid4().hex}"
    print(1)
    if os.path.exists(UPLOAD_DIR):
        shutil.rmtree(UPLOAD_DIR)
    os.makedirs(UPLOAD_DIR, exist_ok=True)

    # Tạo thư mục tạm để giải nén
    os.makedirs(TEMP_EXTRACT_DIR, exist_ok=True)

    zip_path = os.path.join(TEMP_EXTRACT_DIR, zip_file.filename)
    print(2)
    try:
        # Lưu file zip
        with open(zip_path, "wb") as buffer:
            shutil.copyfileobj(zip_file.file, buffer)

        # Giải nén file zip
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(TEMP_EXTRACT_DIR)

        for filename in os.listdir(TEMP_EXTRACT_DIR):
            full_path = os.path.join(TEMP_EXTRACT_DIR, filename)
    
            if os.path.isfile(full_path) and filename.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')):
                dst_path = os.path.join(UPLOAD_DIR, filename)
                shutil.move(full_path, dst_path)

                try:
                    add_img_to_collection(dst_path, collection_name)
                except Exception as e:
                    print(e)


    except Exception as e:
        print(f"Error handling zip file: {e}")
        raise HTTPException(status_code=500, detail="Error processing zip file.")

    finally:
        # Dọn dẹp thư mục tạm (không xóa uploads/)
        if os.path.exists(TEMP_EXTRACT_DIR):
            shutil.rmtree(TEMP_EXTRACT_DIR)