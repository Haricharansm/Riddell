import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report

@st.cache_data
def load_data():
    df = pd.read_excel("assets/Impact & Collision Data.xlsx")
    return df.dropna()

@st.cache_resource
def train_model(df):
    categorical = ['position', 'helmetModel', 'impactType', 'gamePhase']
    numerical = ['peakAcceleration', 'duration', 'rotationalVelocity',
                 'impactLocation.x', 'impactLocation.y', 'impactLocation.z',
                 'temperature', 'humidity']
    target = 'injuryReported'

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
    st.header("Impact Risk Predictor")

    df = load_data()
    model = train_model(df)

    st.subheader("Enter Impact Test Parameters")

    input_data = {
        'position': st.selectbox("Player Position", df['position'].unique()),
        'helmetModel': st.selectbox("Helmet Model", df['helmetModel'].unique()),
        'impactType': st.selectbox("Impact Type", df['impactType'].unique()),
        'gamePhase': st.selectbox("Game Phase", df['gamePhase'].unique()),
        'peakAcceleration': st.slider("Peak Acceleration (g)", 30.0, 150.0, 75.0),
        'duration': st.slider("Impact Duration (ms)", 1, 100, 30),
        'rotationalVelocity': st.slider("Rotational Velocity (rad/s)", 0.0, 100.0, 45.0),
        'impactLocation.x': st.slider("Impact X", -1.0, 1.0, 0.0),
        'impactLocation.y': st.slider("Impact Y", -1.0, 1.0, 0.0),
        'impactLocation.z': st.slider("Impact Z", -1.0, 1.0, 0.0),
        'temperature': st.slider("Temperature (°C)", -10.0, 50.0, 20.0),
        'humidity': st.slider("Humidity (%)", 0.0, 100.0, 50.0)
    }

    input_df = pd.DataFrame([input_data])
    prediction = model.predict(input_df)[0]
    proba = model.predict_proba(input_df)[0]

    st.success(f"🧠 Predicted Concussion Risk: **{'Yes' if prediction else 'No'}**")
    st.write("Confidence:", {
        'No Injury': f"{proba[0]*100:.2f}%",
        'Injury': f"{proba[1]*100:.2f}%"
    })

    st.caption("Model trained on full historical impact dataset with environmental and biomechanical variables.")
