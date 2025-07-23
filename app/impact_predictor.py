import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

@st.cache_data
def load_data():
    df = pd.read_excel("assets/Impact & Collision Data.xlsx")
    df.columns = df.columns.str.strip()
    return df.dropna()

@st.cache_resource
def train_model(df):
    categorical = ['position', 'helmetModel', 'impactType', 'gamePhase']
    numerical = ['peakAcceleration', 'duration', 'rotationalVelocity', 'temperature', 'humidity']
    target = 'injuryReported'

    expected_columns = categorical + numerical + [target]
    missing = [col for col in expected_columns if col not in df.columns]
    if missing:
        st.error(f"❌ Missing columns in dataset: {missing}")
        return None

    X = df[categorical + numerical]
    y = df[target]

    preprocessor = ColumnTransformer([
        ('num', StandardScaler(), numerical),
        ('cat', OneHotEncoder(handle_unknown='ignore'), categorical)
    ])

    clf = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('classifier', RandomForestClassifier(n_estimators=100, random_state=42))
    ])

    clf.fit(X, y)
    return clf

def run():
    st.header("🚨 Impact Risk Predictor")

    role = st.session_state.get("user_role", "analyst")  # 'executive', 'trainer', 'analyst'

    df = load_data()
    model = train_model(df)

    if model is None:
        st.stop()

    with st.form("impact_form"):
        st.subheader("🏈 Player & Scenario Details")
        col1, col2 = st.columns(2)
        with col1:
            position = st.selectbox("Player Position", df['position'].unique())
            helmet_model = st.selectbox("Helmet Model", df['helmetModel'].unique())
        with col2:
            impact_type = st.selectbox("Impact Type", df['impactType'].unique())
            game_phase = st.selectbox("Game Phase", df['gamePhase'].unique())

        st.subheader("📐 Biomechanical & Environmental Metrics")
        col3, col4, col5 = st.columns(3)
        with col3:
            peak_accel = st.slider("Peak Acceleration (g)", 30.0, 150.0, 75.0)
            duration = st.slider("Impact Duration (ms)", 1, 100, 30)
        with col4:
            rotational_velocity = st.slider("Rotational Velocity (rad/s)", 0.0, 100.0, 45.0)
            temperature = st.slider("Temperature (°C)", -10.0, 50.0, 20.0)
        with col5:
            humidity = st.slider("Humidity (%)", 0.0, 100.0, 50.0)

        submitted = st.form_submit_button("🧠 Predict Risk")

    if submitted:
        input_df = pd.DataFrame([{
            'position': position,
            'helmetModel': helmet_model,
            'impactType': impact_type,
            'gamePhase': game_phase,
            'peakAcceleration': peak_accel,
            'duration': duration,
            'rotationalVelocity': rotational_velocity,
            'temperature': temperature,
            'humidity': humidity
        }])

        try:
            prediction = model.predict(input_df)[0]
            proba = model.predict_proba(input_df)[0]

            st.success(f"🎯 Predicted Concussion Risk: **{'Yes' if prediction else 'No'}**")
            st.metric("No Injury Confidence", f"{proba[0]*100:.2f}%")
            st.metric("Injury Risk Confidence", f"{proba[1]*100:.2f}%")

            if role in ["analyst", "trainer"]:
                st.info("ℹ️ Consider re-running with alternate helmets or reducing peak acceleration for better outcomes.")

            if role == "executive":
                st.markdown("""
                    ### Recommendation:
                    - High injury risk → re-evaluate helmet model or position-specific fit
                    - Consider enhanced training protocols or playstyle adjustments
                """)

        except Exception as e:
            st.error(f"⚠️ Prediction failed: {e}")

    st.caption("📊 Model trained using Random Forest on historical game impact data.")
