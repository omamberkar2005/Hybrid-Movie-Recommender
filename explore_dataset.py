import pandas as pd

movies = pd.read_csv("data/movies.csv")
ratings = pd.read_csv("data/ratings.csv")
tags = pd.read_csv("data/tags.csv")
links = pd.read_csv("data/links.csv")

print("Movies Shape:", movies.shape)
print("Ratings Shape:", ratings.shape)
print("Tags Shape:", tags.shape)
print("Links Shape:", links.shape)

print("\n=== Movies Dataset ===")
print(movies.head())

print("\n=== Ratings Dataset ===")
print(ratings.head())

print("\n=== Tags Dataset ===")
print(tags.head())

print("\n=== Links Dataset ===")
print(links.head())

print("\n========== DATASET INFORMATION ==========\n")

print("Movies Info:")
print(movies.info())

print("\nRatings Info:")
print(ratings.info())

print("\nTags Info:")
print(tags.info())

print("\nLinks Info:")
print(links.info())

print("\n========== MISSING VALUES ==========\n")

print("Movies")
print(movies.isnull().sum())

print("\nRatings")
print(ratings.isnull().sum())

print("\nTags")
print(tags.isnull().sum())

print("\nLinks")
print(links.isnull().sum())

print("\n========== DUPLICATES ==========\n")

print("Movies:", movies.duplicated().sum())
print("Ratings:", ratings.duplicated().sum())
print("Tags:", tags.duplicated().sum())
print("Links:", links.duplicated().sum())

print("\n========== UNIQUE COUNTS ==========\n")

print("Unique Movies:", movies["movieId"].nunique())
print("Unique Users:", ratings["userId"].nunique())
print("Unique Rated Movies:", ratings["movieId"].nunique())