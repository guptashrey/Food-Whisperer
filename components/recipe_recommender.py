## Library imports
import streamlit as st
import matplotlib.pyplot as plt


def recipe_recommender_UI(df):
    """
    The main UI function to display the Landing page UI
    """
    st.write("Recipe Recommender")
    st.write("Select a few Recipes you love ... ")

    ## Get the top 30 recipes
    recipes = df.to_dict('records')

    ## Define the recipe columns
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    columns = [col1, col2, col3, col4, col5, col6]
    
    ## Display the top recipes for the user to select
    count = 0
    for recipe in recipes:
        with columns[count]:
            ## Display the recipe image
            st.image(f'./data/images/recipies/{recipe["image"]}', use_column_width=True)

            ## Display the recipe title and checkbox
            recipe["selected"] = st.checkbox(recipe["title"])
            
            ## Increment the column count
            count += 1
            if count >= 6:
                count = 0


    if st.button('Recommend Recipes'):
        print(recipes)
        
