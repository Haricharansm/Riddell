import streamlit as st
from app import fit_optimizer, impact_predictor, dashboard, feedback_nlp, concept_recommender, voting, admin_approval, product_tracker

st.set_page_config(page_title="Riddell AI Helmet R&D", layout="wide")

# Display Riddell logo
st.image("assets/riddell_logo.png", width=200)  # Adjust width as needed

st.title("🏈 Riddell AI-Powered Helmet R&D Prototype")

tabs = st.tabs([
    "Helmet Fit Optimizer",
    "Impact Risk Predictor",
    "Testing Dashboard",
    "Feedback Analyzer",
    "Concept Recommendations",
    "Voting & Prioritization",
    "Admin Approvals",
    "Product Lifecycle Tracker"
])

with tabs[0]:
    fit_optimizer.run()

with tabs[1]:
    impact_predictor.run()

with tabs[2]:
    dashboard.run()

with tabs[3]:
    feedback_nlp.run()

with tabs[4]:
    concept_recommender.run()

with tabs[5]:
    voting.run()

with tabs[6]:
    admin_approval.run()

with tabs[7]:
    product_tracker.run()

