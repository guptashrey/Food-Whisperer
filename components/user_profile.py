import logging
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st

## Initiate logging
logger = logging.getLogger(__name__)

def user_profile_UI(df):
    """
    The main UI function to display the Landing page UI
    """
    st.write("User Profile Setup")