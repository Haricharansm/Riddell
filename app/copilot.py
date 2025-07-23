# app/copilot.py
import streamlit as st
import random

def run():
    st.sidebar.title("🧠 Smart Assistant")

    question = st.sidebar.text_input("Ask a question about helmet R&D data...")

    if st.sidebar.button("Ask"):
        if not question.strip():
            st.sidebar.warning("Please enter a valid question.")
        else:
            st.sidebar.info("🔍 Analyzing...")

            # Placeholder answers (to be replaced with real logic or LLM integration)
            sample_responses = [
                "The average comfort rating has decreased slightly over the last quarter. Consider reviewing foam selection.",
                "Cluster 2 shows promising material durability and fit metrics. You may want to prioritize its development.",
                "Testing pass rate is below 95%. Immediate review of shell material in helmetModel-A is recommended.",
                "Based on recent feedback, chin strap tension is a recurring issue in smaller sizes."
            ]
            st.sidebar.success(random.choice(sample_responses))
