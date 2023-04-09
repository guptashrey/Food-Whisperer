##### Imports ######
import os
import polars as pl
import pandas as pd
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.preprocessing import StandardScaler
import warnings
warnings.filterwarnings('ignore')

##### Constants #####
CUISINES = {'italian', 'chinese', 'indian', 'thai', 'american', 'greek', 'spanish', 'german', 'french', 'japanese', 'lebanese', 'korean', 'australian', 'caribbean', 'filipino', 'scottish', 'mexican', 'indonesian', 'brazilian', 'south-african'}

##### Loading Data Functions #####
def load_processed_recipes_similarity(data_folder_path=os.path.join("data", "processed")):
    """Loads the processed recipes data from the processed data folder.

    Args:
        data_folder_path (str, optional): Path to the data folder containing the processed recipes. Defaults to "data".

    Returns:
        pd.DataFrame: The processed recipes dataframe.
    """
    # Load the processed recipes
    recipes_df_processed = pl.read_csv(os.path.join(data_folder_path, "processed_recipes_for_similarity.csv"))
    recipes_df_processed = recipes_df_processed.to_pandas()
    return recipes_df_processed

def load_processed_recipes_display(data_folder_path=os.path.join("data", "processed")):
    """Loads the processed recipes data from the processed data folder.

    Args:
        data_folder_path (str, optional): Path to the data folder containing the processed recipes. Defaults to "data".

    Returns:
        pd.DataFrame: The processed recipes dataframe.
    """
    # Load the processed recipes
    recipes_df_processed = pl.read_csv(os.path.join(data_folder_path, "processed_recipes_for_display.csv"))
    recipes_df_processed = recipes_df_processed.to_pandas()
    return recipes_df_processed

def load_raw_data(data_folder_path="data"):
    """Loads the interactions and recipes data from the data folder.

    Args:
        data_folder_path (str, optional): path to the folder containing the data. Defaults to "data".

    Returns:
        tuple: tuple containing the interactions and recipe dataframes.
    """
    # Load the interactions and recipes
    interactions_df = load_raw_interactions(data_folder_path=data_folder_path)
    recipes_df = load_raw_recipes(data_folder_path=data_folder_path)
    
    return interactions_df, recipes_df

def load_raw_interactions(data_folder_path="data"):
    """Loads the interactions data from the data folder.

    Args:
        data_folder_path (str, optional): Path to the folder containing the data. Defaults to "data".

    Returns:
        pd.DataFrame: The interactions dataframe.
    """
    # Load the interactions
    interactions_df = pl.read_csv(os.path.join(data_folder_path, "RAW_interactions.csv")) 
    
    # Convert to pandas dataframe
    interactions_df = interactions_df.to_pandas()
    
    # Return the dataframe
    return interactions_df

def load_raw_recipes(data_folder_path="data"):
    """Loads the recipes data from the data folder.

    Args:
        data_folder_path (str, optional): Path to the folder containing the data. Defaults to "data".

    Returns:
        pd.DataFrame: The recipes dataframe.
    """
    # Load the recipes
    recipes_df = pl.read_csv(os.path.join(data_folder_path, "RAW_recipes.csv"))
    
    # Convert to pandas dataframe
    recipes_df = recipes_df.to_pandas()
    
    # Return the dataframe
    return recipes_df

def load_ingredient_mapping_dict(data_folder_path=os.path.join("data", "processed")):
    """Loads the ingredient mapping from the data folder.

    Args:
        data_folder_path (str, optional): Path to the folder containing the data. Defaults to "data/processed".

    Returns:
        dict: The ingredient mapping.
    """
    # Load the ingredient mapping
    ingredient_mapping = pd.read_csv(os.path.join(data_folder_path, "ingredient_mapping.csv")).set_index('ingredient').to_dict()['mapping']
    return ingredient_mapping


