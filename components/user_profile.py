import logging
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st
from streamlit_card import card

## Initiate logging
logger = logging.getLogger(__name__)

def user_profile_UI(df):
    """
    The main UI function to display the Landing page UI
    """
    st.write("Select ingredients available at home to cook your meal today ... ")

    # Define the recipe cards
    recipes = [
        {
            "title": "Spaghetti Carbonara",
            "image": "https://placekitten.com/500/500",
        },
        {
            "title": "Chicken Tikka Masala",
            "image": "https://placekitten.com/500/500",
        },
        {
            "title": "Beef Stroganoff",
            "image": "https://placekitten.com/500/500",
        },
        {
            "title": "Rajma Chawal",
            "image": "https://placekitten.com/500/500",
        },
        {
            "title": "Paneer Tikka Masala",
            "image": "https://placekitten.com/500/500",
        },
        {
            "title": "Chloley Bhature",
            "image": "https://placekitten.com/500/500",
            "selected": False,
        },
        {
            "title": "Momos",
            "image": "https://placekitten.com/500/500",
            "selected": False,
        },
        {
            "title": "Dosa",
            "image": "https://placekitten.com/500/500",
            "selected": False,
        },
        {
            "title": "Dosa1",
            "image": "https://placekitten.com/500/500",
            "selected": False,
        },
        {
            "title": "Dosa2",
            "image": "https://placekitten.com/500/500",
            "selected": False,
        },
        {
            "title": "Dosa3",
            "image": "https://placekitten.com/500/500",
            "selected": False,
        },
        {
            "title": "Dosa4",
            "image": "https://placekitten.com/500/500",
            "selected": False,
        },
    ]


    col1, col2, col3, col4, col5, col6 = st.columns(6)
    columns = [col1, col2, col3, col4, col5, col6]
    
    count = 0
    for recipe in recipes:
        with columns[count]:
            st.image(recipe["image"], use_column_width=True)
            selected = st.checkbox(recipe["title"])
            count += 1
            if count >= 6:
                count = 0
