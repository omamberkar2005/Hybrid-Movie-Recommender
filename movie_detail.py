import streamlit as st
from hero import show_hero
from movie_card import cast_card_html
from tmdb_api import fetch_movie_details
from fallback_matcher import find_best_match
from recommender import show_hybrid_recommendations, show_tmdb_similar


def show_movie_detail(selected_tmdb_id, data):

    links = data["links"]
    content_movies = data["content_movies"]
    content_similarity = data["content_similarity"]
    content_indices = data["content_indices"]
    user_movie_matrix = data["user_movie_matrix"]
    movie_similarity = data["movie_similarity"]
    title_to_movieid = data["title_to_movieid"]
    movieid_to_index = data["movieid_to_index"]

    with st.spinner("Finding the best movies for you..."):

        movie_details = fetch_movie_details(selected_tmdb_id)
        show_hero(movie_details)

        st.markdown("---")
        st.markdown('<div id="official-trailer"></div>', unsafe_allow_html=True)
        st.subheader("🎥 Official Trailer")

        if movie_details["trailer"]:
            st.video(f"https://www.youtube.com/watch?v={movie_details['trailer']}")
        else:
            st.info("Trailer not available.")

        st.markdown("---")
        st.subheader("Top Cast")

        cast_cards = ""
        for actor in movie_details["cast"]:
            photo = (
                "https://image.tmdb.org/t/p/w185" + actor["profile_path"]
                if actor["profile_path"]
                else "https://via.placeholder.com/185x278?text=No+Photo"
            )
            cast_cards += cast_card_html(
                photo=photo, name=actor["name"], character=actor["character"]
            )

        cast_css = """
<style>
.cast-carousel{ display:flex; overflow-x:auto; gap:16px; padding:10px 0 20px 0; scroll-behavior:smooth; }
.cast-carousel::-webkit-scrollbar{ height:10px; }
.cast-carousel::-webkit-scrollbar-thumb{ background:#444; border-radius:20px; }
.cast-card{ min-width:140px; max-width:140px; flex-shrink:0; background:#181818; border-radius:12px; overflow:hidden; box-shadow:0 4px 12px rgba(0,0,0,.45); transition:.2s; }
.cast-card:hover{ transform:scale(1.05); }
.cast-card img{ width:100%; height:180px; object-fit:cover; display:block; }
.cast-content{ padding:8px; }
.cast-name{ font-weight:600; font-size:13px; color:white; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; }
.cast-character{ color:#BDBDBD; font-size:12px; margin-top:2px; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; }
</style>
"""
        st.markdown(cast_css, unsafe_allow_html=True)
        st.markdown(f'<div class="cast-carousel">{cast_cards}</div>', unsafe_allow_html=True)

        if selected_tmdb_id in links["tmdbId"].values:

            movie_id = links.loc[links["tmdbId"] == selected_tmdb_id, "movieId"].values[0]
            selected_movie = content_movies.loc[
                content_movies["movieId"] == movie_id, "title"
            ].values[0]

            st.markdown("---")
            show_hybrid_recommendations(
                selected_movie, content_movies, content_similarity, content_indices,
                user_movie_matrix, movie_similarity, title_to_movieid, movieid_to_index, links
            )

        else:

            st.warning("Movie not found in MovieLens dataset.")

            closest_movie = find_best_match(movie_details, content_movies)
            selected_movie = closest_movie["title"]

            st.info(f"Using '{selected_movie}' as the closest match.")

            show_hybrid_recommendations(
                selected_movie, content_movies, content_similarity, content_indices,
                user_movie_matrix, movie_similarity, title_to_movieid, movieid_to_index, links
            )

            show_tmdb_similar(selected_tmdb_id)