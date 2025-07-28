import streamlit as st
import pandas as pd

@st.cache_data
def load_data():
    try:
        df = pd.read_excel("assets/Player Fit & Comfort Data.xlsx")
        df.columns = df.columns.str.strip()
        return df
    except Exception as e:
        st.error("❌ Failed to load player fit data. Please check the file format or path.")
        return pd.DataFrame()

def run():
    st.header("🧢 Helmet Fit Optimizer")

    role = st.session_state.get("user_role", "fitter")  # 'executive', 'analyst', 'fitter'

    df = load_data()
    if df.empty:
        return

    st.subheader("📋 Enter Player Head Profile")

    with st.form("player_profile_form"):
        col1, col2, col3 = st.columns(3)
        with col1:
            head_circumference = st.slider("Head Circumference (cm)", 50, 65, 58)
        with col2:
            head_length = st.slider("Head Length (cm)", 16, 24, 20)
        with col3:
            head_width = st.slider("Head Width (cm)", 13, 20, 17)

        submitted = st.form_submit_button("🔍 Recommend Helmet")

    if submitted:
        filtered_df = df[
            (df['headCircumference'].between(head_circumference - 2, head_circumference + 2)) &
            (df['headLength'].between(head_length - 1, head_length + 1)) &
            (df['headWidth'].between(head_width - 1, head_width + 1))
        ]

        st.markdown(f"🔎 Matched {len(filtered_df)} historical records based on input profile.")

        if not filtered_df.empty:
            recommendation = filtered_df.sort_values(by='fitScore', ascending=False).iloc[0]
            st.success(f"✅ Recommended Helmet Size: **{recommendation['helmetSize']}**")
            st.metric("Comfort Rating", f"{recommendation['comfortRating']}")
            st.metric("Pressure Points", f"{recommendation['pressurePoints']}")
            st.metric("Chin Strap Tension", f"{recommendation['chinStrapTension']}")

            if role in ["analyst", "executive"]:
                with st.expander("📊 Show Matching Records"):
                    st.dataframe(filtered_df)

        else:
            st.warning("⚠️ No exact match found. Showing top 3 closest matches instead:")

            # Compute Euclidean distance to find closest matches
            df['distance'] = (
                (df['headCircumference'] - head_circumference) ** 2 +
                (df['headLength'] - head_length) ** 2 +
                (df['headWidth'] - head_width) ** 2
            ) ** 0.5

            top_matches = df.sort_values(by='distance').head(3)

            for i, row in top_matches.iterrows():
                st.info(
                    f"🔍 Alternative {i + 1}: Helmet Size **{row['helmetSize']}**\n\n"
                    f"- Fit Score: {row['fitScore']}\n"
                    f"- Comfort Rating: {row['comfortRating']}\n"
                    f"- Pressure Points: {row['pressurePoints']}\n"
                    f"- Chin Strap Tension: {row['chinStrapTension']}\n"
                )

            if role in ["analyst", "executive"]:
                with st.expander("📊 Show Closest Matching Records"):
                    st.dataframe(top_matches.drop(columns=["distance"]))

    st.caption("🔬 This module uses historical player fit & comfort data from Riddell helmet trials.")
