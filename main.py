import asyncio
from crawl4ai import AsyncWebCrawler
import json
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from pymongo import MongoClient
from datetime import datetime

MONGO_URI = "mongodb://localhost:27017/"
DB_NAME = "blinkit_data"
COLLECTION_NAME = "products"

BASE_URL = "https://blinkit.com"

file_path = "/Users/vaishnavishinde/Downloads/all_product_ingredients.json"  # Replace with your JSON file path
try:
    with open(file_path, "r") as file:
        data = json.load(file)
except FileNotFoundError:
    print(f"File not found: {file_path}")

count=0

async def main():
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    collection = db[COLLECTION_NAME]

    async with AsyncWebCrawler(verbose=True) as crawler:
        # result = await crawler.arun(
        #     url="https://blinkit.com/cn/sticks/cid/1969/263",
        # )

        for idx, url in enumerate(data.keys(), start=1):
            full_url = BASE_URL + url
            result3 = await crawler.arun(url=full_url)
            if result3.success:
                process_product(result3.html, collection, url)
            
            # Pause for 1 minute after every 20 URLs
            if idx % 20 == 0:
                print("\nPausing for 1 minute to avoid overloading...\n")
                await asyncio.sleep(30)
                            
    client.close()


def process_product(html, collection, url):
    global count
    soup = BeautifulSoup(html, 'html.parser')

    details = soup.select_one(".ProductDetails__ProductDetailsContainer-sc-z5f4ag-0.fRMVCN")
    extracted_text = details.get_text(strip=True) if details else None

    product_name = soup.select_one("h1[class*='ProductInfoCard__ProductName']")
    extracted_name = product_name.get_text(strip=True) if product_name else None

    image_urls = [img['src'] for img in soup.find_all("img") if img.get("src")]

    document = {
        "product_name": extracted_name,
        "details": extracted_text,
        "image_urls": image_urls,
        "url": url,
        "is_ingredients_in_details":False,
        "is_nutritions_in_details":False,
        "ingredients":None,
        "nutritions":None,
        "timestamp": datetime.utcnow()
    }

    collection.update_one( 
        {"url": url},
        {"$set": document},
        upsert=True,
    )
    count+=1
    print(f"Inserted product {count}: {extracted_name}\n")

asyncio.run(main())
