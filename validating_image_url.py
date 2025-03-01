import utils
import pandas as pd

documents=utils.load_jsonl("/Users/vaishnavishinde/Desktop/blinkit_scrape/product_ingredients_new.jsonl")

# csv_file="image_urls.csv"
count=0

for document in documents:
    new_image_urls=[]
    image_urls=document['images']
    for image_url in image_urls:
        count+=1
        is_valid=utils.preprocessing_image_url(image_url)
        if is_valid != False:
            new_image_urls.append(str(is_valid))
        else:
            continue
    document['images']=new_image_urls
    
    # product_name=document['name']
    # new_str=utils.preprocess_product_name(product_name)
    # document['name']=new_str
    
    utils.save_jsonl("/Users/vaishnavishinde/Desktop/blinkit_scrape/product_ingredients.jsonl",document)

# df = pd.DataFrame(new_image_urls)
print("COUNT",count)
# Write the DataFrame to a CSV file
# df.to_csv(csv_file, mode='a', index=False, header=False)