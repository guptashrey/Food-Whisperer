# Food-Whisperer

A Food Recipe Recommendation System

## Project Description


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