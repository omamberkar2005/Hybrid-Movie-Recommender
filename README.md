🎬 MovieMate
A hybrid movie recommendation system that suggests movies using content-based and collaborative filtering, with live posters, trailers, and cast info from TMDB.

<img width="1907" height="968" alt="Screenshot 2026-07-28 154249" src="https://github.com/user-attachments/assets/eb870882-df80-45f9-b96e-78729081abe8" />

Features

* 🔍 Search any movie and get posters, trailer, cast, and overview
* 🎯 Hybrid recommendations combining content-based (TF-IDF) and collaborative filtering
* 🧩 Fallback matcher for movies outside the dataset, so recommendations never dead-end
* 🎠 Horizontally scrollable rows for Popular, Trending, Top Rated, Now Playing, and Upcoming
* 🖱️ Click any movie card to jump straight into its detail page
* ⚡ Precomputed top-K similarity lookups instead of full similarity matrices — cut model size by ~99% for fast, deployable performance

Tech Stack

* Pandas + NumPy + scikit-learn (TF-IDF, cosine similarity)
* Content-Based Filtering + Collaborative Filtering (Hybrid)
* TMDB API (posters, trailers, cast, live metadata)
* Streamlit (UI)

Setup

1. Clone the repo
2. Install dependencies: `pip install -r requirements.txt`
3. Add your TMDB API key to `.env`: TMDB_API_KEY=your_key_here
4. Run: `streamlit run app.py`

Demo
Search for any movie — recent release or classic — and get personalized recommendations backed by real MovieLens rating data!
