## Library imports
import streamlit as st
import matplotlib.pyplot as plt
import ast


def recommended_recipes_UI():
    """
    The main UI function to display the recommended recipes page
    """
    st.divider()
    st.header('Check these recipies out ... ')

    ## Get the top recommended recipes
    recipes = st.session_state.toprecipies
    
    ## Display the top recipes to the user
    counter = 1
    for recipe in recipes:
        with st.container():
            col1, col2 = st.columns([1, 3])

            ## Display the recipe image    
            with col1:
                st.image(f'./data/images/recomended_recipies/{counter}.jpg', use_column_width=True)
                counter = counter + 1
                if counter > 4:
                    counter = 1

            ## Display the recipe title
            with col2:
                with st.container():
                    col6, col7 = st.columns([2, 1])
                    with col6:
                        st.subheader(recipe["corrected_name"])
                    with col7:
                        st.write(f'<div style="text-align:right"><a href="{recipe["url"]}" style="color:#ccc1c0;">View Recipe</a></div>', unsafe_allow_html=True)
                
                with st.container():
                    col3, col4, col5 = st.columns([1, 1, 1])

                    ## Display the recipe cuisine and calories
                    with col3:
                        if recipe["cuisine"] == '-':
                            cuisine = 'Unknown'
                        else:
                            cuisine = ", ".join(ast.literal_eval(recipe["cuisine"]))
                        st.info(f'Cuisine: {cuisine}', icon="🧑‍🍳")
                        st.success(f'Calories: {recipe["calories"]} Kcal', icon="✅")
                    
                    ## Display the recipe time to cook and number of steps
                    with col4:
                        st.error(f'Time to Cook: {recipe["minutes"]} Mins', icon="🔥")
                        st.error(f'Num of Steps: {recipe["n_steps"]} Steps', icon="🚨")

                    ## Display the recipe ingredients
                    with col5:
                        st.warning(f'Ingredients: {", ".join(ast.literal_eval(recipe["ingredients"]))}', icon="🍕")            
        
        ## Add css to the recipe container
        st.markdown("""
                    <style>
                        [data-testid="stVerticalBlock"] > [style*="flex-direction: column;"] > [data-testid="stVerticalBlock"] {
                            border: 1px groove black;
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
                    </style>""", unsafe_allow_html=True)
    
    ## Add a go back button
    col4, col5, col6 = st.columns([1, 1.5, 1])
    with col5:
        if st.button('Go Back', use_container_width=True):
            ## Move to back to recipe recommender page
            st.session_state["page"] = 1

            ## Confirm the button click
            st.button('Confirm', use_container_width=True)
    
