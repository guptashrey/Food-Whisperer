## Library imports
import streamlit as st
import matplotlib.pyplot as plt
import requests

from config import PAGES

def recipe_recommender_UI(df):
    """
    The main UI function to display the recipe recommender page
    """
    st.divider()
    st.header('Select 5 Recipes you love ... ')

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
                </style>""", unsafe_allow_html=True)
    
    col4, col5, col6 = st.columns([1, 1.5, 1])
    with col5:
        if st.button('Recommend Recipes', use_container_width=True):
            
            ## Get the recipe ids for recippies selected by user
            seleted_recipie_ids = [recipe["recipe_id"] for recipe in recipes if recipe["selected"]]
            
            ## Fetch the recommended recipies from the API
            with st.spinner('Please wait while we cook some recipe recomdations for you ...'):
                responses = []
                for recipe_id in seleted_recipie_ids:
                    response = requests.get('http://144.202.23.218:8060/search/'+str(recipe_id))
                    responses.extend(response.json())
                
                ## Remove duplicate recipes
                st.session_state.toprecipies = [dict(t) for t in {tuple(d.items()) for d in responses}]
            
            ## Move to recommended recipes page
            st.session_state["page"] = 2
            
            ## Confirm the selection
            st.button('Show Recommended Recipies', use_container_width=True)




            

            
        
