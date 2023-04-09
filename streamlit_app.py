## Library imports
import pandas as pd 
import numpy as np 
import streamlit as st
from streamlit import runtime

## Local imports
from components import user_profile
from components import recipe_recommender
from components import recommended_recipies
from components import about_us
from config import PAGES

@st.cache_data
def load_data():
    """ 
    Loads the required dataframe into the webapp 

    Args:
        None

    Returns:
        df (pd.DataFrame): The dataframe containing the top 50 popular recipes
    """

    ## Load the top 50 popular recipes
    df = pd.read_csv('data/top_recipes.csv')
    df["selected"]=False

    ## Save the default recommendations
    st.session_state.toprecipies = df.to_dict('records')

    return df

## Set the page tab title
st.set_page_config(page_title="Food Whisper", page_icon="🤖", layout="wide", initial_sidebar_state="collapsed")

## create dataframe from the load function 
df = load_data()

## Landing page UI
def run_UI():
    """
    The main UI function to display the UI for the webapp
    """

    ## Set the page title and navigation bar
    st.sidebar.title('Select Menu')
    if st.session_state["page"]:
        page=st.sidebar.radio('Navigation', PAGES, index=st.session_state["page"])
    else:
        page=st.sidebar.radio('Navigation', PAGES, index=0)
    st.experimental_set_query_params(page=page)


    ## Display the page selected on the navigation bar
    if page == 'About Us':
        st.sidebar.write("""
            ## About
            
            About Us
        """)
        st.title("About Us")
        about_us.about_us_UI()

    elif page == 'Recipe Recommender':
        st.sidebar.write("""
            ## About
            
            The project aims to provide personalized recipe recommendations to users based on their preferences and available ingredients.
            
            Users will select their favorite recipes, and the system will use content-based filtering to suggest similar and popular recipes.
            
            The recommendations will also the user's available ingredients.
        """)
        st.title("Food Whisper")
        recipe_recommender.recipe_recommender_UI(df)
    
    elif page == 'Recommended Recipes':
        st.sidebar.write("""
            ## About
            
            The project aims to provide personalized recipe recommendations to users based on their preferences and available ingredients.
            
            Users will select their favorite recipes, and the system will use content-based filtering to suggest similar and popular recipes.
            
            The recommendations will also the user's available ingredients.
        """)
        st.title("Food Whisper")
        recommended_recipies.recommended_recipes_UI()

    else:
        st.sidebar.write("""
            ## About
            
            The project aims to provide personalized recipe recommendations to users based on their preferences and available ingredients.
            
            Users will select their favorite recipes, and the system will use content-based filtering to suggest similar and popular recipes.
            
            The recommendations will also the user's available ingredients.
        """)
        st.title("Food Whisper")
        user_profile.user_profile_UI(df)


if __name__ == '__main__':
    ## Load the streamlit app with "Recipe Recommender" as default page
    if runtime.exists():

        ## Get the page name from the URL
        url_params = st.experimental_get_query_params()
        if len(url_params.keys()) == 0:
            st.session_state.page = 1

        if 'loaded' not in st.session_state:
            if len(url_params.keys()) == 0:
                ## Set the default page as "Recipe Recommender"
                st.experimental_set_query_params(page='Recipe Recommender')
                url_params = st.experimental_get_query_params()
                st.session_state.page = PAGES.index(url_params['page'][0])
        
        ## Call the main UI function
        run_UI()