##### Data Processing Functions #####
def process_recipes(recipes_df, processed_data_folder_path=os.path.join("data", "processed")):
    """Processes the recipe data with the following steps:
         - Expand the nutrition column into ['calories', 'fat_amount', 'sodium_amount', 'protein_amount', 'sugar_amount', 'saturated_fat', 'carbohydrates']
         - One-hot encode the tags related to the cuisine of the recipe
         - One-hot encode the ingredients

    Args:
        recipes_df (pd.DataFrame): The recipes dataframe.

    Returns:
        pd.DataFrame: The processed recipes dataframe.
    """
    # Instantiate the MultiLabelBinarizer and load the ingredient mapping
    mlb = MultiLabelBinarizer()
    ingredient_mapping_dict = load_ingredient_mapping_dict(data_folder_path=os.path.join("..", "data", "processed"))

    # Get the appropriate columns from the recipes dataframes and do some renaming
    recipes_df_processed = recipes_df[['name', 'id', 'minutes', 'tags', 'nutrition', 'n_steps', 'ingredients']]
    recipes_df_processed = recipes_df_processed.rename(columns={'tags': 'cuisine'})

    # Expand the nutrition column into 7 columns
    nutrition_columns = ['calories', 'fat_amount', 'sodium_amount', 'protein_amount', 'sugar_amount', 'saturated_fat', 'carbohydrates']
    recipes_df_processed['nutrition'] = recipes_df_processed['nutrition'].str.replace('[', '').str.replace(']', '')
    recipes_df_processed[nutrition_columns] = recipes_df_processed['nutrition'].str.split(',', expand=True).astype(float)
    recipes_df_processed = recipes_df_processed.drop(columns=['nutrition'])

    # Convert the tags column to a cuisine column
    columns_minus_cuisine = list(recipes_df_processed.columns.drop('cuisine'))
    recipes_df_processed["cuisine"] = recipes_df_processed["cuisine"].apply(lambda x: x.replace("[", "").replace("]", "").replace("'", "").split(","))

    # Get all the tags
    recipes_df_processed = recipes_df_processed.explode(column='cuisine')
    recipes_df_processed['cuisine'] = recipes_df_processed['cuisine'].str.strip()

    # Drop tags not in the cuisine types and recombine the cuisine columns
    df_included = recipes_df_processed[recipes_df_processed['cuisine'].isin(CUISINES)]
    df_included = df_included.groupby(columns_minus_cuisine).agg({'cuisine': lambda x: list(x)}).reset_index()
    df_excluded = recipes_df_processed[~recipes_df_processed['cuisine'].isin(CUISINES)]
    df_excluded = df_excluded.groupby(columns_minus_cuisine).agg({'cuisine': lambda x: list(x)}).reset_index()
    recipes_df_processed = df_included.merge(df_excluded, on=columns_minus_cuisine, how='outer').fillna("-")
    recipes_df_processed = recipes_df_processed.drop(columns=['cuisine_y']).rename(columns={'cuisine_x': 'cuisine'})

    # Replace the ingredients using thr mapping
    recipes_df_processed["ingredients"] = recipes_df_processed["ingredients"].apply(lambda x: x.replace("[", "").replace("]", "").replace("'", "").split(","))
    recipes_df_processed["ingredients"] = recipes_df_processed["ingredients"].apply(lambda x: [ingredient_mapping_dict[ingr] for ingr in x])
    recipes_df_processed_display = recipes_df_processed.copy()
    
    # Onehot encode the cuisine columns
    recipes_df_processed = recipes_df_processed.join(pd.DataFrame(mlb.fit_transform(recipes_df_processed.pop('cuisine')),
                            columns=mlb.classes_,
                            index=recipes_df_processed.index))

    # Onehot encode the ingredients columns
    recipes_df_processed = _onehot_encode_ingredients(recipes_df_processed, mlb)


    # Drop the name column for the similarity matrix and normalize the data
    recipes_df_processed = recipes_df_processed.drop(columns=['name'])
    columns_to_normalize = ['minutes', 'n_steps'] + nutrition_columns
    recipes_df_processed[columns_to_normalize] = StandardScaler().fit_transform(recipes_df_processed[columns_to_normalize])

    # Save the results
    print("Saving the results...")
    recipes_df_processed_display.to_csv(os.path.join(processed_data_folder_path, "processed_recipes_for_display.csv"), index=False)
    recipes_df_processed.to_csv(os.path.join(processed_data_folder_path, "processed_recipes_for_similarity.csv"), index=False)


