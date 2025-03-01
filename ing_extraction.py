from pydantic import BaseModel, Field
from datetime import datetime
from pymongo import MongoClient
from litellm import completion
import litellm
import time
from typing import List,Optional
import json

# litellm.set_verbose=True

class ProductProfile(BaseModel):
    name: str = Field(..., description="Product Name")
    url: str = Field(..., description="Product URL")
    details: str = Field(..., description="Product Details")
    images: list = Field(..., description="Image URLs List")
    ingredients: str = Field(None, description="Ingredients")
    nutrients: str = Field(None, description="Nutrients")
    updated: datetime = Field(default_factory=datetime.now)

    def dict_with_datetime(self):
        data = self.model_dump()
        data['updated'] = self.updated.isoformat()  # Convert datetime to ISO 8601 string
        return data

MONGO_URI_update = "mongodb://localhost:27017/"
DB_NAME_update = "blinkit_data"
COLLECTION_NAME_update = "products_update2"

client = MongoClient(MONGO_URI_update)
db = client[DB_NAME_update]
collection = db[COLLECTION_NAME_update]

existing_jsonl_file = "/Users/vaishnavishinde/Desktop/blinkit_scrape/products_ingredients.jsonl"
jsonl_file = "/Users/vaishnavishinde/Desktop/blinkit_scrape/remaining_products.jsonl"

