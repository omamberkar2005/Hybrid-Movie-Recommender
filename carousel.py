import streamlit as st


def start_carousel(title):

    st.markdown(f"## {title}")

    html = """
<style>
.carousel{ display:flex; overflow-x:auto; gap:20px; padding:10px 0 20px 0; scroll-behavior:smooth; }
.carousel::-webkit-scrollbar{ height:10px; }
.carousel::-webkit-scrollbar-thumb{ background:#444; border-radius:20px; }
.card{ min-width:220px; flex-shrink:0; }
</style>

<div class="carousel">
"""

    st.markdown(html, unsafe_allow_html=True)


def end_carousel():

    st.markdown("</div>", unsafe_allow_html=True)