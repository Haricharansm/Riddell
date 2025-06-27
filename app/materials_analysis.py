import streamlit as st
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

@st.cache_data
def load_data():
    return pd.read_excel("assets/Materials_Testing_Data.xlsx")

def run():
    st.header("Materials Analysis with ML Predictions & Optimal Recommendations")

    df = load_data()

    st.subheader("Select Filters to Analyze Best Materials")

    foam_type = st.multiselect("Foam Type", options=df['foamType'].unique())
    shell_material = st.multiselect("Shell Material", options=df['shellMaterial'].unique())

    filtered_df = df.copy()
    if foam_type:
        filtered_df = filtered_df[filtered_df['foamType'].isin(foam_type)]
    if shell_material:
        filtered_df = filtered_df[filtered_df['shellMaterial'].isin(shell_material)]

    if not filtered_df.empty:
        st.dataframe(filtered_df[['foamType', 'foamDensity', 'foamThickness', 'shellMaterial', 'shellThickness', 'compressionResistance', 'energyAbsorption', 'durabilityScore', 'weight', 'cost', 'temperatureStability', 'moistureResistance']])

        st.subheader("ML Predictions")

        features = filtered_df[['foamDensity', 'foamThickness', 'shellThickness', 'compressionResistance', 'weight', 'cost']]
        durability_target = filtered_df['durabilityScore']
        energy_target = filtered_df['energyAbsorption']

        X_train_dur, X_test_dur, y_train_dur, y_test_dur = train_test_split(features, durability_target, test_size=0.2, random_state=42)
        model_dur = LinearRegression()
        model_dur.fit(X_train_dur, y_train_dur)

        X_train_en, X_test_en, y_train_en, y_test_en = train_test_split(features, energy_target, test_size=0.2, random_state=42)
        model_en = LinearRegression()
        model_en.fit(X_train_en, y_train_en)

        st.subheader("Predict Durability and Energy Absorption")
        input_data = {}
        for col in features.columns:
            input_data[col] = st.number_input(f"{col}", float(features[col].min()), float(features[col].max()), float(features[col].mean()))
        input_df = pd.DataFrame([input_data])

        pred_dur = model_dur.predict(input_df)[0]
        pred_en = model_en.predict(input_df)[0]

        st.success(f"Predicted Durability Score: {pred_dur:.2f}")
        st.success(f"Predicted Energy Absorption: {pred_en:.2f}")

        st.subheader("Optimal Material Recommendations")
        # Define custom weighted score: prioritize high durability & absorption, low cost & weight
        filtered_df['optimalScore'] = (
            (filtered_df['durabilityScore'] * 0.4) +
            (filtered_df['energyAbsorption'] * 0.4) -
            (filtered_df['cost'] * 0.1) -
            (filtered_df['weight'] * 0.1)
        )
        top_materials = filtered_df.sort_values(by='optimalScore', ascending=False).head(5)
        st.write("Top Recommended Materials:")
        st.dataframe(top_materials[['foamType', 'shellMaterial', 'durabilityScore', 'energyAbsorption', 'weight', 'cost', 'optimalScore']])

    else:
        st.warning("No data matching the selected filters.")

    st.caption("Data, ML predictions, and optimal recommendations based on lab material testing for Riddell helmet prototypes.")
