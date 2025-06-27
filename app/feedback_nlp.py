import streamlit as st
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk import word_tokenize

nltk.download('punkt')
nltk.download('vader_lexicon')

def run():
    st.header("Player & Coach Feedback Analyzer with NLP")

    feedback = st.text_area("Enter Player or Coach Feedback")

    if feedback:
        st.subheader("Keyword Extraction")
        tokens = word_tokenize(feedback)
        st.write(list(set(tokens)))

        st.subheader("Sentiment Scoring")
        sia = SentimentIntensityAnalyzer()
        sentiment = sia.polarity_scores(feedback)
        st.write(sentiment)

        st.subheader("Overall Insight")
        if sentiment['compound'] > 0.2:
            st.success("Positive Feedback")
        elif sentiment['compound'] < -0.2:
            st.error("Negative Feedback")
        else:
            st.warning("Neutral Feedback")

    else:
        st.info("Please enter feedback for analysis.")
