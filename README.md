# Blinkit_scrape

### This project is about extraction of details of various food products from the blinkit.com to create a dataset of different products.

## How to run the project:
1. main.py
   (Ouput: It will create a database in mongodb.)
2. ing_extraction.py
   (Output: Create a class of product and convert database into jsonl. Also extract the ingredients from the product_details using a model.)
3. validating_image_url.py
   (Output: check for valid image url in dataset.)
4. image_resolution.py
   (Output: Increase the resolution of the image.)
5. download_image.py
   (Output: Download the image using url. Also create a bucket url and save it to the document.)
6. image_class.py
   (Output: create a class of image.)
7. image_ocr.ipynb
   (Output: extract the text from the image.)
