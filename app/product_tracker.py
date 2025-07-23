import streamlit as st
import pandas as pd
from datetime import date, datetime
from app import db_utils
import sqlite3

lifecycle_stages = ["Concept", "Design", "Prototype", "Testing", "Production"]

def run():
    st.header("🗂️ Project Lifecycle Tracker Module")

    db_utils.initialize_db()
    conn = db_utils.create_connection()
    cursor = conn.cursor()

    # Load top voted concepts if available
    top_concepts = st.session_state.get('top_voted_concepts', [])

    if top_concepts:
        st.info("📥 Importing top voted concepts into the project tracker...")

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
                'Imported from Voting Module'
            ))
    conn.commit()

    # Load all project records
    df = pd.read_sql_query("SELECT * FROM projects", conn)

    if df.empty:
        st.warning("No projects have been created yet. Submit concepts or approve to get started.")
        return

    # Display editable cards for each project
    for idx, project in df.iterrows():
        st.subheader(f"📌 Project: Cluster {project['cluster']} – {project['helmet_size']} Helmet")

        col1, col2, col3 = st.columns(3)
        with col1:
            new_stage = st.selectbox(
                f"Stage (Cluster {project['cluster']})",
                lifecycle_stages,
                index=lifecycle_stages.index(project['stage']),
                key=f"stage_{project['id']}"
            )
        with col2:
            new_owner = st.text_input(
                f"Owner",
                value=project['owner'],
                key=f"owner_{project['id']}"
            )
        with col3:
            new_date = st.date_input(
                f"Target Date",
                value=pd.to_datetime(project['target_date']),
                key=f"date_{project['id']}"
            )

        new_notes = st.text_area(
            f"Status Notes",
            value=project['status_notes'],
            key=f"notes_{project['id']}"
        )

        if st.button(f"💾 Save for Cluster {project['cluster']}", key=f"save_{project['id']}"):
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
            st.success(f"✅ Updates saved for Cluster {project['cluster']}")

        st.markdown("---")

    # Final project table
    st.subheader("📊 Full Project Portfolio Summary")
    df_updated = pd.read_sql_query("SELECT * FROM projects", conn)
    st.dataframe(df_updated)

    conn.close()
    st.caption("✔️ Project updates are saved persistently using SQLite.")
