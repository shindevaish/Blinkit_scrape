import requests
import os
from firebase_admin import credentials, initialize_app, storage, get_app
import utils
import json
import firebase
import time
from firebase import FirebaseService, get_settings
from pymongo import MongoClient

settings = get_settings()
firebase = FirebaseService(settings)

count=0
def download_image(url, filename):
    global count
    try:
        folder="/Users/vaishnavishinde/Desktop/_new_image_blinkit/"
        os.makedirs(folder, exist_ok=True)

        save_path = os.path.join(folder, filename)

        response = requests.get(url, stream=True)
        response.raise_for_status()  

        with open(save_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        count+=1
        
        url = firebase.upload_image(save_path, "b")
        return url
    except requests.exceptions.RequestException as e:
        print(f"Failed to download image: {e}. URL: {url}")
    except FileNotFoundError as fnf_error:
        print(f"File not found: {fnf_error}. URL: {url}")
        return None
    except Exception as e:
        print(e)
        return None

documents = utils.load_jsonl("/Users/vaishnavishinde/Desktop/blinkit_scrape/product_ingredients_updated.jsonl")

# for document in documents:
document={"name": "Kellogg's Corn Flakes Original", "url": "https://blinkit.com/prn/kelloggs-corn-flakes-original/prid/95769", "details": "Product DetailsCorn FlakesTypeKey FeaturesKellogg\u2019s Corn Flakes is a nourishing and tasty ready-to-eat breakfast cereal which is High in Iron, Vitamin C and key essential B group Vitamins such as B1, B2, B3, B6, B12 and Folate.Kellogg\u2019s Corn Flakes Original is naturally cholesterol free. It contains only 1% Fat. You can count on Kellogg\u2019s for a great tasting and convenient breakfast that is nourishing.These corn flakes are made from sun ripened corn. The selected grains are cooked, flattened and are gently toasted to develop into your delicious golden crispy cereal.Kellogg\u2019s Corn Flakes is a quick and convenient breakfast option that is ready in minutes.Serve it with milk or curd/yoghurt and top it with fresh fruits such as bananas, strawberry or mangoes, dry fruits, honey and enjoy a nourishing breakfast.Break the monotony of breakfast and use Kellogg\u2019s Corn Flakes as a nourishing/tasty ingredient in a variety of recipes. Crunch up your Chana Chats, Fruity Yoghurt or Stir Fry with Kellogg\u2019s Corn Flakes and enjoy it at breakfast, lunch or dinner. Use it to prepare various tasty delights loved by kids and adults alike.IngredientsCorn Grits, Sugar, Malt Extract, Iodized Salt, Vitamins, Minerals and Antioxidant (INS 320)Unit875 gFSSAI License10013022002031Shelf Life12 monthsReturn PolicyThis Item is non-returnable. For a damaged, defective, incorrect or expired item, you can request a replacement within 72 hours of delivery.In case of an incorrect item, you may raise a replacement or return request only if the item is sealed/ unopened/ unused and in original condition.Packaging TypePouchManufacturer DetailsKelloggs India Pvt Ltd, Plot No. L2 & L3, Taloja MIDC, Dist. Rajgad, Maharashtra - 410208Marketed ByKelloggs India Pvt Ltd, Plot No. L2 & L3, Taloja MIDC, Dist. Rajgad, Maharashtra - 410208Country of OriginIndiaCustomer Care DetailsEmail: info@blinkit.comSellerSUPERWELL COMTRADE PRIVATE LIMITEDSeller FSSAI13323999000038DescriptionKellogg\u2019s Corn Flakes is a nourishing and tasty ready-to-eat breakfast cereal which is High in Iron, Vitamin C and key essential B group Vitamins such as B1, B2, B3, B6, B12 and Folate. Kellogg\u2019s Corn Flakes Original is naturally cholesterol free. It contains only 1% Fat. You can count on Kellogg\u2019s for a great tasting and convenient breakfast that is nourishing. These corn flakes are made from sun ripened corn. The selected grains are cooked, flattened and are gently toasted to develop into your delicious golden crispy cereal. Kellogg\u2019s Corn Flakes is a quick and convenient breakfast option that is ready in minutes. Serve it with milk or curd/yoghurt and top it with fresh fruits such as bananas, strawberry or mangoes, dry fruits, honey and enjoy a nourishing breakfast. Break the monotony of breakfast and use Kellogg\u2019s Corn Flakes as a nourishing/tasty ingredient in a variety of recipes. Use it to prepare various tasty delights loved by kids and adults alike.DisclaimerEvery effort is made to maintain the accuracy of all information. However, actual product packaging and materials may contain more and/or different information. It is recommended not to solely rely on the information presented.", "images": ["https://cdn.grofers.com/cdn-cgi/image/f=auto,fit=scale-down,q=85,metadata=none,w=1920,h=1920/da/cms-assets/cms/product/large_images/a781cf48-209c-4bcd-a591-4ec50f0f6468.jpg", "https://cdn.grofers.com/cdn-cgi/image/f=auto,fit=scale-down,q=85,metadata=none,w=1920,h=1920/da/cms-assets/cms/product/large_images/a781cf48-209c-4bcd-a591-4ec50f0f6468.jpg", "https://cdn.grofers.com/cdn-cgi/image/f=auto,fit=scale-down,q=85,metadata=none,w=1920,h=1920/da/cms-assets/cms/product/d8b3d7a7-a0ff-4b8c-b317-63b7d18a717d.jpg", "https://cdn.grofers.com/cdn-cgi/image/f=auto,fit=scale-down,q=85,metadata=none,w=1920,h=1920/da/cms-assets/cms/product/0e606099-759a-4c58-b377-a79240b8d29a.jpg", "https://cdn.grofers.com/cdn-cgi/image/f=auto,fit=scale-down,q=85,metadata=none,w=1920,h=1920/da/cms-assets/cms/product/70e4e020-b818-47fa-9d1e-ad88c6c9bf67.jpg", "https://cdn.grofers.com/cdn-cgi/image/f=auto,fit=scale-down,q=85,metadata=none,w=1920,h=1920/da/cms-assets/cms/product/e401f813-6d13-468a-92a0-7fc2234e1215.jpg", "https://cdn.grofers.com/cdn-cgi/image/f=auto,fit=scale-down,q=85,metadata=none,w=1920,h=1920/da/cms-assets/cms/product/1d78378d-1c0c-4c36-94e4-6e96f7141bc3.jpg", "https://cdn.grofers.com/cdn-cgi/image/f=auto,fit=scale-down,q=85,metadata=none,w=1920,h=1920/da/cms-assets/cms/product/6bc4fa99-0b84-4235-a368-d7acb029edfd.jpg", "https://cdn.grofers.com/cdn-cgi/image/f=auto,fit=scale-down,q=85,metadata=none,w=1920,h=1920/da/cms-assets/cms/product/5eaf136a-2ff1-421a-87cf-56224b3f7c02.jpg", "https://cdn.grofers.com/cdn-cgi/image/f=auto,fit=scale-down,q=85,metadata=none,w=1920,h=1920/da/cms-assets/cms/product/2286ec74-ec02-4d34-a51b-a68766828974.jpg"], "ingredients": "Corn Grits, Sugar, Malt Extract, Iodized Salt, Vitamins, Minerals and Antioxidant (INS 320)", "nutrients": None, "updated": "2024-12-26T00:08:39.583173", "image_bucket_urls": ["https://storage.googleapis.com/openlabel-lab-firebase.appspot.com/uploads/b/kelloggs_corn_flakes_original_95769_1.jpg", "https://storage.googleapis.com/openlabel-lab-firebase.appspot.com/uploads/b/kelloggs_corn_flakes_original_95769_2.jpg", "https://storage.googleapis.com/openlabel-lab-firebase.appspot.com/uploads/b/kelloggs_corn_flakes_original_95769_3.jpg", "https://storage.googleapis.com/openlabel-lab-firebase.appspot.com/uploads/b/kelloggs_corn_flakes_original_95769_4.jpg", "https://storage.googleapis.com/openlabel-lab-firebase.appspot.com/uploads/b/kelloggs_corn_flakes_original_95769_5.jpg", "https://storage.googleapis.com/openlabel-lab-firebase.appspot.com/uploads/b/kelloggs_corn_flakes_original_95769_6.jpg", "https://storage.googleapis.com/openlabel-lab-firebase.appspot.com/uploads/b/kelloggs_corn_flakes_original_95769_7.jpg", "https://storage.googleapis.com/openlabel-lab-firebase.appspot.com/uploads/b/kelloggs_corn_flakes_original_95769_8.jpg", "https://storage.googleapis.com/openlabel-lab-firebase.appspot.com/uploads/b/kelloggs_corn_flakes_original_95769_9.jpg"]}
# image_urls=document["images"]
image_urls=["https://cdn.grofers.com/cdn-cgi/image/f=auto,fit=scale-down,q=85,metadata=none,w=1920,h=1920/da/cms-assets/cms/product/2286ec74-ec02-4d34-a51b-a68766828974.jpg"]
product_name=document['name']
new_str=utils.preprocess_product_name(product_name)
image_bucket_urls=[]
prid=document["url"].split('/')
for i,image_url in enumerate(image_urls, start=1 ):
    save_path = new_str.lower().replace(" ", "_").replace("  ","_") + "_" + str(prid[-1]) + "_" + str(i) + ".jpg"
    url=download_image(image_url, save_path)
    # image_bucket_urls.append(url)
print("URL",url)
# time.sleep(0.25)
# document["image_bucket_urls"] = image_bucket_urls

# utils.save_jsonl("image_bucket_urls.jsonl", document) 