def ingredient_extractor(details):
    prompt = """
        You are a copywriter who can extract information from the text.
        Food label ingredients are extracted as text which is not in a structured format.
        Your task is to copy the ingredient information from the below given text as exactly given.
        Rules to follow:
        1. Only extract ingredients if they start with 'ingredient'
        2. Extract all the ingredients from the text.
        3. Don't explain the ingredients.
        4. Only generate ingredients as response
        5. If ingredients is not present in details then response should print("None")

        Example:
        Text: Product DetailsIngredientsFresh Chicken MeatNutrition InformationEnergy 19.5 Kcal, Protein 29.55g. Fat 7.72g, Carbo 0g, Soduim 393 mg, Potassium 243 mg, Cholesterol 83 mg.Bone/BoneLessWith BoneSkin/SkinLessWith SkinFresh/FrozenFrozenStorage TipsFreezerUnit1 unitCut TypeCurry CutTypeCurry CutFSSAI License13320009000043Serve SizeServes 3Pieces3 pcsHygienically Vacuum PackedYesShelf Life12 MonthsReturn PolicyThis Item is non-returnable. For a damaged, defective, incorrect or expired item, you can request a replacement within 72 hours of delivery. In case of an incorrect item, you may raise a replacement or return request only if the item is sealed/ unopened/ unused and in original condition.Packaging TypeVaccum PouchManufacturer DetailsGlobal Commodities, A 21, Nangal Dewat Vasant Kunj New delhi - 110070.Country of OriginIndiaCustomer Care DetailsEmail: info@blinkit.comSellerKEMEXEL ECOMMERCE PRIVATE LIMITEDSeller FSSAI10823999000118DisclaimerQuantity variations from the weight may occur, caused by loss or gain of moisture during the course of good distribution practices or by unavoidable reasons.
        Response: Fresh Chicken Meat

        Text: Product DetailsCoconut & ChocolateFlavourIngredientsMilk chocolate coating (36%): Milk Chocolate coating (Sugar, Milk Solids, (skimmed milk powder, lactose, milk fat, whey powder), Cocoa Butter, Cocoa Mass, Centre filling (desiccated coconut (21%), Emulsifier (soya lecithin (E322)), natural vanilla extract), Sugar, Glucose syrup, Emulsifiers (mono-an diglycerides of fatty acids (E471), glycerol (E422)), salt, natural vanilla extract). Milk chocolate: cocoa solids 25% min.Key FeaturesThis Bounty Miniatures Pouch contains 13 coconut chocolate treats insideEnjoy moist & tender coconut covered in a thick milk chocolate coatingMake every moment extra special with Bounty imported chocolatesThese miniature chocolates offer irresistible bites full of rich & creamy textureEnjoy Bounty chocolate shared pack as a post-meal treat or a leisure-time snackFSSAI License10012011000434Shelf Life12 MonthsReturn PolicyThis Item is non-returnable. For a damaged, defective, incorrect or expired item, you can request a replacement within 72 hours of delivery.In case of an incorrect item, you may raise a replacement or return request only if the item is sealed/ unopened/ unused and in original condition.Unit130 gCountry of OriginNetherlandsCustomer Care DetailsEmail: info@blinkit.comSellerKEMEXEL ECOMMERCE PRIVATE LIMITEDSeller FSSAI10823999000118DescriptionBounty Miniature chocolate pack is a perfect choice to add to your quality time. Treat your taste buds to the delicious combination of classic coconut and rich chocolate. Drive away mid-week blues or share sweet moments with friends or family. People who love chocolates and coconut will surely relish every bite of this heavenly mini chocolate.DisclaimerEvery effort is made to maintain accuracy of all information. However, actual product packaging and materials may contain more and/or different information. It is recommended not to solely rely on the information presented.
        Response: Milk chocolate coating (36%): Milk Chocolate coating (Sugar, Milk Solids, (skimmed milk powder, lactose, milk fat, whey powder), Cocoa Butter, Cocoa Mass, Centre filling (desiccated coconut (21%), Emulsifier (soya lecithin (E322)), natural vanilla extract), Sugar, Glucose syrup, Emulsifiers (mono-an diglycerides of fatty acids (E471), glycerol (E422)), salt, natural vanilla extract). Milk chocolate: cocoa solids 25% min.

        Text: Product DetailsCut TypeBengali CutUnit500 gTypeCatla FishFSSAI License1332000900043Shelf Life4 daysReturn PolicyThis Item is non-returnable. For a damaged, defective, incorrect or expired item, you can request a replacement within 72 hours of delivery.In case of an incorrect item, you may raise a replacement or return request only if the item is sealed/ unopened/ unused and in original condition.Packaging TypeVacuum PouchManufacturer DetailsGlobal Commodities, C-5/56, First Floor, Vasant Kunj-110070Marketed ByGlobal Commodities, Vasant Kunj, New Delhi-110070Country of OriginIndiaCustomer Care DetailsEmail: info@blinkit.comSellerKEMEXEL ECOMMERCE PRIVATE LIMITEDSeller FSSAI10823999000118DescriptionSeafood includes vital nutrients needed for health and wellness at all ages, including omega-3s, iron, B and D vitamins, and protein. Fish and other seafood supply the nutrients, vitamins, and omega 3s essential for strong bones, brain development, and a healthy heart and immune system.DisclaimerQuantity variations from the weight may occur, caused by loss or gain of moisture during the course of good distribution practices or by unavoidable reasons.
        Response: None

        Text: {{details}}
        Response:
        """

    if "ingredient" in details.lower():
        prompt_ = prompt.replace("{{details}}", details)
        try:
            response = completion(
                model="gemini/gemini-1.5-flash",
                messages=[{"role": "user", "content": prompt_}],
                api_key="AIzaSyCrAJDwe0-6c8uOv1tARIgLJd8R6grT06o"
            )
        except Exception as e :
            print(e)
            time.sleep(50)
            response = completion(
                model="gemini/gemini-1.5-flash",
                messages=[{"role": "user", "content": prompt_}],
                api_key="AIzaSyCrAJDwe0-6c8uOv1tARIgLJd8R6grT06o", 
            )


        try:
            extracted_ingredients = response['choices'][0]['message']['content'].strip()
        except (KeyError, IndexError, AttributeError):
            extracted_ingredients = None
        
        return extracted_ingredients




lst=[]
with open(existing_jsonl_file, "r", encoding='UTF-8') as file:
    for line in file:
        data = json.loads(line) 
        if 'url' in data:
            last_number = data['url'].split('/')[-1]  
            lst.append(last_number)
    

try:
    with open(jsonl_file, "w") as file:
        documents = collection.find()

        for doc in documents:
            if doc['url'].split('/')[-1] not in lst:
                got_from_db_product = {
                    "name": doc.get('product_name'),
                    "url": doc.get('url'),
                    "details": doc.get('details'),
                    "images": doc.get('image_urls', []),
                }
                try:
                    update_product = ProductProfile(**got_from_db_product)
                    # time.sleep(2)
                    response = ingredient_extractor(update_product.details)

                    if response:
                        update_product.ingredients = response

                    # Convert to dictionary and write to JSONL
                    file.write(json.dumps(update_product.dict_with_datetime()) + "\n")
                    print(f"Updated document with url {doc['url']}: Ingredient - {update_product.ingredients}\n")
                except Exception as e:
                    print(e)

except Exception as e:
    print(e)
    client.close()