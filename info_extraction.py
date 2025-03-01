def get_information(urls):
    prompt="""
    You are a copywriter who can extract information from the given images.
    Examine the provided food images and extract the text from it. Answer the following requirements based on your text extracted:

    1. Does the image show the front side of a food package label? This side typically includes branding, the product name, and other marketing information.
    2. Extract ingredients if they start with 'ingredient'
    3. Extract the nutritional information, such as calories, macronutrients, vitamins, and minerals, fat, carbs, potassium, sodium, cholesterol, etc if it contains?
    4. Extract manufactured by details if it contains?
    5. Extract marketted by details if it contains?
    6. Extract fssai license if it contains?


    Provide your answers in a structured JSON format as follows:
        "is_image_front_food_label": [],
        "ingredients": [],
        "nutrition": [],
        "manufactured_by": [],
        "marketted_by": [],
        "fssai": [],


    Please only respond with the JSON structure based on the image content.

    Example: For the given images

    Response:{
        "is_image_front_food_label": true,
        "ingredients": WATER, SOYBEAN SOLIDS, SUGAR, COCOA SOLIDS, MINERAL (TRICALCIUM PHOSPHATE), EMULSIFIER (460, 466), SUNFLOWER LECITHIN, HONEY, FRUCTOSE, ACIDITY REGULATOR (501 ii), FLAVOURS (NATURE IDENTICAL FLAVOURING SUBSTANCES), EDIBLE COMMON SALT, VITAMIN E (ACETATE), VITAMIN A (ACETATE), VITAMIN B1 (THIAMINE MONONITRATE), VITAMIN B2 (RIBOFLAVIN) AND VITAMIN B12 (CYANOCOBALAMIN),
        "nutrition": NUTRITIONAL INFORMATION, TYPICAL VALUES PER 100 ml, ENERGY (Approx): 67 kcal, PROTEIN 3.0 g, TOTAL CARBOHYDRATE 10.3 g, SUGAR 7.5 g, DIETARY FIBER 0.8 g, TOTAL FAT 2.0 g, SATURATED FAT 0.5 g, TRANS FAT 0.0 g, CHOLESTEROL 0.0 g, CALCIUM 100 mg, IRON 0.3 mg, SODIUM 55 mg, VITAMIN E 0.7mg, VITAMIN A 56 mcg, VITAMIN B1 0.14mg,VITAMIN B2 0.16mg,VITAMIN B12 0.31 mcg,
        "manufactured_by": HERSHEY INDIA PRIVATE LIMITED PLOT NO. 5, NEW INDUSTRIAL AREA NO. 1, MANDIDEEP DIST RAISEN, ACTIAL, MP, INDIA,
        "marketted_by": HERSHEY INDIA PRIVATE LIMITED SCHINDLER HOUSE, HIRANANDANI GARDENS, POWAI, MUMBAI- 400076,
        "fssai": 10012022000243,
    }

    Example: For the given images

    Response:{
        "is_image_front_food_label": true,
        "ingredients": Durum Wheat Semolina,
        "nutrition": Energy (Kcal)   349.9, Protein (g)  10.9, Carbohydrates (g)    74.5, of which Sugars (g)   2.0, Total Fat (g)   0.9,
        "manufactured_by": WEXFIELD FOODS PVT. LTD, WEXFIELD ESTATE, GAT NO.- 485, LONIKAND NAGAR ROAD, TALUKA - HAVELI, DIST. - PUNE 412 208, MAHARASHTRA, INDIA. WWW.WEXFIELD.COM,
        "marketted_by": null,
        "fssai": Lic. No. 10012022001051,
    }

    Example: For the given images

    Response:{
        "is_image_front_food_label": true,
        "ingredients": Sugar, Vegetable fats (Palm, Sal, Shea), Skimmed Milk Powder (19.5%), Wheat Flour, Fat-reduced Cocoa Powder (3.5%), Wheat Starch, Malt Extract, Emulsifier (Lecithin - INS 322), Whey Powder, Hazelnuts, Raising Agent (INS 500ii, INS 503ii), lodised Salt, Flavouring substance (Vanillin).
        "nutrition": Energy (Kcal)   349.9, Protein (g)  10.9, Carbohydrates (g)    74.5, of which Sugars (g)   2.0, Total Fat (g)   0.9,
        "manufactured_by": WEXFIELD FOODS PVT. LTD, WEXFIELD ESTATE, GAT NO.- 485, LONIKAND NAGAR ROAD, TALUKA - HAVELI, DIST. - PUNE 412 208, MAHARASHTRA, INDIA. WWW.WEXFIELD.COM,
        "marketted_by": null,
        "fssai": Lic. No. 10012022001051,
    }


    Image_urls: []
    Response: 
    """
    message = [
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": prompt,
                },

            ],
        }
    ]
    for url in urls:
        message.append(
            {
                "type": "image_url",
                "image_url": {"url": url},
            }
        )
    response = litellm.completion(
        model="gemini/gemini-1.5-flash",
        api_key="AIzaSyCrAJDwe0-6c8uOv1tARIgLJd8R6grT06o",
        messages=message,
    )
    return response

urls=["https://storage.googleapis.com/openlabel-lab-firebase.appspot.com/uploads/b/paper_boat_zero_green_apple_flavoured_sparkling_drink__pack_of_2_532876_1.jpg", "https://storage.googleapis.com/openlabel-lab-firebase.appspot.com/uploads/b/paper_boat_zero_green_apple_flavoured_sparkling_drink__pack_of_2_532876_2.jpg", "https://storage.googleapis.com/openlabel-lab-firebase.appspot.com/uploads/b/paper_boat_zero_green_apple_flavoured_sparkling_drink__pack_of_2_532876_3.jpg", "https://storage.googleapis.com/openlabel-lab-firebase.appspot.com/uploads/b/paper_boat_zero_green_apple_flavoured_sparkling_drink__pack_of_2_532876_4.jpg", "https://storage.googleapis.com/openlabel-lab-firebase.appspot.com/uploads/b/paper_boat_zero_green_apple_flavoured_sparkling_drink__pack_of_2_532876_5.jpg", "https://storage.googleapis.com/openlabel-lab-firebase.appspot.com/uploads/b/paper_boat_zero_green_apple_flavoured_sparkling_drink__pack_of_2_532876_6.jpg", "https://storage.googleapis.com/openlabel-lab-firebase.appspot.com/uploads/b/paper_boat_zero_green_apple_flavoured_sparkling_drink__pack_of_2_532876_7.jpg", "https://storage.googleapis.com/openlabel-lab-firebase.appspot.com/uploads/b/paper_boat_zero_green_apple_flavoured_sparkling_drink__pack_of_2_532876_8.jpg", "https://storage.googleapis.com/openlabel-lab-firebase.appspot.com/uploads/b/paper_boat_zero_green_apple_flavoured_sparkling_drink__pack_of_2_532876_9.jpg", "https://storage.googleapis.com/openlabel-lab-firebase.appspot.com/uploads/b/paper_boat_zero_green_apple_flavoured_sparkling_drink__pack_of_2_532876_10.jpg"]
response=get_information(urls)
print(response)

