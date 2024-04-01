import pymongo
from bson.binary import Binary
import json
from tqdm import tqdm
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

file_paths = config['file_paths']
json_path = file_paths['json_path']
with open(json_path, 'r') as file:
    img_paths = json.load(file)

def add_image_to_mongodb(image_path):
    with open('.'+image_path, "rb") as f:
        image_data = f.read()

    binary_data = Binary(image_data)

    image_id = image_collection.insert_one({"image_data": binary_data, "image_path": image_path}).inserted_id

    return image_id


for index in tqdm(img_paths):
    for img in img_paths[index]:
        image_path = img_paths[index]['image_path']
        image_id = add_image_to_mongodb(image_path)