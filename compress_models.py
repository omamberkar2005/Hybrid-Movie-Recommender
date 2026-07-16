import numpy as np
import pickle

top_k = 20

# ---- Content-based similarity ----
print("Loading content_similarity.pkl...")
with open("models/content_similarity.pkl", "rb") as f:
    content_similarity = pickle.load(f)

print("Compressing content similarity...")
top_similar_content = {}
for idx in range(content_similarity.shape[0]):
    sim_scores = content_similarity[idx]
    top_indices = np.argsort(sim_scores)[::-1][1:top_k+1]
    top_similar_content[idx] = [(int(i), float(sim_scores[i])) for i in top_indices]

with open("models/content_similarity_topk.pkl", "wb") as f:
    pickle.dump(top_similar_content, f)

print("Saved content_similarity_topk.pkl")

# ---- Collaborative similarity ----
print("Loading movie_similarity.pkl...")
with open("models/movie_similarity.pkl", "rb") as f:
    movie_similarity = pickle.load(f)

print("Compressing collaborative similarity...")
top_similar_collab = {}
for idx in range(movie_similarity.shape[0]):
    sim_scores = movie_similarity[idx]
    top_indices = np.argsort(sim_scores)[::-1][1:top_k+1]
    top_similar_collab[idx] = [(int(i), float(sim_scores[i])) for i in top_indices]

with open("models/movie_similarity_topk.pkl", "wb") as f:
    pickle.dump(top_similar_collab, f)

print("Saved movie_similarity_topk.pkl")
print("Done!")