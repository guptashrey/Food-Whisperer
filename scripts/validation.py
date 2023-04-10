import os
import pandas as pd
import numpy as np
from data_processing import load_processed_recipes_similarity
from inference import get_top_n_recipe_ids
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics import mean_squared_error

def predict_rating(user_recipe_pair, simtable, Xtrain, ytrain):
    # Extract the user_id and recipe_id from the user_recipe_pair
    user_id = user_recipe_pair['u']
    recipe_id = user_recipe_pair['i']
    # Get all the recipes the user has already rated
    recipes_rated_by_user = Xtrain.loc[Xtrain['u']==user_id, 'i'].tolist()
    simtable_filtered = simtable.loc[recipe_id,recipes_rated_by_user]
    # Get the most similar recipe already rated to current recipe to rate
    most_similar_rating = simtable_filtered.index[np.argmax(simtable_filtered)]
    # Get user's rating for most similar recipe
    idx = Xtrain.loc[(Xtrain['u']==user_id) & (Xtrain['i']==most_similar_rating)].index.values[0]
    most_similar_rating = ytrain.loc[idx]
    return most_similar_rating


if __name__ == "__main__":
    # Load the data
    print("Loading data...")
    interactions_val_df = pd.read_csv(os.path.join("..", "data", "raw", "interactions_train.csv"))
    interactions_test_df = pd.read_csv(os.path.join("..", "data", "raw", "interactions_test.csv"))
    recipes_df_processed = load_processed_recipes_similarity(data_folder_path=os.path.join("..", "data", "processed"))

    # Use only 10000 recipes
    recipes_df_processed = recipes_df_processed.iloc[:10000,:]
    interactions_val_df = interactions_val_df.loc[interactions_val_df['i'].isin(recipes_df_processed['id']),:]
    interactions_test_df = interactions_test_df.loc[interactions_test_df['i'].isin(recipes_df_processed['id']),:]
    
    
    # Calculate the similarity matrix
    print("Calculating similarity matrix...")
    csmatrix = cosine_similarity(recipes_df_processed.drop(columns=['id']))
    csmatrix = pd.DataFrame(csmatrix,columns=recipes_df_processed.id,index=recipes_df_processed.id)
    #print(csmatrix.head())

    # Split our data into training and test sets
    print("Splitting data into training and test sets...")
    Xtrain = interactions_val_df[['u', 'i']]
    Xtest = interactions_test_df[['u', 'i']]
    ytrain = interactions_val_df['rating']
    ytest = interactions_test_df['rating']
    
    # Get the predicted ratings for each movie in the validation set and calculate the RMSE
    print("Calculating RMSE...")
    print(Xtest.head())
    print(csmatrix)
    print(177847 in csmatrix.index)
    ratings_valset = Xtest.apply(lambda x: predict_rating(x, simtable=csmatrix, Xtrain=Xtrain, ytrain=ytrain),axis=1)
    val_rmse = np.sqrt(mean_squared_error(ytest,ratings_valset))
    print('RMSE of predicted ratings is {:.3f}'.format(val_rmse))