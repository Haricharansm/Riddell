import streamlit as st
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import shap

@st.cache_data
def load_data():
    return pd.read_excel("assets/Safety Performance Data.xlsx")

def run():
    st.header("Safety Performance Analysis with Explainable AI for Compliance")

    df = load_data()

    st.subheader("Filter Test Data")

    helmet_model = st.multiselect("Helmet Model", options=df['helmetModel'].unique())
    condition = st.multiselect("Condition", options=df['condition'].unique())

    filtered_df = df.copy()
    if helmet_model:
        filtered_df = filtered_df[filtered_df['helmetModel'].isin(helmet_model)]
    if condition:
        filtered_df = filtered_df[filtered_df['condition'].isin(condition)]

    if not filtered_df.empty:
        st.dataframe(filtered_df[['testDate', 'helmetModel', 'condition', 'dropHeight', 'impactVelocity', 'peakDeceleration', 'HIC15', 'rotationalAccel', 'energyTransferred', 'reboundVelocity', 'pass', 'temperature', 'relativeHumidity']])

        st.subheader("Safety Insights")

        avg_hic = filtered_df['HIC15'].mean()
        avg_peak_dec = filtered_df['peakDeceleration'].mean()
        pass_rate = filtered_df['pass'].value_counts(normalize=True).get(True, 0) * 100

        st.metric("Average HIC15", f"{avg_hic:.2f}")
        st.metric("Average Peak Deceleration (g)", f"{avg_peak_dec:.2f}")
        st.metric("Pass Rate (%)", f"{pass_rate:.2f}%")

        st.subheader("Predict Compliance Pass/Fail with Explanations")

        feature_cols = ['dropHeight', 'impactVelocity', 'peakDeceleration', 'HIC15', 'rotationalAccel', 'energyTransferred', 'reboundVelocity', 'temperature', 'relativeHumidity']
        X = filtered_df[feature_cols]
        y = filtered_df['pass']

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)

        st.markdown("### Predict for New Test")
        input_data = {}
        for col in feature_cols:
            input_data[col] = st.number_input(f"{col}", float(X[col].min()), float(X[col].max()), float(X[col].mean()))

        input_df = pd.DataFrame([input_data])
        prediction = model.predict(input_df)[0]
        prob = model.predict_proba(input_df)[0]

        st.success(f"Predicted Compliance Result: {'Pass' if prediction else 'Fail'}")
        st.write("Confidence:", { 'Fail': f"{prob[0]*100:.2f}%", 'Pass': f"{prob[1]*100:.2f}%" })

        st.subheader("Explainable AI (SHAP) Output")
        explainer = shap.TreeExplainer(model)
        shap_values = explainer.shap_values(input_df)
        st.write("Feature Impact Summary:")
        for i, col in enumerate(feature_cols):
            st.write(f"{col}: {shap_values[1][0][i]:.4f}")

        st.success("✅ Compliance model trained with explainable AI outputs provided for regulatory review.")
    else:
        st.warning("No data matching the selected filters.")

    st.caption("Data analysis, compliance prediction, and explainability based on helmet safety test performance logs.")
