import pickle

from sklearn.metrics.pairwise import cosine_similarity


with open("models/fallback_vectorizer.pkl", "rb") as file:
    vectorizer = pickle.load(file)

with open("models/fallback_tfidf.pkl", "rb") as file:
    tfidf_matrix = pickle.load(file)


def find_best_match(
    tmdb_movie,
    content_movies
):

    genres = " ".join(
        genre["name"]
        for genre in tmdb_movie["genres"]
    )

    overview = tmdb_movie.get("overview", "")

    tmdb_text = f"{genres} {overview}"

    tmdb_vector = vectorizer.transform(
        [tmdb_text]
    )

    similarity = cosine_similarity(
        tmdb_vector,
        tfidf_matrix
    )

    best_index = similarity.argmax()

    return content_movies.iloc[best_index]