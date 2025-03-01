from pydantic import BaseModel, Field
from datetime import datetime
from litellm import completion
import litellm
import time
from typing import List,Optional
import utils

# litellm.set_verbose=True

class ImageDetails(BaseModel):
    url: str = Field(..., description="Image URL")
    raw_ocr_text: str = Field(..., description="Raw OCR Text extracted from the image")
    relevant: bool = Field(..., description="Indicates if the image is relevant or not")

    def dict_with_datetime(self):
        return self.model_dump()

class ProductProfile(BaseModel):
    name: str = Field(..., description="Product Name")
    url: str = Field(..., description="Product URL")
    details: str = Field(..., description="Product Details")
    images: list = Field(..., description="Image URLs List")
    image_bucket_urls: List[ImageDetails] = Field(..., description="List of Image Details")
    ingredients: str = Field(None, description="Ingredients")
    nutrients: str = Field(None, description="Nutrients")
    updated: datetime = Field(default_factory=datetime.now)

    def dict_with_datetime(self):
        data = self.model_dump()
        data['updated'] = self.updated.isoformat()
        return data

output_file="/Users/vaishnavishinde/Desktop/blinkit_scrape/updated_products.jsonl"

try:
    documents = utils.load_jsonl("/Users/vaishnavishinde/Desktop/blinkit_scrape/image_bucket_urls.jsonl")

    for doc in documents:
        got_from_db_product = {
            "name": doc.get('name'),
            "url": doc.get('url'),
            "details": doc.get('details'),
            "images": doc.get('images', {}),
        }

        image_details_list = []
        if 'image_bucket_urls' in doc:
            for image_url in doc['image_bucket_urls']:
                raw_ocr_text = f"Simulated OCR text"
                is_relevant = "keyword" in raw_ocr_text.lower()

                image_detail = ImageDetails(
                    url=image_url,
                    raw_ocr_text=raw_ocr_text,
                    relevant=is_relevant
                )
                image_details_list.append(image_detail.dict_with_datetime())
        
            # print(f"Processed image details: {image_details_list}")

        got_from_db_product["image_bucket_urls"] = image_details_list


        try:
            update_product = ProductProfile(**got_from_db_product)
            utils.save_jsonl(output_file,update_product.dict_with_datetime())
            print(f"Updated document with URL {doc['url']}\n")
        except Exception as e:
            print(f"Error updating product: {e}")

except Exception as e:
    print(f"Error processing documents: {e}")
