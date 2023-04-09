# library imports
import os
import sys
sys.path.append('..')

from data_processing import load_processed_recipes_similarity, load_processed_recipes_display

import pandas as pd
import numpy as np
import numba

# loading the data
recipes_df_similarity = load_processed_recipes_similarity(data_folder_path=os.path.join('..', 'data', 'processed'))
recipes_df_display = load_processed_recipes_display(data_folder_path=os.path.join('..', 'data', 'processed'))
recipes_df_display["url"] = "https://www.food.com/recipe/" + recipes_df_display["name"].replace(' ', '-', regex=True) + "-" + recipes_df_display["id"].astype(str)
recipe_name_mapping = pd.read_csv("../data/processed/recipe_name_mapping.csv")
recipes_df_display = recipes_df_display.merge(recipe_name_mapping, on="name", how="left")
recipes_df_display.corrected_name.fillna(recipes_df_display.name.str.title(), inplace=True)

@numba.jit(nopython=True, parallel=True)
def fast_cosine_matrix(u, M):
    """
    Computes the cosine similarity between a vector u and each row of a matrix M.

    Args:
        u (np.array): vector of shape (m,).
        M (np.array): matrix of shape (n, m).

    Returns:
        np.array: vector of shape (n,) containing the cosine similarity between u and each row of M.
    """
    scores = np.zeros(M.shape[0])
    for i in numba.prange(M.shape[0]):
        v = M[i]
        m = u.shape[0]
        udotv = 0
        u_norm = 0
        v_norm = 0
        for j in range(m):
            if (np.isnan(u[j])) or (np.isnan(v[j])):
                continue

            udotv += u[j] * v[j]
            u_norm += u[j] * u[j]
            v_norm += v[j] * v[j]

        u_norm = np.sqrt(u_norm)
        v_norm = np.sqrt(v_norm)

        if (u_norm == 0) or (v_norm == 0):
            ratio = 1.0
        else:
            ratio = udotv / (u_norm * v_norm)
        scores[i] = ratio
    return scores

def get_top_n_recipe_ids(recipe_id, top_n=5):
    """
    Returns the top n recipe ids that are most similar to the recipe with id recipe_id.

    Args:
        recipe_id (int): recipe id.
        top_n (int, optional): number of recipes to return. Defaults to 5.

    Returns:
        list: list of recipe ids.
    """

    # assign u as the row of recipes_df_similarity corresponding to recipe_id
    # assign M as the matrix of recipes_df_similarity without the first column
    u = recipes_df_similarity.iloc[:, 1:][recipes_df_similarity["id"]==recipe_id].to_numpy().squeeze()
    M = recipes_df_similarity.iloc[:, 1:].to_numpy()
    
    # calculate the cosine similarity between u and each row of M
    res = fast_cosine_matrix(u, M)

    # get the top n recipe ids according to the cosine similarity
    res = np.argsort(res)[-(top_n+1):][:-1]
    
    # return the recipe ids
    return list(recipes_df_similarity.iloc[res].id)

def get_recommended_recipes(recipe_ids, top_n=5):
    """
    Returns the top n recipes that are most similar to the recipe with id recipe_id.

    Args:
        recipe_id (int): recipe id.
        top_n (int, optional): number of recipes to return. Defaults to 5.

    Returns:
        pd.DataFrame: dataframe containing the top n recipes.
    """

    recommended_recipes = recipes_df_display[:0]
    
    # get the top n recipes for each recipe id
    for id in recipe_ids:
        ids = get_top_n_recipe_ids(id, top_n)
        temp = recipes_df_display[recipes_df_display["id"].isin(ids)]
        recommended_recipes = pd.concat([recommended_recipes, temp])
    
    # drop duplicates and reset index
    recommended_recipes = recommended_recipes.drop_duplicates()
    recommended_recipes = recommended_recipes.reset_index(drop=True)
    
    # return the dataframe
    return recommended_recipes