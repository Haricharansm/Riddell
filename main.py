import streamlit as st
from app import fit_optimizer, impact_predictor, dashboard, feedback_nlp

st.set_page_config(page_title="Riddell AI Helmet R&D", layout="wide")

st.title("🏈 Riddell AI-Powered Helmet R&D Prototype")

tabs = st.tabs(["Helmet Fit Optimizer", "Impact Risk Predictor", "Testing Dashboard", "Feedback Analyzer"])

with tabs[0]:
    fit_optimizer.run()

with tabs[1]:
    impact_predictor.run()

with tabs[2]:
    dashboard.run()

with tabs[3]:
    feedback_nlp.run()
