# Food Whisper: Food Recipe Recommender
> #### _Archit, Bryce, Shrey | Spring '23 | Duke AIPI 540 Recommender Systems Project_
&nbsp;

## Project Description

From our perspective, there are two types of people when it comes to cooking: those who see it as a fun activity and a hobby of theirs and those who see it as a chore they need to do for themselves or their family each day. If you are in the former group, you likely enjoy trying out new recipes often. Unfortunately, choosing which recipe to try next is often the hardest part. There are so many unique and delicious recipes out there, and it can be very difficult to narrow them all down to one or two that you want to try next. If you view cooking as a chore, you likely have a small set of meals that you cook over and over and over again. These can become stale and boring over time, and adding in a few new meals once in a while is a great way to spice things up. Either way, if you find yourself in need of some new recipes, we have just the solution for you!

We have created a recipe recommendation system that allows you to get a series of recipes that align with your preferences in no time. Using information such as how long the meal takes to make, the nutritional value, and the ingredients present in the dish, we utilize content filtering to recommend recipes similar to those of meals that you already know you like. As a new user, you simply select what meals and dishes you enjoy / think look good and then we recommend the best recipes for you to try next.

## Data

For this project we used a [recipe dataset](https://www.kaggle.com/datasets/shuyangli94/food-com-recipes-and-user-interactions?select=RAW_recipes.csv) on [Kaggle](https://www.kaggle.com/) that contains data on recipes and corresponding ratings provided by users. This dataset is a collection of ratings and recipes from [Food.com](https://www.food.com/) and contains 230k+ recipes and 700k+ reviews from users over a span of 18 years. This dataset was originally used in the paper [Generating Personalized Recipes from Historical User Preferences](https://aclanthology.org/D19-1613/) written by Bodhisattwa Prasad Majumder, Shuyang Li, Jianmo Ni, and Julian McAuley. The recipe and user data consists of the following:

**Recipe Data**:

- `name`: The name of the recipe
- `id`: ID of the recipe
- `minutes`: The number of minutes needed to follow the recipe.
- `contributor_id`: ID of the user who contributed the recipe.
- `submitted`: The date the recipe was submitted in YYYY-MM-DD format.
- `tags`: A list of tags associated with the recipe. Some examples are `60-minutes-or-less`, `weeknight`, and `italian`.
- `nutrition`: A list of 7 values representing the following categories: `[calories (#), total fat (PDV), sugar (PDV), sodium (PDV), protein (PDV) , saturated fat, and carbohydrates]`.
- `n_steps`: The number of steps in the recipe.
- `steps`: The text description of the steps that make up the recipe.
- `description`: A text description of the recipe left by the contributor.
- `ingredients`: The list of ingredients needed for the recipe.
- `n_ingredients`: The number of ingredients in the recipe.

**Interaction Data**:

- `user_id`: ID number for the user leaving a review.
- `recipe_id`: ID number for the recipe.
- `date`: The date the user left the review in YYYY-MM-DD format.
- `rating`: The rating the user gave the recipe on a 1-5 scale.
- `review`: The text review the user left describing their thoughts about the recipe.

## Running the Demo

## Project Structure
The project data and codes are arranged in the following manner:

```
├── data                                <- directory for project data
    ├── processed                       <- directory to store processed data
    ├── raw                             <- directory to store raw data
├── notebooks                           <- directory to store any exploration/scratch notebooks used
├── scripts                             <- directory for data processing, inference server and metrics scripts
    ├── coverage_calculation.py         <- script to calculate the coverage metric
    ├── data_processing.py              <- script to process the raw data
    ├── image_scraping.py               <- script to scrape the recipe images from food.com
    ├── inference_server.py             <- script to run the recommendation pipeline server
    ├── inference.py                    <- script to run the recommendation pipeline
├── .gitattributes                      <- git attributes file (for git lfs)
├── .gitignore                          <- git ignore file
├── LICENSE                             <- license file
├── README.md                           <- description of project and how to set up and run it
├── requirements.txt                    <- requirements file to document dependencies
```
&nbsp;
## Food Whisperer (Streamlit):
* Refer to the [README.md](https://github.com/guptashrey/Food-Whisperer/blob/st/README.md) at this link to run the Streamlit-based web application or access it [here](https://food-whisperer.streamlit.app/).
* You can find the code for the Streamlit web-app [here](https://github.com/guptashrey/Food-Whisperer/tree/st)