import pickle

from sklearn.feature_extraction.text import TfidfVectorizer

from data_loader import load_data


data = load_data()

content_movies = data["content_movies"]


vectorizer = TfidfVectorizer(
    stop_words="english"
)

tfidf_matrix = vectorizer.fit_transform(
    content_movies["features"]
)


with open(
    "models/fallback_vectorizer.pkl",
    "wb"
) as file:

    pickle.dump(vectorizer, file)


with open(
    "models/fallback_tfidf.pkl",
    "wb"
) as file:

    pickle.dump(tfidf_matrix, file)


print("Fallback model created successfully!")