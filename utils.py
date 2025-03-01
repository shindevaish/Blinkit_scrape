import json
# import jsonlines
import re
from datetime import datetime

def load_jsonl(file_path):
    data = []
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            item = json.loads(line)
            data.append(item)
    return data

documents_response=load_jsonl("/content/product_with_ocr.jsonl")

count=0
for document in documents_response:
    count+=1

def save_jsonl(output_file, data):
    global count
    with open(output_file, "a", encoding="utf-8") as f:
        if "_id" in data:
            data["_id"] = str(data["_id"]) 
        if "timestamp" in data and isinstance(data["timestamp"], datetime):
            data["timestamp"] = data["timestamp"].isoformat() 
        
        line = json.dumps(data)  
        f.write(line + "\n")
    count+=1
    
    print(f"Data appended to file successfully. {count} items appended.")

def dict_with_datetime(self):
    data = self.model_dump()
    data['updated'] = self.updated.isoformat()  # Convert datetime to ISO 8601 string
    return data



 
def extract_image_data(file_path):
    all_image_urls = []
    with jsonlines.open(file_path) as reader:
        for item in reader:
            image_urls = item.get("images", [])
            all_image_urls.append(image_urls)
    return all_image_urls

    
def preprocessing_image_url(image_url):
    lst=image_url.split('?')
    if check_valid_image_url(lst[0]):
        return lst[0]
    else:
        return False

def check_valid_image_url(lst):
    if lst.startswith('https://cdn') and lst.endswith('jpg') :
        return True
    else:
        return False

def preprocess_product_name(name):
    new_name = re.sub(r'\(.*?\)', '', name)
    new_str=''
    for char in new_name:
        if not char.isalnum() and not char.isspace():
            continue
        else:
            new_str+=char
    return new_str

def image_url_resolution(image_url):
    image_url = re.sub(r'w=\d+', f'w=1920', image_url)
    image_url = re.sub(r'h=\d+', f'h=1920', image_url)
    return image_url
