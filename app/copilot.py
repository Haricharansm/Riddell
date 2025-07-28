import streamlit as st
import pandas as pd

def run():
    st.sidebar.title("🧠 Smart Assistant")
    question = st.sidebar.text_input("Ask a question about helmet fit and comfort...")

    # Load and preprocess the data
    @st.cache_data
    def load_data():
        df = pd.read_excel("Player Fit & Comfort Data.xlsx")
        df.columns = [col.strip().replace(" ", "_").lower() for col in df.columns]
        return df

    df = load_data()

    # Logic to handle questions
    if st.sidebar.button("Ask"):
        if not question.strip():
            st.sidebar.warning("Please enter a valid question.")
            return

        q = question.lower()
        answer = "🤔 I'm not sure how to answer that yet."

        if "low fit score" in q or "poor fit" in q:
            low_fit = df[df['fitscore'] < 80]
            answer = f"There are {len(low_fit)} players with a fit score below 80. Consider checking their helmet size and pressure points."

        elif "pressure point" in q:
            high_pressure = df[df['pressurepoints'] > 2]
            answer = f"{len(high_pressure)} players had more than 2 pressure points. Common positions include: {', '.join(high_pressure['position'].unique())}"

        elif "most adjustments" in q:
            max_adj = df['adjustmentsmade'].max()
            players = df[df['adjustmentsmade'] == max_adj]
            answer = f"Player(s) with most adjustments ({max_adj}): {', '.join(players['id'])}"

        elif "comfort rating" in q and "position" in q:
            avg_comfort = df.groupby('position')['comfortrating'].mean().sort_values(ascending=False)
            answer = f"Average comfort rating by position:\n" + avg_comfort.to_string()

        elif "chin strap tension" in q and "comfort" in q:
            corr = df['chinstraptension'].corr(df['comfortrating'])
            answer = f"Correlation between chin strap tension and comfort rating is {corr:.2f}. (Closer to -1 or 1 indicates strong relation)"

        elif "vision" in q and "head width" in q:
            corr = df['headwidth'].corr(df['visionscore'])
            answer = f"Correlation between head width and vision score is {corr:.2f}."

        elif "fit score" in q and "comfort" in q:
            corr = df['fitscore'].corr(df['comfortrating'])
            answer = f"Fit score and comfort rating have a correlation of {corr:.2f}."

        elif "helmet size" in q:
            summary = df.groupby('helmetsize').agg({'fitscore': 'mean', 'adjustmentsmade': 'sum'}).sort_values(by='fitscore')
            answer = f"Helmet size insights:\n" + summary.to_string()

        st.sidebar.success(answer)
