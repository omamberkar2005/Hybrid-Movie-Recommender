import streamlit as st


def movie_card(
    poster,
    title,
    rating=None,
    genres="",
    match_score=None
):
    """Widget-based card — for use inside st.columns() grids."""

    rating_text = f"{rating:.1f}" if rating is not None else "N/A"

    match_html = ""
    if match_score is not None:
        match_html = f'<div class="movie-match">{match_score*100:.0f}% Match</div>'

    st.markdown(f"""
<style>
.movie-card{{ background:#181818; border-radius:14px; overflow:hidden; box-shadow:0 6px 16px rgba(0,0,0,.45); transition:.2s; margin-bottom:18px; }}
.movie-card:hover{{ transform:scale(1.03); }}
.movie-title{{ font-weight:700; font-size:17px; color:white; margin-top:8px; }}
.movie-rating{{ color:#FFD54F; margin-top:6px; }}
.movie-match{{ color:#4CAF50; margin-top:4px; }}
.movie-genre{{ color:#BDBDBD; font-size:13px; margin-top:5px; }}
</style>
""", unsafe_allow_html=True)

    st.image(poster, use_container_width=True)

    st.markdown(f"""
<div class="movie-title">{title}</div>
<div class="movie-rating">⭐ {rating_text}</div>
{match_html}
<div class="movie-genre">{genres}</div>
""", unsafe_allow_html=True)


def movie_card_html(
    poster,
    title,
    rating=None,
    genres="",
    match_score=None,
    year="",
    tmdb_id=None
):
    rating_text = f"{rating:.1f}" if rating is not None else "N/A"

    match_html = ""
    if match_score is not None:
        match_html = f'<div class="card-match">{match_score*100:.0f}% Match</div>'

    year_html = ""
    if year:
        year_html = f'<div class="card-year">{year}</div>'

    card_inner = f"""
<div class="card">
<img src="{poster}">
<div class="card-content">
<div class="card-title">{title}</div>
<div class="card-rating">⭐ {rating_text}</div>
{match_html}
<div class="card-genre">{genres}</div>
{year_html}
</div>
</div>
"""

    if tmdb_id:
        return f'<a href="?movie_id={tmdb_id}" target="_self" style="text-decoration:none; color:inherit;">{card_inner}</a>'

    return card_inner

def cast_card_html(photo, name, character):
    return f"""
<div class="cast-card">
<img src="{photo}">
<div class="cast-content">
<div class="cast-name">{name}</div>
<div class="cast-character">{character}</div>
</div>
</div>
"""