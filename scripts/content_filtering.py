##### Imports #####
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

##### Functions #####
def most_similar_recipes(recipes_df, recipes_df_processed, recipe_id, top_n=10):
    """Gets the top n most similar recipes to a given recipe. A recipe is passed
    by using it's id

    Args:
        recipes_df (pd.DataFrame): The raw dataframe of recipes.
        recipes_df_processed (pd.DataFrame): the processed dataframe of recipes.
        recipe_id (int): the id of the recipe to find similar recipes to.
        top_n (int, optional): The number of recipes to find. Defaults to 10.

    Returns:
        tuple: The top n most similar recipe names and ids.
    """
    top_recipe_names = []
    top_recipe_ids = []
            
    # Build the similarity matrix of recipes
    csmatrix = calculate_similarity_matrix(recipes_df_processed)
    
    # Get the top n most similar recipes
    most_similar_recipes = csmatrix.loc[recipe_id, :].sort_values(ascending=False).index[1:top_n+1]
    for recipe in most_similar_recipes:
        top_recipe_names.append(recipes_df[recipes_df['id'] == recipe]['name'])
        top_recipe_ids.append(recipe)
    
    # Return the top names and ids
    return top_recipe_names, top_recipe_ids 

def calculate_similarity_matrix(df):
    """Calculates the cosine similarity matrix of a dataframe.

    Args:
        df (pd.DataFrame): The dataframe to calculate the cosine similarity matrix of.

    Returns:
        pd.DataFrame: The resulting cosine similarity matrix.
    """
    csmatrix = cosine_similarity(df)
    csmatrix = pd.DataFrame(csmatrix,columns=df['id'],index=df['id'])
    return csmatrix
