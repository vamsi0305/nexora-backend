import os
import cloudinary
import cloudinary.uploader
from dotenv import load_dotenv

load_dotenv()

# Configuration
cloudinary.config( 
  cloud_name = os.getenv("CLOUDINARY_CLOUD_NAME"), 
  api_key = os.getenv("CLOUDINARY_API_KEY"), 
  api_secret = os.getenv("CLOUDINARY_API_SECRET") 
)

def upload_image(file_data, folder="nexora"):
    """
    Uploads an image to cloudinary and returns the secure URL.
    file_data can be directly passed from FastAPI UploadFile.file
    """
    try:
        response = cloudinary.uploader.upload(file_data, folder=folder)
        return response.get("secure_url")
    except Exception as e:
        print(f"Cloudinary Error: {e}")
        return None