##### Helper Functions #####
def _onehot_encode_ingredients(recipes_df_processed, mlb, min_num_occurences=100):
    """A helper function to one-hot encode the ingredients column of the recipes dataframe.

    Args:
        recipes_df_processed (pd.DataFrame): The processed recipes dataframe.
        mlb (sklearn.preprocessing.MultiLabelBinarizer): An instance of the MultiLabelBinarizer class.
        min_num_occurences (int, optional): The minimum number of occurances of an ingredient for it to be included in the one-hot encoding. Defaults to 10.

    Returns:
        pd.DataFrame: The recipes dataframe with the ingredients column one-hot encoded.
    """
    columns_minus_ingredients = list(recipes_df_processed.columns.drop('ingredients'))
    recipes_df_processed = recipes_df_processed.explode(column='ingredients')

    # Only keep ingredients if they occur often enough
    recipes_df_processed['ingredients'] = recipes_df_processed['ingredients'].str.strip()
    ingredient_counts = recipes_df_processed['ingredients'].value_counts()
    top_ingredients = ingredient_counts[ingredient_counts >= min_num_occurences]

    # Seperate the recipes with and without ingredients in top_ingredients
    df_included = recipes_df_processed[recipes_df_processed['ingredients'].isin(top_ingredients.index)]
    df_included = df_included.groupby(columns_minus_ingredients).agg({'ingredients': lambda x: list(x)}).reset_index()

    df_excluded = recipes_df_processed[~recipes_df_processed['ingredients'].isin(top_ingredients.index)]
    df_excluded = df_excluded.groupby(columns_minus_ingredients).agg({'ingredients': lambda x: list(x)}).reset_index()

    # One-hot encode the ingredients
    df_included = df_included.join(pd.DataFrame(mlb.fit_transform(df_included.pop('ingredients')),
                            columns=mlb.classes_,
                            index=df_included.index))

    # Combine the excluded recipes back in
    recipes_df_processed = df_included.merge(df_excluded, on=columns_minus_ingredients, how='outer').fillna(0)
    recipes_df_processed = recipes_df_processed.drop(columns=['ingredients'])
    
    # Return the results
    return recipes_df_processed

def _get_top_recipes(interactions_df, recipes_df, num_recipes=25):
    """Helper function to get the top recipes based on the number of ratings it has

    Args:
        interactions_df (pd.DataFrame): The interactions dataframe.
        recipes_df (pd.DataFrame): The  recipes dataframe.
        num_recipes (int, optional): The number of recipes to be included. Defaults to 25.

    Returns:
        pd.DataFrame: A dataframe containing the top recipes
    """
    # Get the top recipe_ids
    top_recipes = interactions_df.groupby("recipe_id").count().sort_values("rating", ascending=False).reset_index()
    recipe_ids = top_recipes[['recipe_id']].head(num_recipes)

    # Combine with the interactions_df
    combined_df = pd.merge(recipe_ids, recipes_df, left_on='recipe_id', right_on='id').drop(columns=['id'])
    return combined_df

##### Main Function #####
if __name__ == "__main__":
    print("Loading data...")
    interactions_df, recipes_df = load_raw_data(data_folder_path=os.path.join("..", "data", "raw"))
    
    print("Processing recipes...")
    process_recipes(recipes_df, processed_data_folder_path=os.path.join("..", "data", "processed"))

    #num_recipes=50
    #print(f"Getting top {num_recipes} recipes...")
    #top_recipes = _get_top_recipes(interactions_df, recipes_df, num_recipes=num_recipes)
    #top_recipes[['recipe_id', 'name']].to_csv(os.path.join("..", "data", "processed", "top_recipes.csv"), index=False)