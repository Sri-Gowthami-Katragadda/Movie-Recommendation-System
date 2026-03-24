import streamlit as st
import pickle
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

st.set_page_config(page_title="Movie Recommender", layout="wide")

# Load data
df = pd.read_pickle("df.pkl")
indices = pickle.load(open("indices.pkl", "rb"))
tfidf_matrix = pickle.load(open("tf_idfmatrix.pkl", "rb"))

# Recommendation function (same as your notebook)
def recommend(title, n=5):
    if title not in indices:
        return ["Movie not found"]

    idx = indices[title]

    similarity = cosine_similarity(tfidf_matrix[idx], tfidf_matrix)
    similar_idx = similarity[0].argsort()[::-1][1:n+1]

    return df["title"].iloc[similar_idx].values

# UI
st.title("🎬 Movie Recommendation System")

movie_list = df["title"].values
selected_movie = st.selectbox("Select a movie", movie_list)

if st.button("Recommend"):
    recommendations = recommend(selected_movie)

    st.subheader("Top Recommendations:")
    cols = st.columns(5)

    for i, col in enumerate(cols):
        with col:
            if i < len(recommendations):
                st.write(recommendations[i])