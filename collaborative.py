import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

def load_data():
    movies = pd.read_csv("data/movies.csv")
    ratings = pd.read_csv("data/ratings.csv")

    return movies, ratings

def create_user_movie_matrix(ratings):
    user_movie_matrix = ratings.pivot_table(
        index="userId",
        columns="movieId",
        values="rating"
    )

    user_movie_matrix = user_movie_matrix.fillna(0)

    return user_movie_matrix

def build_movie_similarity(user_movie_matrix):
    movie_similarity = cosine_similarity(user_movie_matrix.T)

    return movie_similarity

def create_title_to_movieid(movies):
    return pd.Series(movies["movieId"].values, index=movies["title"])

def create_movieid_to_index(user_movie_matrix):
    return {
        movie_id: index
        for index, movie_id in enumerate(user_movie_matrix.columns)
    }

def recommend_collaborative(
    movie_title,
    movies,
    user_movie_matrix,
    movie_similarity_topk,
    title_to_movieid,
    movieid_to_index,
    top_n=5
):
    if movie_title not in title_to_movieid:
        print("Movie not found!")
        return

    movie_id = title_to_movieid[movie_title]

    if movie_id not in movieid_to_index:
        print("Movie has no ratings!")
        return

    idx = movieid_to_index[movie_id]

    similarity_scores = movie_similarity_topk[idx][:top_n]

    recommendations = []
    for movie_index, score in similarity_scores:

        recommended_movie_id = user_movie_matrix.columns[movie_index]

        title = movies.loc[
            movies["movieId"] == recommended_movie_id,
            "title"
        ].values[0]

        recommendations.append((title, score))

    return recommendations

def main():
    movies, ratings = load_data()
    user_movie_matrix = create_user_movie_matrix(ratings)

    print(user_movie_matrix.head())
    print(movies.head())
    print(ratings.head())

    movie_similarity = build_movie_similarity(user_movie_matrix)

    title_to_movieid = create_title_to_movieid(movies)

    movieid_to_index = create_movieid_to_index(user_movie_matrix)

    print(movie_similarity.shape)
    
    print(movie_similarity[:5, :5])

    recommendations = recommend_collaborative(
    "Toy Story (1995)",
    movies,
    user_movie_matrix,
    movie_similarity,
    title_to_movieid,
    movieid_to_index,
    top_n=10
    )

    for i, (title, score) in enumerate(recommendations, start=1):
        print(f"{i}. {title} ({score:.3f})")

if __name__ == "__main__":
    main()



