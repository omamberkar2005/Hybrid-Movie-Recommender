import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def load_data():
    movies = pd.read_csv("data/movies.csv")
    tags = pd.read_csv("data/tags.csv")

    return movies, tags


def build_features(movies, tags):
    # Combine all tags for the same movie
    grouped_tags = tags.groupby("movieId")["tag"].apply(" ".join).reset_index()

    # Merge tags with movies
    movies = movies.merge(grouped_tags, on="movieId", how="left")

    # Replace missing tags
    movies["tag"] = movies["tag"].fillna("")

    # Create a combined features column
    movies["features"] = movies["genres"] + " " + movies["tag"]

    return movies


def build_similarity_matrix(movies):
    tfidf = TfidfVectorizer()

    tfidf_matrix = tfidf.fit_transform(movies["features"])

    cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

    return cosine_sim


def create_indices(movies):
    return pd.Series(movies.index, index=movies["title"])


def main():
    movies, tags = load_data()

    movies = build_features(movies, tags)

    cosine_sim = build_similarity_matrix(movies)

    indices = create_indices(movies)

    recommendations = recommend(
        "Toy Story (1995)",
        movies,
        cosine_sim,
        indices,
        top_n=10
    )
    for i, (title, score) in enumerate(recommendations, start=1):
        print(f"{i}. {title} ({score:.3f})")

def recommend(movie_title, movies, content_similarity_topk, indices, top_n=10):
    if movie_title not in indices:
        print("Movie not found!")
        return

    idx = indices[movie_title]

    similarity_scores = content_similarity_topk[idx][:top_n]

    recommendations = []
    for movie_index, score in similarity_scores:
        title = movies.iloc[movie_index]["title"]
        recommendations.append((title, score))

    return recommendations
