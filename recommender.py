import streamlit as st
import pandas as pd
from tmdb_api import fetch_movie_details, fetch_tmdb_recommendations, get_tmdb_id, get_poster_url
from movie_card import movie_card_html
from content_based import recommend
from collaborative import recommend_collaborative


def hybrid_recommend(
    selected_movie,
    content_movies,
    content_similarity,
    content_indices,
    user_movie_matrix,
    movie_similarity,
    title_to_movieid,
    movieid_to_index,
    top_n=10
):

    content_recommendations = recommend(
        selected_movie,
        content_movies,
        content_similarity,
        content_indices,
        top_n
    )

    collaborative_recommendations = recommend_collaborative(
        selected_movie,
        content_movies,
        user_movie_matrix,
        movie_similarity,
        title_to_movieid,
        movieid_to_index,
        top_n
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

    return sorted_recommendations

def find_closest_movie_by_genres(
    tmdb_genres,
    content_movies
):

    best_match = None
    best_score = -1

    tmdb_genres = set(tmdb_genres)

    for _, row in content_movies.iterrows():

        movie_genres = set(row["genres"].split("|"))

        score = len(
            tmdb_genres.intersection(movie_genres)
        )

        if score > best_score:

            best_score = score

            best_match = row["title"]

    return best_match

CAROUSEL_CSS = """
<style>
.carousel{ display:flex; overflow-x:auto; gap:20px; padding:10px 0 20px 0; scroll-behavior:smooth; }
.carousel::-webkit-scrollbar{ height:10px; }
.carousel::-webkit-scrollbar-thumb{ background:#444; border-radius:20px; }
.card{ min-width:220px; max-width:220px; flex-shrink:0; background:#181818; border-radius:12px; overflow:hidden; box-shadow:0 4px 14px rgba(0,0,0,.5); transition:.2s; }
.card:hover{ transform:scale(1.04); }
.card img{ width:100%; height:320px; object-fit:cover; display:block; }
.card-content{ padding:10px; }
.card-title{ font-weight:700; font-size:15px; color:white; margin-top:4px; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; }
.card-rating{ color:#FFD54F; margin-top:6px; font-size:14px; }
.card-match{ color:#4CAF50; margin-top:4px; font-size:14px; }
.card-genre{ color:#BDBDBD; font-size:12px; margin-top:5px; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; }
.card-year{ color:#888; font-size:12px; margin-top:3px; }
</style>
"""


def show_hybrid_recommendations(
    selected_movie,
    content_movies,
    content_similarity,
    content_indices,
    user_movie_matrix,
    movie_similarity,
    title_to_movieid,
    movieid_to_index,
    links
):
    sorted_recommendations = hybrid_recommend(
        selected_movie,
        content_movies,
        content_similarity,
        content_indices,
        user_movie_matrix,
        movie_similarity,
        title_to_movieid,
        movieid_to_index,
        top_n=10
    )

    st.markdown("Hybrid Recommendations")

    cards = ""
    for title, score in sorted_recommendations[:10]:
        tmdb_id = get_tmdb_id(title, content_movies, links)
        movie = fetch_movie_details(tmdb_id)

        rating = content_movies.loc[content_movies["title"] == title, "rating"].values[0]
        genres = content_movies.loc[content_movies["title"] == title, "genres"].values[0]
        year = movie.get("release_date", "")[:4] if movie.get("release_date") else ""

        cards += movie_card_html(
            poster=movie["poster"],
            title=title,
            rating=(rating * 2) if pd.notna(rating) else None,
            genres=genres.replace("|", " • "),
            match_score=score,
            year=year,
            tmdb_id=tmdb_id
        )

    st.markdown(CAROUSEL_CSS, unsafe_allow_html=True)
    st.markdown(f'<div class="carousel">{cards}</div>', unsafe_allow_html=True)


def show_tmdb_similar(selected_tmdb_id):

    st.markdown("---")
    st.markdown("TMDB Similar Movies")

    tmdb_recommendations = fetch_tmdb_recommendations(selected_tmdb_id)

    cards = ""
    for movie in tmdb_recommendations[:15]:
        poster = get_poster_url(movie["poster_path"])
        year = movie.get("release_date", "")[:4] if movie.get("release_date") else ""

        cards += movie_card_html(
            poster=poster,
            title=movie["title"],
            rating=movie.get("vote_average"),
            genres="",
            year=year,
            tmdb_id=movie["id"]
        )

    st.markdown(CAROUSEL_CSS, unsafe_allow_html=True)
    st.markdown(f'<div class="carousel">{cards}</div>', unsafe_allow_html=True)