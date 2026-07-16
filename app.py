import streamlit as st
from data_loader import load_data
from tmdb_api import fetch_movies, search_movies, fetch_genres
from sections import display_section
from movie_detail import show_movie_detail

st.set_page_config(page_title="Hybrid Movie Recommender", page_icon="🎬", layout="wide")

st.markdown("""
<style>
.block-container { padding-left: 3rem; padding-right: 3rem; padding-top: 0rem; max-width: 100%; }
header[data-testid="stHeader"] { background: transparent; height: 2.5rem; }
.stApp { background-color: #0E0E10; }
</style>
""", unsafe_allow_html=True)

data = load_data()
links = data["links"]

query_params = st.query_params
clicked_tmdb_id = None
if "movie_id" in query_params:
    try:
        clicked_tmdb_id = int(query_params["movie_id"])
    except (ValueError, TypeError):
        clicked_tmdb_id = None

top_bar_css = """
<style>
.topbar-wrap { display: flex; align-items: center; gap: 20px; padding: 10px 0 20px 0; }
.topbar-logo { display: flex; align-items: center; gap: 10px; flex-shrink: 0; }
.topbar-logo-icon { font-size: 26px; }
.topbar-logo-text { font-size: 22px; font-weight: 700; color: white; }
</style>
"""
st.markdown(top_bar_css, unsafe_allow_html=True)

logo_col, search_col = st.columns([1, 3])
with logo_col:
    st.markdown(
        '<div class="topbar-logo"><span class="topbar-logo-icon">🎬</span>'
        '<span class="topbar-logo-text">MovieMate</span></div>',
        unsafe_allow_html=True
    )
with search_col:
    search = st.text_input("Search", placeholder="🔍 Search for any movie", label_visibility="collapsed")

st.sidebar.header("About")
st.sidebar.info("""
This application recommends movies using:

Content-Based Filtering

Collaborative Filtering

Hybrid Recommendation System
""")

popular_movies = fetch_movies("movie/popular")
top_rated_movies = fetch_movies("movie/top_rated")
trending_movies = fetch_movies("trending/movie/week")
now_playing_movies = fetch_movies("movie/now_playing")
upcoming_movies = fetch_movies("movie/upcoming")
genre_dict = fetch_genres()

selected_movie = None
selected_tmdb_id = None

if search:
    results = search_movies(search)
    if results:
        movie_options = {}
        for movie in results[:10]:
            year = movie["release_date"][:4] if movie.get("release_date") else "N/A"
            label = f"{movie['title']} ({year})"
            movie_options[label] = movie["id"]

        selected_movie = st.selectbox("Search Results", list(movie_options.keys()))
        selected_tmdb_id = movie_options[selected_movie]

if clicked_tmdb_id:
    selected_tmdb_id = clicked_tmdb_id
    selected_movie = "clicked"

if not selected_tmdb_id:
    display_section("Popular Movies", popular_movies, genre_dict)
    display_section("Top Rated", top_rated_movies, genre_dict)
    display_section("Trending This Week", trending_movies, genre_dict)
    display_section("Now Playing", now_playing_movies, genre_dict)
    display_section("Upcoming", upcoming_movies, genre_dict)

if selected_tmdb_id:
    show_movie_detail(selected_tmdb_id, data)