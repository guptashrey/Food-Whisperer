## Library imports
import streamlit as st
import matplotlib.pyplot as plt


def recommended_recipes_UI():
    """
    The main UI function to display the Landing page UI
    """
    st.divider()
    st.header('Check these recipies out ... ')

    ## Get the top recommended recipes
    recipes = st.session_state.toprecipies

    
        
    ## Display the top recipes to the user
    for recipe in recipes:
        with st.container():
            col1, col2, col3 = st.columns([1, 2, 1])
            #for recipe in recipes:

            ## Display the recipe image    
            with col1:
                st.image(f'./data/images/recipies/{recipe["image"]}', use_column_width=True)
            ## Display the recipe title
            with col2:
                st.write(recipe["title"])
        
        ## Add css to the recipe container
        st.markdown("""
                    <style>
                        [data-testid="stVerticalBlock"] > [style*="flex-direction: column;"] > [data-testid="stVerticalBlock"] {
                            border: 2px groove black;
                            padding: 10px;
                        }
                    </style>
                    """,
                        unsafe_allow_html=True,
                    )
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
    
    ## Add a go back button
    col4, col5, col6 = st.columns([1, 1.5, 1])
    with col5:
        if st.button('Go Back', use_container_width=True):
            ## Move to back to recipe recommender page
            st.session_state["page"] = 1

            ## Confirm the button click
            st.button('Confirm', use_container_width=True)
    
