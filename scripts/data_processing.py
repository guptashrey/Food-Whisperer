##### Imports ######
import os
import polars as pl
import pandas as pd
from sklearn.preprocessing import MultiLabelBinarizer
import warnings
warnings.filterwarnings('ignore')

##### Constants #####
CUISINES = {'italian', 'chinese', 'indian', 'thai', 'american', 'greek', 'spanish', 'german', 'french', 'japanese', 'lebanese', 'korean', 'australian', 'caribbean', 'filipino', 'scottish', 'mexican', 'indonesian', 'brazilian', 'south-african'}
NUM_INGREDIENTS = 100

##### Loading Data Functions #####
def load_raw_data(data_folder_path="data"):
    """Loads the interactions and recipes data from the data folder.

    Args:
        data_folder_path (str, optional): path to the folder containing the data. Defaults to "data".

    Returns:
        tuple: tuple containing the interactions and recipe dataframes.
    """
    # Load the interactions and recipes
    interactions_df = load_interactions(data_folder_path=data_folder_path)
    recipes_df = load_recipes(data_folder_path=data_folder_path)
    
    return interactions_df, recipes_df

def load_interactions(data_folder_path="data"):
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

def load_recipes(data_folder_path="data"):
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


##### Data Processing Functions #####
def process_recipes(recipes_df):
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
    new_columns = ['calories', 'fat_amount', 'sodium_amount', 'protein_amount', 'sugar_amount', 'saturated_fat', 'carbohydrates']
    recipes_df_processed['nutrition'] = recipes_df_processed['nutrition'].str.replace('[', '').str.replace(']', '')
    recipes_df_processed[new_columns] = recipes_df_processed['nutrition'].str.split(',', expand=True).astype(float)
    recipes_df_processed = recipes_df_processed.drop(columns=['nutrition'])

    # Explode the tags column and one hot encode them
    recipes_df_processed["tags"] = recipes_df_processed["tags"].apply(lambda x: x.replace("[", "").replace("]", "").replace("'", "").split(","))
    recipes_df_processed = _tags_to_cuisines(recipes_df_processed)
    recipes_df_processed = recipes_df_processed.join(pd.DataFrame(mlb.fit_transform(recipes_df_processed.pop('tags')),
                            columns=mlb.classes_,
                            index=recipes_df_processed.index))

    # Explode the ingredients column and one hot encode them
    recipes_df_processed["ingredients"] = recipes_df_processed["ingredients"].apply(lambda x: x.replace("[", "").replace("]", "").replace("'", "").split(","))
    recipes_df_processed = _remove_sparse_ingredients(recipes_df_processed, keep_top_n=NUM_INGREDIENTS)
    recipes_df_processed = recipes_df_processed.join(pd.DataFrame(mlb.fit_transform(recipes_df_processed.pop('ingredients')),
                            columns=mlb.classes_,
                            index=recipes_df_processed.index))
    
    return recipes_df_processed

##### Helper Functions #####
def _remove_sparse_ingredients(df, keep_top_n=20):
    """Helper function to remove ingredients that are not in the top n ingredients.

    Args:
        df (pd.DataFrame): The recipes dataframe.
        keep_top_n (int, optional): How many ingredients to be kept in the data. Defaults to 20.

    Returns:
        pd.DataFrame: The recipes dataframe with the ingredients column processed.
    """
    df_processed = df.copy()
    columns_minus_ingredients = list(df_processed.columns.drop('ingredients'))

    # Get the top n ingredients
    df_processed = df_processed.explode(column='ingredients')
    df_processed['ingredients'] = df_processed['ingredients'].str.strip()
    ingredient_counts = df_processed['ingredients'].value_counts()
    top_n = ingredient_counts.iloc[:keep_top_n]
    
    # Drop rows where ingredient not in top n
    df_processed = df_processed[df_processed['ingredients'].isin(top_n.index)]
    df_processed = df_processed.groupby(columns_minus_ingredients).agg({'ingredients': lambda x: list(x)}).reset_index()

    # Return the results
    return df_processed

def _tags_to_cuisines(df):
    """Helper function to convert the tags column into a cuisine column.

    Args:
        df (pd.DataFrame): the recipes dataframe.

    Returns:
        pd.DataFrame: The new dataframe with all irrelevant tags removed.
    """
    df_processed = df.copy()
    columns_minus_tags = list(df_processed.columns.drop('tags'))
    
    # Get all the tags
    df_processed = df_processed.explode(column='tags')
    df_processed['tags'] = df_processed['tags'].str.strip()
    
    # Drop tags not in the cuisine types
    df_processed = df_processed[df_processed['tags'].isin(CUISINES)]
    df_processed = df_processed.groupby(columns_minus_tags).agg({'tags': lambda x: list(x)}).reset_index()
    
    # Return the results
    return df_processed

##### Main Function #####
if __name__ == "__main__":
    print("Loading data...")
    interactions_df, recipes_df = load_raw_data(data_folder_path=os.path.join("..", "data"))
    
    print("Processing recipes...")
    recipes_df_processed = process_recipes(recipes_df)
    print(recipes_df_processed)