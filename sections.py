import streamlit as st
from movie_card import movie_card_html
from tmdb_api import get_poster_url

def display_section(title, movies, genre_dict):

    st.markdown(f"## {title}")

    cards = ""
    for movie in movies[:15]:
        poster = get_poster_url(movie["poster_path"])
        genres = " • ".join(
            genre_dict.get(genre_id, "")
            for genre_id in movie["genre_ids"]
        )
        year = movie.get("release_date", "")[:4] if movie.get("release_date") else ""

        cards += movie_card_html(
            poster=poster,
            title=movie["title"],
            rating=movie.get("vote_average"),
            genres=genres,
            year=year,
            tmdb_id=movie["id"]
        )

    st.markdown(f"""
<style>
.carousel{{ display:flex; overflow-x:auto; gap:20px; padding:10px 0 20px 0; scroll-behavior:smooth; }}
.carousel::-webkit-scrollbar{{ height:10px; }}
.carousel::-webkit-scrollbar-thumb{{ background:#444; border-radius:20px; }}
.card{{ min-width:220px; max-width:220px; flex-shrink:0; background:#181818; border-radius:12px; overflow:hidden; box-shadow:0 4px 14px rgba(0,0,0,.5); transition:.2s; }}
.card:hover{{ transform:scale(1.04); }}
.card img{{ width:100%; height:320px; object-fit:cover; display:block; }}
.card-content{{ padding:10px; }}
.card-title{{ font-weight:700; font-size:15px; color:white; margin-top:4px; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; }}
.card-rating{{ color:#FFD54F; margin-top:6px; font-size:14px; }}
.card-match{{ color:#4CAF50; margin-top:4px; font-size:14px; }}
.card-genre{{ color:#BDBDBD; font-size:12px; margin-top:5px; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; }}
</style>

<div class="carousel">
{cards}
</div>
""", unsafe_allow_html=True)