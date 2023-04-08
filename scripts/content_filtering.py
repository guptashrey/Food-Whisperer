##### Imports #####
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

##### Functions #####
def most_similar_recipe(recipes_df, recipes_df_processed, recipe_id, top_n=10):
    top_recipe_names = []
    top_recipe_ids = []
            
    # Build the similarity matrix of recipes
    csmatrix = cosine_similarity(recipes_df_processed)
    csmatrix = pd.DataFrame(csmatrix,columns=recipes_df_processed['id'],index=recipes_df_processed['id'])
    
    # Get the top n most similar recipes
    most_similar_recipes = csmatrix.loc[recipe_id, :].sort_values(ascending=False).index[1:top_n+1]
    for recipe in most_similar_recipes:
        top_recipe_names.append(recipes_df[recipes_df['id'] == recipe]['name'])
        top_recipe_ids.append(recipe)
    
    # Return the top names and ids
    return top_recipe_names, top_recipe_ids 
