import re
import os
import clip
import open_clip
import torch
import json
import glob
from PIL import Image
import faiss
import numpy as np
from utils.nlp_processing import Translation

os.environ['KMP_DUPLICATE_LIB_OK']='True'

class MyFaiss:
    def __init__(self, bin_clip_path: str, json_path: str):
        self.index_clip = self.load_bin_file(bin_clip_path)
        self.id2img_fps = self.load_json_file(json_path)
        self.translater = Translation()
        self.__device = "cuda" if torch.cuda.is_available() else "cpu"
        self.clip_model, _ = clip.load("ViT-B/16", device=self.__device)

    def load_bin_file(self, bin_file: str):
        return faiss.read_index(bin_file)
    
    def load_json_file(self, json_path: str):
        with open(json_path, 'r') as f: 
            js = json.load(f)
        return {int(k):v for k,v in js.items()}
    
    def text_search(self, text, k):
        gpu_index = self.index_clip
        # res = faiss.StandardGpuResources()
        # print(faiss.index_cpu_to_gpus_list)
        # gpu_index = faiss.index_cpu_to_all_gpus(gpu_index)

        text = self.translater(text)
        text = clip.tokenize([text]).to(self.__device)
        text_features = self.clip_model.encode_text(text)
        text_features /= text_features.norm(dim=-1, keepdim=True)
        text_features = text_features.cpu().detach().numpy().astype(np.float32)
        scores, idx_image = gpu_index.search(text_features, k)
      
        idx_image = idx_image.flatten()
        
        infos_query = list(map(self.id2img_fps.get, list(idx_image)))
        image_paths = [info['image_path'] for info in infos_query]
        return scores.flatten(), idx_image, infos_query, image_paths

def main():
    

    bin_file = "dict/faiss_clip.bin"
    json_path = 'dict/id2img_fps.json'

    cosine_faiss = MyFaiss(bin_file, json_path)

    text = 'con gà'
    scores, _, infos_query, image_paths = cosine_faiss.text_search(text, k=1000)

    # print(scores)
    # print(infos_query)
    # for i in image_paths:
    #     link = 'data_image' + i
    #     img = Image.open(link)
    #     img.show()

if __name__ == "__main__":
    main()