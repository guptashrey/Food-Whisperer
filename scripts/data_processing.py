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
def load_processed_recipes(data_folder_path=os.path.join("data", "processed")):
    """Loads the processed recipes data from the processed data folder.

    Args:
        data_folder_path (str, optional): Path to the data folder containing the processed recipes. Defaults to "data".

    Returns:
        pd.DataFrame: The processed recipes dataframe.
    """
    # Load the processed recipes
    recipes_df_processed = pl.read_csv(os.path.join(data_folder_path, "processed_recipes.csv"))
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
    # Get the appropriate columns from the recipes dataframe
    recipes_df_processed = recipes_df[['id', 'minutes', 'tags', 'nutrition', 'n_steps', 'ingredients']]
    mlb = MultiLabelBinarizer()

    # Expand the nutrition column into 7 columns
    nutrition_columns = ['calories', 'fat_amount', 'sodium_amount', 'protein_amount', 'sugar_amount', 'saturated_fat', 'carbohydrates']
    recipes_df_processed['nutrition'] = recipes_df_processed['nutrition'].str.replace('[', '').str.replace(']', '')
    recipes_df_processed[nutrition_columns] = recipes_df_processed['nutrition'].str.split(',', expand=True).astype(float)
    recipes_df_processed = recipes_df_processed.drop(columns=['nutrition'])

    # Normalize the columns that aren't onehot encoded
    scaler = StandardScaler()
    columns_to_normalize = ['minutes', 'n_steps'] + nutrition_columns
    recipes_df_processed[columns_to_normalize] = scaler.fit_transform(recipes_df_processed[columns_to_normalize])

    # Explode the tags column and one hot encode them
    recipes_df_processed["tags"] = recipes_df_processed["tags"].apply(lambda x: x.replace("[", "").replace("]", "").replace("'", "").split(","))
    recipes_df_processed = _onehot_encode_cuisines(recipes_df_processed, mlb)

    # Explode the ingredients column and one hot encode them
    recipes_df_processed["ingredients"] = recipes_df_processed["ingredients"].apply(lambda x: x.replace("[", "").replace("]", "").replace("'", "").split(","))
    ingredient_mapping = load_ingredient_mapping_dict(data_folder_path=processed_data_folder_path)
    # One-hot encode the ingredients
    recipes_df_processed = _onehot_encode_ingredients(recipes_df_processed, mlb, ingredient_mapping)
    
    # Save the results
    print("Saving the results...")
    recipes_df_processed.to_csv(os.path.join(processed_data_folder_path, "processed_recipes.csv"), index=False)


##### Helper Functions #####
def _onehot_encode_ingredients(df, mlb, ingredient_mapping_dict, min_num_occurances=100):
    """A helper function to one-hot encode the ingredients column of the recipes dataframe.Before one-hot encoding, 
    the ingredients are mapped to a smaller set of ingredients using the ingredient_mapping.csv file.

    Args:
        df (pd.DataFrame): The recipes dataframe.
        mlb (sklearn.preprocessing.MultiLabelBinarizer): An instance of the MultiLabelBinarizer class.
        min_num_occurences (int, optional): The minimum number of occurances of an ingredient for it to be included in the one-hot encoding. Defaults to 10.

    Returns:
        pd.DataFrame: The recipes dataframe with the ingredients column one-hot encoded.
    """
    columns_minus_ingredients = list(df.columns.drop('ingredients'))

    # Explode the ingredients column
    df_processed = df.explode(column='ingredients')
    
    # Replace the ingredients using the ingredient mapping
    df_processed['ingredients'] = df_processed['ingredients'].apply(lambda x: ingredient_mapping_dict[x])
    
    # Only keep ingredients if they occur often enough
    df_processed['ingredients'] = df_processed['ingredients'].str.strip()
    ingredient_counts = df_processed['ingredients'].value_counts()
    top_ingredients = ingredient_counts[ingredient_counts >= min_num_occurances]
    
    # Seperate the recipes with and without ingredients in top_ingredients
    df_included = df_processed[df_processed['ingredients'].isin(top_ingredients.index)]
    df_included = df_included.groupby(columns_minus_ingredients).agg({'ingredients': lambda x: list(x)}).reset_index()
    
    df_excluded = df_processed[~df_processed['ingredients'].isin(top_ingredients.index)]
    df_excluded = df_excluded.groupby(columns_minus_ingredients).agg({'ingredients': lambda x: list(x)}).reset_index()
    
    # One-hot encode the ingredients
    df_included = df_included.join(pd.DataFrame(mlb.fit_transform(df_included.pop('ingredients')),
                          columns=mlb.classes_,
                          index=df_included.index))
    
    # Combine the excluded recipes back in
    df_processed = df_included.merge(df_excluded, on=columns_minus_ingredients, how='outer').fillna(0)
    df_processed = df_processed.drop(columns=['ingredients'])
    
    # Return the results
    return df_processed

def _onehot_encode_cuisines(df, mlb):
    """A helper function to one-hot encode the tags and turn them into cuisine data

    Args:
        df (pd.DataFrame): The recipes dataframe.
        mlb (sklearn.preprocessing.MultiLabelBinarizer): An instantiated MultiLabelBinarizer object.

    Returns:
        pd.DataFrame: The recipes dataframe with one-hot encoded cuisine data.
    """
    columns_minus_tags = list(df.columns.drop('tags'))
    
    # Get all the tags
    df_processed = df.explode(column='tags')
    df_processed['tags'] = df_processed['tags'].str.strip()
    
    # Drop tags not in the cuisine types
    df_included = df_processed[df_processed['tags'].isin(CUISINES)]
    df_included = df_included.groupby(columns_minus_tags).agg({'tags': lambda x: list(x)}).reset_index()
    
    df_excluded = df_processed[~df_processed['tags'].isin(CUISINES)]
    df_excluded = df_excluded.groupby(columns_minus_tags).agg({'tags': lambda x: list(x)}).reset_index()
    
    # One-hot encode the tags
    df_included = df_included.join(pd.DataFrame(mlb.fit_transform(df_included.pop('tags')),
                          columns=mlb.classes_,
                          index=df_included.index))
    # Combine the excluded recipes back in
    df_processed = df_included.merge(df_excluded, on=columns_minus_tags, how='outer').fillna(0)
    df_processed = df_processed.drop(columns=['tags'])                                     
    
    # Return the results
    return df_processed

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
    interactions_df, recipes_df = load_raw_data(data_folder_path=os.path.join("..", "data"))
    
    print("Processing recipes...")
    process_recipes(recipes_df, processed_data_folder_path=os.path.join("..", "data", "processed"))

    #num_recipes=50
    #print(f"Getting top {num_recipes} recipes...")
    #top_recipes = _get_top_recipes(interactions_df, recipes_df, num_recipes=num_recipes)
    #top_recipes[['recipe_id', 'name']].to_csv(os.path.join("..", "data", "processed", "top_recipes.csv"), index=False)