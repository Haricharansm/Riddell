import streamlit as st
import pandas as pd
from datetime import date
from app import db_utils
import sqlite3

lifecycle_stages = ["Concept", "Design", "Prototype", "Testing", "Production"]

def run():
    st.header("🗂️ Project Lifecycle Tracker Module")

    db_utils.initialize_db()

    conn = db_utils.create_connection()
    cursor = conn.cursor()

    # Load top voted concepts from session state
    top_concepts = st.session_state.get('top_voted_concepts', [])

    # Insert top voted concepts into DB if not already present
    for concept in top_concepts:
        cursor.execute("""
            SELECT COUNT(*) FROM projects WHERE cluster = ? AND helmet_size = ?
        """, (concept['Cluster'], concept['Helmet Size']))
        if cursor.fetchone()[0] == 0:
            cursor.execute("""
                INSERT INTO projects (cluster, helmet_size, foam_type, shell_material, stage, owner, target_date, status_notes)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                concept['Cluster'],
                concept['Helmet Size'],
                concept['Foam Type'],
                concept['Shell Material'],
                'Concept',
                '',
                date.today().isoformat(),
                ''
            ))
    conn.commit()

    # Fetch all projects
    df = pd.read_sql_query("SELECT * FROM projects", conn)

    # Display and edit each project
    for idx, project in df.iterrows():
        st.subheader(f"Project Cluster {project['cluster']} - {project['helmet_size']} Helmet")

        col1, col2, col3 = st.columns(3)
        with col1:
            new_stage = st.selectbox(
                f"Stage for Cluster {project['cluster']}",
                lifecycle_stages,
                index=lifecycle_stages.index(project['stage'])
            )
        with col2:
            new_owner = st.text_input(f"Owner for Cluster {project['cluster']}", value=project['owner'])
        with col3:
            new_date = st.date_input(f"Target Date for Cluster {project['cluster']}", value=pd.to_datetime(project['target_date']))

        new_notes = st.text_area(
            f"Status Notes for Cluster {project['cluster']}",
            value=project['status_notes']
        )

        # Update changes in DB
        if st.button(f"Save Updates for Cluster {project['cluster']}"):
            cursor.execute("""
                UPDATE projects
                SET stage = ?, owner = ?, target_date = ?, status_notes = ?
                WHERE id = ?
            """, (
                new_stage,
                new_owner,
                new_date.isoformat(),
                new_notes,
                project['id']
            ))
            conn.commit()
            st.success("Project updated successfully.")

        st.markdown("---")

    # Display full project portfolio
    st.subheader("📊 Project Portfolio Summary")
    df_updated = pd.read_sql_query("SELECT * FROM projects", conn)
    st.dataframe(df_updated)

    conn.close()

    st.caption("✅ Data is now stored persistently in SQLite for reliable project tracking.")

    
