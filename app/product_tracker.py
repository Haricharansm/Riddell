import streamlit as st
import pandas as pd
from datetime import date

# Dummy concepts for demonstration (replace with top voted concepts if integrating live)
concepts = [
    {'Cluster': 0, 'Helmet Size': 'Medium', 'Foam Type': 'Foam B', 'Shell Material': 'Polycarbonate'},
    {'Cluster': 1, 'Helmet Size': 'Large', 'Foam Type': 'Foam C', 'Shell Material': 'ABS'}
]

lifecycle_stages = ["Concept", "Design", "Prototype", "Testing", "Production"]

def run():
    st.header("🗂️ Project Lifecycle Tracker Module")

    # Load top voted concepts from session state
    top_concepts = st.session_state.get('top_voted_concepts', [])

    # Initialize projects in session state if not existing
    if 'projects' not in st.session_state:
        st.session_state.projects = []
        for concept in concepts:
            st.session_state.projects.append({
                'Cluster': concept['Cluster'],
                'Helmet Size': concept['Helmet Size'],
                'Foam Type': concept['Foam Type'],
                'Shell Material': concept['Shell Material'],
                'Stage': 'Concept',
                'Owner': '',
                'Target Date': date.today(),
                'Status Notes': ''
            })

    # Display and manage each project
    for idx, project in enumerate(st.session_state.projects):
        st.subheader(f"Project Cluster {project['Cluster']} - {project['Helmet Size']} Helmet")

        col1, col2, col3 = st.columns(3)
        with col1:
            project['Stage'] = st.selectbox(
                f"Stage for Cluster {project['Cluster']}",
                lifecycle_stages,
                index=lifecycle_stages.index(project['Stage'])
            )
        with col2:
            project['Owner'] = st.text_input(f"Owner for Cluster {project['Cluster']}", value=project['Owner'])
        with col3:
            project['Target Date'] = st.date_input(f"Target Date for Cluster {project['Cluster']}", value=project['Target Date'])

        project['Status Notes'] = st.text_area(
            f"Status Notes for Cluster {project['Cluster']}",
            value=project['Status Notes']
        )

        st.markdown("---")

    # Display project summary table
    st.subheader("📊 Project Portfolio Summary")

    project_df = pd.DataFrame(st.session_state.projects)
    st.dataframe(project_df)

    st.caption("⚠️ Data is stored in Streamlit session state for demo purposes. For production, integrate with SQLite or cloud database for persistence.")
