import streamlit as st
import pandas as pd

@st.cache_data
def load_data():
    return pd.read_excel("assets/Player Fit & Comfort Data.xlsx")

def run():
    st.header("Helmet Fit Optimizer")

    df = load_data()

    st.subheader("Enter Player Head Profile")

    head_circumference = st.slider("Head Circumference (cm)", 50, 65, 58)
    head_length = st.slider("Head Length (cm)", 16, 24, 20)
    head_width = st.slider("Head Width (cm)", 13, 20, 17)

    filtered_df = df[
        (df['headCircumference'].between(head_circumference - 2, head_circumference + 2)) &
        (df['headLength'].between(head_length - 1, head_length + 1)) &
        (df['headWidth'].between(head_width - 1, head_width + 1))
    ]

    if not filtered_df.empty:
        recommendation = filtered_df.sort_values(by='fitScore', ascending=False).iloc[0]
        st.success(f"🧢 Recommended Helmet Size: **{recommendation['helmetSize']}**")
        st.write("- Comfort Rating:", recommendation['comfortRating'])
        st.write("- Pressure Points:", recommendation['pressurePoints'])
        st.write("- Chin Strap Tension:", recommendation['chinStrapTension'])
    else:
        st.warning("No exact match found. Consider scanning player data.")

    st.caption("Model based on historical fit comfort analysis from Riddell trials.")
