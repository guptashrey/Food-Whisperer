## Library imports
import streamlit as st
import matplotlib.pyplot as plt


def recipe_recommender_UI(df):
    """
    The main UI function to display the Landing page UI
    """
    st.write("Recipe Recommender")

def sentiment_classic_explain_UI(unseen_df):
    """
    The main UI function to display the page UI for animal classification
    """
    st.write('''  
        ### Sentiment Analysis using TF-IDF and Random Forest with Explainability      
        ''')
    
    hotel_list = [f"Hotel {i}" for i in unseen_df.index]
    
    with st.container():
        selected_hotel_review = st.selectbox("Select a Review", hotel_list)
        selected_hotel_review_index = int(selected_hotel_review.split(" ")[1])
    
    st.write("Original REVIEW")
    st.write(unseen_df.loc[selected_hotel_review_index, 'Review'])
    
    if st.button('Analyse Review'):
        force_plot, shap_values, top_keywords, top_adjective, review_corrected_text, top_adjective_shap, remaining_adjectives, pred_class = 0 #run_pipiline(instance=int(selected_hotel_review_index))
        
        ## Display the grammar corrected review
        st.write("Grammar Corrected REVIEW")
        st.write(review_corrected_text)

        ## Display the sentiment
        st.write("Predicted Sentiment")
        if pred_class == 1:
            st.success("Positive Sentiment", icon="✅")
        else:
            st.error("Negative Sentiment", icon="🚨")

        ## Display the SHAP plot
        st.write("Sentiment Explanability using SHAP")
        st.pyplot(fig=force_plot ,dpi=200, pad_inches=0)
        plt.clf()

        ## Display the top keywords
        st.write("Few important 'Keywords' contributing to the 'Sentiment'")
        col1, col2, col3, col4 = st.columns(4)
        columns = [col1, col2, col3, col4]
        
        count = 0
        for keyword in top_keywords:
            with columns[count]:
                if count == 0:
                    st.success(keyword)
                else:
                    st.info(keyword)
                count += 1
                if count >= 4:
                    count = 0

        ## Display what the top adjective describe in the review
        st.write("What do the 'Most Important Adjectives' describe?")
        #st.write(top_adjective_shap)
        col2_1, col2_2, col2_3, col2_4 = st.columns(4)
        columns_2 = [col2_1, col2_2, col2_3, col2_4]
        count_2 = 0
        for adj, noun in top_adjective_shap:
            with columns_2[count_2]:
                st.error(f"{adj} -> {noun}")
                count_2 += 1
                if count_2 >= 4:
                    count_2 = 0

        ## Display what the other adjectives descrbe in the review
        st.write("What do the 'Other Adjectives' describe?")
        #st.write(remaining_adjectives)
        col3_1, col3_2, col3_3, col3_4 = st.columns(4)
        columns_3 = [col3_1, col3_2, col3_3, col3_4]
        count_3 = 0
        for adj, dependency in remaining_adjectives:
            with columns_3[count_3]:
                st.warning(f"{adj} -> {dependency}")
                count_3 += 1
                if count_3 >= 4:
                    count_3 = 0