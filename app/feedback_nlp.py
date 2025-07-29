# app/feedback_nlp.py
import streamlit as st
import pandas as pd
import re

# Simple sentiment dictionaries
POSITIVE_WORDS = {"good", "great", "excellent", "comfortable", "lightweight", "love", "perfect", "well-fitting"}
NEGATIVE_WORDS = {"bad", "poor", "uncomfortable", "tight", "loose", "pain", "hurt", "discomfort", "heavy", "hate"}

def analyze_feedback(feedback_text):
    """Extract sentiment and key themes from customer feedback without NLTK or TextBlob."""
    
    words = re.findall(r'\b\w+\b', feedback_text.lower())
    positive_count = sum(1 for w in words if w in POSITIVE_WORDS)
    negative_count = sum(1 for w in words if w in NEGATIVE_WORDS)

    # Determine sentiment
    if positive_count > negative_count:
        sentiment_label = "😊 Positive"
    elif negative_count > positive_count:
        sentiment_label = "⚠️ Negative"
    else:
        sentiment_label = "😐 Neutral"

    # Common helmet-related issues
    common_issues = [w for w in words if w in [
        "fit", "comfort", "tight", "loose", "strap", "foam", "pressure",
        "durability", "impact", "chin", "ventilation", "weight"
    ]]
    
    keywords_found = list(set(common_issues))

    return sentiment_label, keywords_found


def run():
    st.header("🗣️ Customer Feedback Insights")

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

        # Summary KPIs
        positive_count = (results_df['Sentiment'] == "😊 Positive").sum()
        negative_count = (results_df['Sentiment'] == "⚠️ Negative").sum()
        neutral_count = (results_df['Sentiment'] == "😐 Neutral").sum()

        st.metric("Positive Feedback", positive_count)
        st.metric("Negative Feedback", negative_count)
        st.metric("Neutral Feedback", neutral_count)

        # Insights Summary
        st.subheader("💡 Overall Insights")
        all_keywords = set()
        for kw in results_df['Key Themes']:
            if kw != "N/A":
                all_keywords.update(kw.split(", "))
        if all_keywords:
            st.write(f"Players report common issues with: **{', '.join(all_keywords)}**")
        else:
            st.write("No recurring issues found in feedback.")

    else:
        st.info("⬆️ Please upload a feedback CSV file to begin analysis.")
