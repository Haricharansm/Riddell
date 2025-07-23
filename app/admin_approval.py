import streamlit as st
import sqlite3
import pandas as pd

DB_PATH = "riddell_ai.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS approvals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            concept_name TEXT,
            cluster_id INTEGER,
            summary TEXT,
            status TEXT,
            comments TEXT
        )
    """)
    conn.close()

def load_pending_concepts():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql("SELECT * FROM approvals WHERE status = 'Pending'", conn)
    conn.close()
    return df

def update_approval(id, status, comments):
    conn = sqlite3.connect(DB_PATH)
    conn.execute("UPDATE approvals SET status = ?, comments = ? WHERE id = ?", (status, comments, id))
    conn.commit()
    conn.close()

def run():
    st.header("🛡️ Admin Approval Workflow")

    init_db()
    df = load_pending_concepts()

    if df.empty:
        st.info("No pending approvals at the moment.")
        return

    for _, row in df.iterrows():
        with st.expander(f"Concept: {row['concept_name']} (Cluster {row['cluster_id']})"):
            st.write(row["summary"])
            status = st.selectbox("Decision", ["Approve", "Reject"], key=row["id"])
            comments = st.text_area("Comments", key=f"comment_{row['id']}")
            if st.button("Submit Decision", key=f"submit_{row['id']}"):
                update_approval(row["id"], status, comments)
                st.success("Decision recorded.")
