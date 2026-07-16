from content_based import (
    load_data as load_content_data,
    build_features,
    build_similarity_matrix,
    create_indices,
    recommend
)

from collaborative import (
    load_data as load_collaborative_data,
    create_user_movie_matrix,
    build_movie_similarity,
    create_title_to_movieid,
    create_movieid_to_index,
    recommend_collaborative
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

    content_recommendations = recommend(
    "Toy Story (1995)",
    content_movies,
    content_similarity,
    content_indices,
    top_n=10
    )

    collaborative_recommendations = recommend_collaborative(
    "Toy Story (1995)",
    collab_movies,
    user_movie_matrix,
    movie_similarity,
    title_to_movieid,
    movieid_to_index,
    top_n=10
    )

    hybrid_scores = {}

    for title, score in content_recommendations:
        hybrid_scores[title] = score * 0.5

    for title, score in collaborative_recommendations:

        if title in hybrid_scores:
            hybrid_scores[title] += score * 0.5
        else:
            hybrid_scores[title] = score * 0.5

    sorted_recommendations = sorted(
    hybrid_scores.items(),
    key=lambda x: x[1],
    reverse=True
    )

    print("\nHybrid Recommendations:\n")

    for i, (title, score) in enumerate(sorted_recommendations[:10], start=1):
        print(f"{i}. {title} ({score:.3f})")

if __name__ == "__main__":
    main()