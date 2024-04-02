import pymongo
from PIL import Image
import io
from utils.config import load_config

config = load_config('configs/config.yml')

mongodb_config = config['mongodb']
host = mongodb_config['host']
port = mongodb_config['port']
database = mongodb_config['database']
collection = mongodb_config['collection']

client = pymongo.MongoClient(f"mongodb://{host}:{port}/")
db = client[database]
image_collection = db[collection]

def get_image_from_mongodb(image_path):
    # Tìm kiếm ảnh trong cơ sở dữ liệu dựa trên image_path
    image_data = image_collection.find_one({"image_path": image_path})

    if image_data:
        # Đọc dữ liệu ảnh nhị phân từ MongoDB
        binary_data = image_data["image_data"]
        
        # Chuyển dữ liệu nhị phân thành đối tượng hình ảnh
        image = Image.open(io.BytesIO(binary_data))
        
        return image
    else:
        return None
