import streamlit as st
from app import fit_optimizer, impact_predictor, dashboard, feedback_nlp, concept_recommender, voting, product_tracker, admin_approval

st.set_page_config(page_title="Riddell AI Helmet R&D", layout="wide")

# ------------------ LOGIN ------------------
if "role" not in st.session_state:
    st.title("🔐 Riddell R&D Access Portal")
    user = st.selectbox("Select your role", ["R&D Lead", "Analyst", "Engineer"])
    if st.button("Login"):
        st.session_state.role = user
        st.experimental_rerun()
    st.stop()

# ------------------ HEADER ------------------
st.image("assets/riddell_logo.png", width=200)
st.title("\U0001F3C8 Riddell AI-Powered Helmet R&D Prototype")

role = st.session_state.role
st.sidebar.success(f"Logged in as: {role}")

# ------------------ ROLE-BASED TABS ------------------
tabs = []
modules = []

# Everyone has access to these
tabs.append("Helmet Fit Optimizer")
modules.append(fit_optimizer.run)

tabs.append("Impact Risk Predictor")
modules.append(impact_predictor.run)

# Analysts and Leads
if role in ["R&D Lead", "Analyst"]:
    tabs += [
        "Testing Dashboard",
        "Feedback Analyzer",
        "Concept Recommendations"
    ]
    modules += [
        dashboard.run,
        feedback_nlp.run,
        concept_recommender.run
    ]

# R&D Lead Only
if role == "R&D Lead":
    tabs += [
        "Voting & Prioritization",
        "Project Lifecycle Tracker",
        "Admin Approvals"
    ]
    modules += [
        voting.run,
        product_tracker.run,
        admin_approval.run
    ]

# Render selected tabs
selected_tab = st.tabs(tabs)
for i, tab in enumerate(selected_tab):
    with tab:
        modules[i]()
