# Imports for webscraping
from io import BytesIO
import os
from PIL import Image
from bs4 import BeautifulSoup
import requests
import re
import numpy as np

def scrape_image(recipe_name, recipe_id, image_save_folder_path="images", height=None, width=None):
    """Given a recipe name and id, scrape the image from the recipe page and save it to the specified folder

    Args:
        recipe_name (str): The name of the recipe
        recipe_id (int): The id of the recipe
        image_save_folder_path (str, optional): The path to the folder where the image will be saved. 
                                                It is created if it doesn't exist. Defaults to "images".
        height (int, optional): The height of the resulting image you want. Defaults to None.
        width (int, optional): the width of the resulting image you want. Defaults to None.

    Returns:
        tuple: The url of the recipe page and whether the image was found
    """
    # Track whether we got an image or not
    ImageFound = True
    
    # Craft the url for the specific recipe page
    base_url = "https://www.Food.com/recipe/"
    
    recipe_name = recipe_name.strip().split(" ")
    recipe_name = [word.lower().strip() for word in recipe_name if word != ""]
    recipe_name = "-".join(recipe_name)
    recipe_url = f"{base_url}{recipe_name}-{recipe_id}"
    
    try:
        # Get the html from the recipe page
        page = requests.get(recipe_url)
        soup = BeautifulSoup(page.content, 'html.parser')
        
        # Find the image url in the div block with class media "svelte-wgcq7z"
        image_url = soup.find("div", class_="media svelte-wgcq7z").find("img")["src"]
        
        # Adjust the height and width of the image
        if width is not None and height is not None:
            aspect_ratio_width = int(np.ceil(width / height))
            aspect_ratio_height = int(np.ceil(height / width))
            aspect_ratio = f"{aspect_ratio_width}:{aspect_ratio_height}"
            
            image_url = re.sub(r"w_\d+", f"w_{width}", image_url)
            image_url = re.sub(r"ar_\d+:\d+", f"ar_{aspect_ratio}", image_url)
        elif width is not None:
            print("Height not specified, image is remaining unchanged")
        elif height is not None:
            print("Width not specified, image is remaining unchanged")
        
        # Get the image from the url
        image = requests.get(image_url)
        image = Image.open(BytesIO(image.content))
        
        # Save the image to the folder
        save_path = os.path.join(image_save_folder_path, f"{recipe_id}.jpg")
        # Make sure the path exists
        if not os.path.exists(image_save_folder_path):
            os.makedirs(image_save_folder_path)
        image.save(save_path)
    
    except:
        # Unable to load image
        ImageFound = False
    
    # Return the recipe url and whether the image was found
    return recipe_url, ImageFound
    
if __name__ == "__main__":
    recipe_name = "alouette   potatoes"
    recipe_id = 59389
    
    url, imageFound = scrape_image(recipe_name, recipe_id,width=500,height=500)
    print(f"Recipe Name: {recipe_name}")
    print(f"Recipe ID: {recipe_id}")
    print(f"Image Found: {imageFound}")