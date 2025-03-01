import utils

documents=utils.load_jsonl("/Users/vaishnavishinde/Desktop/blinkit_scrape/product_ingredients.jsonl")

for document in documents:
    new_image_list=[]
    image_urls=document["images"]
    for image_url in image_urls:
        image_updated=utils.image_url_resolution(str(image_url))

        new_image_list.append(image_updated)
    document["images"]=new_image_list

    utils.save_jsonl("/Users/vaishnavishinde/Desktop/blinkit_scrape/product_ingredients_updated.jsonl",document)