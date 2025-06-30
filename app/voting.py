import streamlit as st
import pandas as pd

# Dummy concept recommendations for demonstration (replace with concept_df import if running live)
concepts = [
    {'Cluster': 0, 'Helmet Size': 'Medium', 'Foam Type': 'Foam B', 'Shell Material': 'Polycarbonate'},
    {'Cluster': 1, 'Helmet Size': 'Large', 'Foam Type': 'Foam C', 'Shell Material': 'ABS'},
    {'Cluster': 2, 'Helmet Size': 'Small', 'Foam Type': 'Foam A', 'Shell Material': 'Carbon Fiber'}
]

def run():
    st.header("🗳️ Concept Voting & Prioritization Module")

    # Initialize session state vote counts
    if 'votes' not in st.session_state:
        st.session_state.votes = {i: 0 for i in range(len(concepts))}

    # Display each concept with voting buttons
    for idx, concept in enumerate(concepts):
        st.subheader(f"Concept Cluster {concept['Cluster']}")
        st.write(f"Helmet Size: {concept['Helmet Size']}")
        st.write(f"Foam Type: {concept['Foam Type']}")
        st.write(f"Shell Material: {concept['Shell Material']}")

        col1, col2, col3 = st.columns([1,1,2])
        with col1:
            if st.button(f"👍 Upvote {idx}"):
                st.session_state.votes[idx] += 1
        with col2:
            if st.button(f"👎 Downvote {idx}"):
                st.session_state.votes[idx] -= 1
        with col3:
            st.write(f"Current Votes: {st.session_state.votes[idx]}")

    # Display ranked list based on votes
    st.subheader("🏆 Ranked Concepts Based on Votes")

    ranked = sorted(st.session_state.votes.items(), key=lambda x: x[1], reverse=True)
    ranked_df = pd.DataFrame([{
        'Cluster': concepts[idx]['Cluster'],
        'Helmet Size': concepts[idx]['Helmet Size'],
        'Foam Type': concepts[idx]['Foam Type'],
        'Shell Material': concepts[idx]['Shell Material'],
        'Votes': votes
    } for idx, votes in ranked])

    st.dataframe(ranked_df)

    st.caption("⚠️ Votes are stored in Streamlit session state for demo purposes. For production, integrate with a persistent database.")

