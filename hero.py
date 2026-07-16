import streamlit as st
import textwrap

def show_hero(movie):

    genres = " • ".join(
        g["name"] for g in movie["genres"]
    )

    hero_html = f"""
<style>
.hero-wrap {{ position: relative; margin-bottom: 0px; }}

.hero-backdrop{{
    position:relative;
    height:420px;
    width:100%;
    background-image:
        linear-gradient(
            to right,
            rgba(8,8,8,.95) 15%,
            rgba(8,8,8,.45) 55%,
            rgba(8,8,8,.8) 100%
        ),
        url('{movie["backdrop"]}');
    background-size:cover;
    background-position:center;
}}

hero-fade {{
    position: absolute;
    width: 100%;
    left: 0;
    top: 0;
    height: 420px;
    background: linear-gradient(180deg, rgba(14,14,16,0) 40%, rgba(14,14,16,1) 100%);
}}

.hero-body {{ display: flex; align-items: flex-end; gap: 30px; margin-top: -140px; padding: 0 40px; position: relative; z-index: 2; }}
.hero-poster {{ width: 220px; border-radius: 14px; box-shadow: 0 10px 30px rgba(0,0,0,0.7); border: 3px solid #0E0E10; flex-shrink: 0; }}
.hero-info {{ flex: 1; color: white; padding-bottom: 10px; }}
.hero-title {{ font-size: 44px; font-weight: 700; margin-bottom: 8px; text-shadow: 0 2px 10px rgba(0,0,0,0.8); }}
.hero-rating {{ font-size: 24px; color: #FFD54F; margin-bottom: 10px; }}
.hero-genres {{ font-size: 16px; color: #BBBBBB; margin-bottom: 14px; }}
.hero-overview {{ font-size: 16px; line-height: 1.6; color: #DDDDDD; max-width: 700px; }}
</style>

<div class="hero-wrap">
<div class="hero-backdrop"></div>
<div class="hero-fade"></div>
<div class="hero-body">
<img class="hero-poster" src="{movie['poster']}">
<div class="hero-info">
<div class="hero-title">{movie['title']}</div>
<div class="hero-rating">⭐ {movie['rating']:.1f}/10</div>
<div class="hero-genres">{genres}</div>
<div class="hero-overview">{movie['overview']}</div>
</div>
</div>
</div>
"""

    st.markdown(textwrap.dedent(hero_html), unsafe_allow_html=True)