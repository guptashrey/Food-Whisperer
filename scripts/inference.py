import os

from scripts.data_processing import load_processed_recipes_similarity, load_processed_recipes_display, load_raw_recipes

import pandas as pd
import numpy as np
import numba

recipes_df_similarity = load_processed_recipes_similarity(data_folder_path=os.path.join('data', 'processed'))
recipes_df_display = load_processed_recipes_display(data_folder_path=os.path.join('data', 'processed'))

@numba.jit(nopython=True, parallel=True)
def fast_cosine_matrix(u, M):
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
    u = recipes_df_similarity.iloc[:, 1:][recipes_df_similarity["id"]==recipe_id].to_numpy().squeeze()
    M = recipes_df_similarity.iloc[:, 1:].to_numpy()
    
    res = fast_cosine_matrix(u, M)
    res = np.argsort(res)[-(top_n+1):][:-1]
    return list(recipes_df_similarity.iloc[res].id)

def get_recommended_recipes(recipe_ids, top_n=5):
    recommended_recipes = recipes_df_display[:0]
    
    for id in recipe_ids:
        ids = get_top_n_recipe_ids(id, top_n)
        temp = recipes_df_display[recipes_df_display["id"].isin(ids)]
        recommended_recipes = pd.concat([recommended_recipes, temp])
    
    recommended_recipes = recommended_recipes.drop_duplicates()
    recommended_recipes = recommended_recipes.reset_index(drop=True)
    
    return recommended_recipes