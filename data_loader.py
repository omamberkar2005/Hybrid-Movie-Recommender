import pickle
import pandas as pd
import streamlit as st

@st.cache_data
def load_data():

    # Load CSV files
    links = pd.read_csv("data/links.csv")
    ratings = pd.read_csv("data/ratings.csv")

    average_ratings = (
        ratings.groupby("movieId")["rating"]
        .mean()
        .reset_index()
    )

    # Load Pickle files
    with open("models/content_movies.pkl", "rb") as file:
        content_movies = pickle.load(file)

    with open("models/content_similarity_topk.pkl", "rb") as file:
        content_similarity = pickle.load(file)

    with open("models/content_indices.pkl", "rb") as file:
        content_indices = pickle.load(file)

    with open("models/user_movie_matrix.pkl", "rb") as file:
        user_movie_matrix = pickle.load(file)

    with open("models/movie_similarity_topk.pkl", "rb") as file:
        movie_similarity = pickle.load(file)

    with open("models/title_to_movieid.pkl", "rb") as file:
        title_to_movieid = pickle.load(file)

    with open("models/movieid_to_index.pkl", "rb") as file:
        movieid_to_index = pickle.load(file)

    # Merge average ratings
    content_movies = content_movies.merge(
        average_ratings,
        on="movieId",
        how="left"
    )

    return {
        "links": links,
        "ratings": ratings,
        "content_movies": content_movies,
        "content_similarity": content_similarity,
        "content_indices": content_indices,
        "user_movie_matrix": user_movie_matrix,
        "movie_similarity": movie_similarity,
        "title_to_movieid": title_to_movieid,
        "movieid_to_index": movieid_to_index
    }