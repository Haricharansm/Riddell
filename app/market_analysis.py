import streamlit as st
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk import word_tokenize, pos_tag, ne_chunk

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('maxent_ne_chunker')
nltk.download('words')
nltk.download('vader_lexicon')

def run():
    st.header("Market & Competition Analysis with NLP Insights")

    uploaded_file = st.file_uploader("Upload Market Analysis Text", type=["txt"])
    
    if uploaded_file:
        text = uploaded_file.read().decode('utf-8')
        st.text_area("Market Analysis Content:", value=text, height=300)

        st.subheader("Keyword Extraction")
        tokens = word_tokenize(text)
        keywords = [word for word, pos in pos_tag(tokens) if pos.startswith('NN')]
        st.write(list(set(keywords)))

        st.subheader("Named Entity Recognition")
        entities = ne_chunk(pos_tag(tokens))
        named_entities = set()
        for subtree in entities:
            if hasattr(subtree, 'label'):
                named_entities.add(' '.join(c[0] for c in subtree))
        st.write(named_entities)

        st.subheader("Sentiment Analysis")
        sia = SentimentIntensityAnalyzer()
        sentiment = sia.polarity_scores(text)
        st.write(sentiment)

    else:
        st.info("Please upload a market analysis text file.")
