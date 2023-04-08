## Library imports
import streamlit as st
import matplotlib.pyplot as plt
from config import PAGES

def recipe_recommender_UI(df):
    """
    The main UI function to display the Landing page UI
    """
    st.divider()
    st.header('Select a few Recipes you love ... ')

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

    ## Add css to the button
    st.markdown("""
                <style>
                div.stButton > button:first-child {
                    background-color: #0099ff;
                    color:#ffffff;
                }
                div.stButton > button:hover {
                    background-color: #03fc88;
                    color:#ff0000;
                    }
                </style>""", unsafe_allow_html=True)
    
    col4, col5, col6 = st.columns([1, 1.5, 1])
    with col5:
        if st.button('Recommend Recipes', use_container_width=True):
            ## Get the selected recipes
            seleted_recipied = [recipe for recipe in recipes if recipe["selected"]]

            ## Save the selected recipes to the session state
            st.session_state.toprecipies = seleted_recipied
            
            ## Move to recommended recipes page
            st.session_state["page"] = 2
            
            ## Confirm the selection
            st.button('Confirm', use_container_width=True)
        
