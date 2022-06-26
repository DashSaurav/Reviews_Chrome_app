import streamlit as st
import pandas as pd 
from textblob import TextBlob

st.header("Reviews Sentiment Look Up")
st.sidebar.warning("Please Provide Password and then upload the **Reviews.csv** file in Below Space.")

def check_password():
    s1,s2,s3 = st.columns(3)
    with s2:
        def password_entered():
            """Checks whether a password entered by the user is correct."""
            if st.session_state["password"] == st.secrets["password"]:
                st.session_state["password_correct"] = True
                del st.session_state["password"]  # don't store password
            else:
                st.session_state["password_correct"] = False

        if "password_correct" not in st.session_state:
            # First run, show input for password.
            st.text_input(
                "Please Write Your Password", type="password", on_change=password_entered, key="password"
            )
            return False
        elif not st.session_state["password_correct"]:
            # Password not correct, show input + error.
            st.text_input(
                "Please Write Your Password", type="password", on_change=password_entered, key="password"
            )
            st.error("😕 Password incorrect")
            return False
        else:
            # Password correct.
            return True

if check_password():
    uploaded_file = st.sidebar.file_uploader('Browse file', type = ['csv'])
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        # loading the data into a csv file and stroing it for further use.
        st.sidebar.info("After sucessfully uploaded the csv file click on Load Data to transform the csv into the desired data")

        if st.button("Load Data"):
            # st.dataframe(df)
            df.to_csv('data/main_data.csv', index=False)

            df_start = df[['ID','Text','Star']]
            df_start = df_start[df_start.Star != 5]
            df_start = df_start[df_start.Star != 4]
            df_start = df_start[df_start.Star != 3]

            # use textblob for sentiment category.
            list_sentiment = []
            for i in df_start["Text"]:
                score = TextBlob(i).sentiment[0]
                if (score > 0):
                    list_sentiment.append('Positive')
                elif (score < 0):
                    list_sentiment.append('Negative')
                else:
                    list_sentiment.append('Neutral')
            df_start["Sentiment"]=list_sentiment
            df_start = df_start[df_start.Sentiment == 'Positive']

            df_new = df[['ID','Review URL','User Name','Review Date']]
            df_merge = pd.merge(df_start, df_new, on="ID")
            st.subheader("List of Positive Comments with Low Rating")
            st.dataframe(df_merge)

            # st.dataframe(df_new)