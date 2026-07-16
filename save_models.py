import pickle

from content_based import (
    load_data as load_content_data,
    build_features,
    build_similarity_matrix,
    create_indices
)

from collaborative import (
    load_data as load_collaborative_data,
    create_user_movie_matrix,
    build_movie_similarity,
    create_title_to_movieid,
    create_movieid_to_index
)

def main():
    content_movies, tags = load_content_data()

    collab_movies, ratings = load_collaborative_data()

    content_movies = build_features(content_movies, tags)

    content_similarity = build_similarity_matrix(content_movies)

    content_indices = create_indices(content_movies)

    user_movie_matrix = create_user_movie_matrix(ratings)

    movie_similarity = build_movie_similarity(user_movie_matrix)

    title_to_movieid = create_title_to_movieid(collab_movies)

    movieid_to_index = create_movieid_to_index(user_movie_matrix)

    print("✅ Models built successfully!")

    with open("models/content_movies.pkl", "wb") as file:
        pickle.dump(content_movies, file)

    with open("models/content_similarity.pkl", "wb") as file:
        pickle.dump(content_similarity, file)

    with open("models/content_indices.pkl", "wb") as file:
        pickle.dump(content_indices, file)

    with open("models/user_movie_matrix.pkl", "wb") as file:
        pickle.dump(user_movie_matrix, file)

    with open("models/movie_similarity.pkl", "wb") as file:
        pickle.dump(movie_similarity, file)

    with open("models/title_to_movieid.pkl", "wb") as file:
        pickle.dump(title_to_movieid, file)

    with open("models/movieid_to_index.pkl", "wb") as file:
        pickle.dump(movieid_to_index, file)

    print("✅ All models saved successfully!")
    
if __name__ == "__main__":
    main()