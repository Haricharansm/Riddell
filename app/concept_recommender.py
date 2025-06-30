import streamlit as st
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

@st.cache_data
def load_data():
    fit_df = pd.read_excel("assets/Player Fit & Comfort Data.xlsx")
    materials_df = pd.read_excel("assets/Materials Testing Data.xlsx")
    safety_df = pd.read_excel("assets/Safety Performance Data.xlsx")
    
    # Clean column names
    fit_df.columns = fit_df.columns.str.strip()
    materials_df.columns = materials_df.columns.str.strip()
    safety_df.columns = safety_df.columns.str.strip()
    
    return fit_df, materials_df, safety_df

def run():
    st.header("🤖 AI Concept Recommendation Engine (ML-Based Prototype)")

    fit_df, materials_df, safety_df = load_data()

    st.subheader("Generating ML-based concept recommendations")

    # Merge relevant dataframes for clustering analysis
    merged_df = pd.merge(fit_df, materials_df, how='cross')

    # Select features for clustering
    features = merged_df[['comfortRating', 'durabilityScore', 'energyAbsorption', 'temperatureStability']]
    features = features.dropna()

    # Standardize features
    scaler = StandardScaler()
    scaled_features = scaler.fit_transform(features)

    # KMeans clustering
    k = st.slider("Select number of clusters (design concepts)", 2, 10, 3)
    kmeans = KMeans(n_clusters=k, random_state=42)
    kmeans.fit(scaled_features)

    merged_df['Cluster'] = kmeans.labels_

    # Generate concept recommendations per cluster centroid
    st.subheader("Recommended Concepts per Cluster")

    concepts = []
    for cluster_id in range(k):
        cluster_data = merged_df[merged_df['Cluster'] == cluster_id]

        # Get representative concept (e.g. median values)
        if not cluster_data.empty:
            concept = {
                'Cluster': cluster_id,
                'Helmet Size': cluster_data['helmetSize'].mode()[0] if 'helmetSize' in cluster_data else 'N/A',
                'Avg Comfort Rating': cluster_data['comfortRating'].mean(),
                'Foam Type': cluster_data['foamType'].mode()[0],
                'Shell Material': cluster_data['shellMaterial'].mode()[0],
                'Avg Durability': cluster_data['durabilityScore'].mean(),
                'Avg Energy Absorption': cluster_data['energyAbsorption'].mean(),
                'Avg Temp Stability': cluster_data['temperatureStability'].mean()
            }
            concepts.append(concept)

    concept_df = pd.DataFrame(concepts)
    st.dataframe(concept_df)

    # Natural language summary output
    st.subheader("📢 Concept Recommendations Summary (Natural Language)")

    if not concept_df.empty:
        for idx, row in concept_df.iterrows():
            recommendation = (
                f"**Cluster {row['Cluster']} Recommendation:**  \n"
                f"We recommend developing a **{row['Helmet Size']} helmet** using **{row['Foam Type']} foam** "
                f"combined with a **{row['Shell Material']} shell**. "
                f"This design offers an average comfort rating of **{row['Avg Comfort Rating']:.1f}**, "
                f"durability score of **{row['Avg Durability']:.1f}**, "
                f"and energy absorption of **{row['Avg Energy Absorption']:.1f}**, "
                f"with temperature stability of **{row['Avg Temp Stability']:.1f}**. "
                f"This concept is positioned to enhance player comfort while maintaining strong impact protection and material resilience."
            )
            st.markdown(recommendation)
    else:
        st.warning("No concept recommendations generated. Adjust data inputs or clustering parameters.")

