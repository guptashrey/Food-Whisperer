##### Imports ######
import os
import pandas as pd

##### Functions #####
def process_data(data_folder_path="data"):
    # Load the data
    print("Loading data...")
    interactions_df, recipes_df, ingredient_mapping = load_raw_data(data_folder_path=data_folder_path)
    
def load_raw_data(data_folder_path="data"):
    """Loads the interactions (contains ratings from users), recipes, and 
    ingredient mapping dataframes from the data folder

    Args:
        data_folder_path (str, optional): Path to the folder containing the data. Defaults to "data".

    Returns:
        tuple: the interactions, recipes, and ingredient mapping dataframes
    """
    # Load the interactions and recipes
    interactions_df = pd.read_csv(os.path.join(data_folder_path, "RAW_interactions.csv")) 
    recipes_df = pd.read_csv(os.path.join(data_folder_path, "RAW_recipes.csv"))
    
    # Load the ingredient mapping
    ingredient_mapping = pd.read_pickle(os.path.join(data_folder_path, "ingr_map.pkl"))
    
    # Return each dataframe
    return interactions_df, recipes_df, ingredient_mapping


##### Main Function #####
if __name__ == "__main__":
    process_data(data_folder_path=os.path.join("..", "data"))