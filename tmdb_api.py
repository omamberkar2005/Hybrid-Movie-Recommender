import requests
import os
from dotenv import load_dotenv
import streamlit as st

load_dotenv()

API_KEY = os.getenv("TMDB_API_KEY")


def get_poster_url(poster_path):

    if poster_path:
        return "https://image.tmdb.org/t/p/w500" + poster_path

    return "https://via.placeholder.com/500x750?text=No+Poster"


def fetch_movies(endpoint):

    url = f"https://api.themoviedb.org/3/{endpoint}?api_key={API_KEY}"

    response = requests.get(url)

    data = response.json()

    return data.get("results", [])


def search_movies(query):

    url = (
        f"https://api.themoviedb.org/3/search/movie"
        f"?api_key={API_KEY}"
        f"&query={query}"
    )

    response = requests.get(url)

    data = response.json()

    return data.get("results", [])

def fetch_movie_details(tmdb_id):

    url = (
        f"https://api.themoviedb.org/3/movie/"
        f"{tmdb_id}"
        f"?api_key={API_KEY}"
        f"&append_to_response=videos,credits"
    )

    response = requests.get(url)

    data = response.json()

    # ---------- Trailer ----------
    trailer_key = None

    for video in data.get("videos", {}).get("results", []):
        if (
            video["site"] == "YouTube"
            and video["type"] == "Trailer"
        ):
            trailer_key = video["key"]
            break

    # ---------- Cast ----------
    cast = data.get("credits", {}).get("cast", [])[:10]

    # ---------- Director ----------
    director = "Unknown"

    for crew in data.get("credits", {}).get("crew", []):
        if crew["job"] == "Director":
            director = crew["name"]
            break

    return {
        "poster": get_poster_url(data.get("poster_path")),
        "backdrop": get_poster_url(data.get("backdrop_path")),
        "title": data.get("title"),
        "overview": data.get("overview"),
        "release_date": data.get("release_date"),
        "rating": data.get("vote_average"),
        "runtime": data.get("runtime"),
        "language": data.get("original_language"),
        "genres": data.get("genres", []),
        "director": director,
        "cast": cast,
        "trailer": trailer_key
    }

def fetch_tmdb_recommendations(tmdb_id):

    url = (
        f"https://api.themoviedb.org/3/movie/"
        f"{tmdb_id}/recommendations?api_key={API_KEY}"
    )

    response = requests.get(url)

    data = response.json()

    return data.get("results", [])


def get_tmdb_id(movie_title, content_movies, links):

    movie_id = content_movies.loc[
        content_movies["title"] == movie_title,
        "movieId"
    ].values[0]

    tmdb_id = links.loc[
        links["movieId"] == movie_id,
        "tmdbId"
    ].values[0]

    return int(tmdb_id)

@st.cache_data
def fetch_genres():

    url = (
        f"https://api.themoviedb.org/3/genre/movie/list"
        f"?api_key={API_KEY}"
    )

    response = requests.get(url)

    data = response.json()

    genre_dict = {}

    for genre in data["genres"]:
        genre_dict[genre["id"]] = genre["name"]

    return genre_dict