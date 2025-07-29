# app/feedback_nlp.py
import streamlit as st
import pandas as pd
import re
from textblob import TextBlob

def analyze_feedback(feedback_text):
    """Extract sentiment and key themes from customer feedback without NLTK."""
    
    # --- Sentiment Analysis ---
    blob = TextBlob(feedback_text)
    sentiment = blob.sentiment.polarity  # -1 (negative) to +1 (positive)

    if sentiment > 0.2:
        sentiment_label = "😊 Positive"
    elif sentiment < -0.2:
        sentiment_label = "⚠️ Negative"
    else:
        sentiment_label = "😐 Neutral"

    # --- Keyword Extraction (simple frequency) ---
    words = re.findall(r'\b\w+\b', feedback_text.lower())
    common_issues = [w for w in words if w in [
        "fit", "comfort", "tight", "loose", "strap", "foam", "pressure",
        "durability", "impact", "chin", "ventilation", "weight"
    ]]
    
    keywords_found = list(set(common_issues))

    return sentiment_label, keywords_found


def run():
    st.header("🗣️ Customer Feedback Insights")

    st.write("Upload player/customer feedback to extract insights and sentiment.")

    uploaded_file = st.file_uploader("Upload CSV", type=["csv"])
    if uploaded_file:
        try:
            df = pd.read_csv(uploaded_file)
        except Exception:
            st.error("❌ Failed to read CSV file. Ensure it's in proper format.")
            return

        if 'feedback' not in df.columns:
            st.error("❌ CSV must have a 'feedback' column.")
            return

        st.subheader("📊 Feedback Analysis")
        results = []
        for feedback in df['feedback'].dropna():
            sentiment_label, keywords = analyze_feedback(feedback)
            results.append({
                "Feedback": feedback,
                "Sentiment": sentiment_label,
                "Key Themes": ", ".join(keywords) if keywords else "N/A"
            })

        results_df = pd.DataFrame(results)
        st.dataframe(results_df)

        # --- Summary KPI ---
        positive_count = (results_df['Sentiment'] == "😊 Positive").sum()
        negative_count = (results_df['Sentiment'] == "⚠️ Negative").sum()
        neutral_count = (results_df['Sentiment'] == "😐 Neutral").sum()

        st.metric("Positive Feedback", positive_count)
        st.metric("Negative Feedback", negative_count)
        st.metric("Neutral Feedback", neutral_count)

        # --- Insights Summary ---
        st.subheader("💡 Overall Insights")
        st.write(f"Players report common issues with: **{', '.join(results_df['Key Themes'].unique())}**")
        st.caption("Insights derived from historical Riddell helmet trial feedback.")

    else:
        st.info("⬆️ Please upload a feedback CSV file to begin analysis.")
