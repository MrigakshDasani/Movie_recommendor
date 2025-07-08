
# Enhanced Movie Recommendation Model
import pandas as pd
import numpy as np
import ast
import nltk
import requests
import difflib
from nltk.stem.porter import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from fuzzywuzzy import fuzz
import re

nltk.download('punkt')

# Load data
movies = pd.read_csv('tmdb_5000_movies.csv')
credits = pd.read_csv('tmdb_5000_credits.csv')
movies = movies.merge(credits, on='title')
movies = movies[['movie_id', 'title', 'overview', 'genres', 'keywords', 'cast', 'crew', 'vote_average', 'vote_count']]
movies.dropna(inplace=True)

# --- Data Preprocessing ---
def convert(obj):
    return [i['name'] for i in ast.literal_eval(obj)]

def convert_cast(obj):
    return [i['name'] for i in ast.literal_eval(obj)[:3]]

def fetch_director(obj):
    for i in ast.literal_eval(obj):
        if i['job'] == 'Director':
            return [i['name']]
    return []

movies['genres'] = movies['genres'].apply(convert)
movies['keywords'] = movies['keywords'].apply(convert)
movies['cast'] = movies['cast'].apply(convert_cast)
movies['crew'] = movies['crew'].apply(fetch_director)
movies['overview'] = movies['overview'].apply(lambda x: x.split())

for feature in ['genres', 'keywords', 'cast', 'crew']:
    movies[feature] = movies[feature].apply(lambda x: [i.replace(" ", "") for i in x])

movies['tags'] = movies['overview'] + movies['genres'] + movies['keywords'] + movies['cast'] + movies['crew']
new_df = movies[['movie_id', 'title', 'tags', 'genres', 'vote_average', 'vote_count']].copy()
new_df['tags'] = new_df['tags'].apply(lambda x: " ".join(x)).str.lower()

ps = PorterStemmer()
def stem(text):
    return " ".join([ps.stem(word) for word in text.split()])

new_df['tags'] = new_df['tags'].apply(stem)

tfidf = TfidfVectorizer(max_features=8000, stop_words='english', ngram_range=(1, 2), min_df=2, max_df=0.8)
vectors = tfidf.fit_transform(new_df['tags']).toarray()
similarity = cosine_similarity(vectors)

API_KEY = Your_API_KEY

def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US"
    data = requests.get(url).json()
    if data.get("poster_path"):
        return "https://image.tmdb.org/t/p/w500" + data["poster_path"]
    return "https://via.placeholder.com/500x750?text=No+Image"

def find_best_movie_match(movie_name):
    movie_name = movie_name.lower().strip()
    all_titles = new_df['title'].str.lower().tolist()

    exact_matches = [i for i, title in enumerate(all_titles) if title == movie_name]
    if exact_matches:
        return exact_matches[0]

    partial_matches = [(i, title) for i, title in enumerate(all_titles) if movie_name in title or title in movie_name]
    if partial_matches:
        partial_matches.sort(key=lambda x: abs(len(x[1]) - len(movie_name)))
        return partial_matches[0][0]

    best_match = None
    best_score = 0
    for i, title in enumerate(all_titles):
        score = fuzz.ratio(movie_name, title)
        if score > best_score and score > 70:
            best_score = score
            best_match = i

    if best_match is not None:
        return best_match

    movie_words = set(movie_name.split())
    for i, title in enumerate(all_titles):
        title_words = set(title.split())
        if movie_words.intersection(title_words):
            return i

    return None

def extract_franchise_name(title):
    title = re.sub(r'\b(part|pt\.?)\s*\d+\b', '', title, flags=re.IGNORECASE)
    title = re.sub(r'\b(ii|iii|iv|v|vi|vii|viii|ix|x)\b', '', title, flags=re.IGNORECASE)
    title = re.sub(r'\b\d+\b', '', title)
    title = re.sub(r'[:\-\(\)]', '', title)
    return title.strip()

def recommend_by_movie(movie):
    movie_index = find_best_movie_match(movie)
    if movie_index is None:
        return [], []

    distances = list(enumerate(similarity[movie_index]))
    sorted_movies = sorted(distances, key=lambda x: x[1], reverse=True)[1:]

    enhanced_scores = []
    input_title = new_df.iloc[movie_index]['title'].lower()
    input_genres = set(new_df.iloc[movie_index]['genres'])

    for idx, similarity_score in sorted_movies:
        candidate_title = new_df.iloc[idx]['title'].lower()
        candidate_genres = set(new_df.iloc[idx]['genres'])

        title_similarity = fuzz.ratio(input_title, candidate_title) / 100
        genre_overlap = len(input_genres.intersection(candidate_genres)) / len(input_genres.union(candidate_genres))
        popularity_score = min(new_df.iloc[idx]['vote_count'] / 1000, 1.0)
        rating_score = new_df.iloc[idx]['vote_average'] / 10.0

        franchise_bonus = 0.3 if extract_franchise_name(input_title) == extract_franchise_name(candidate_title) else 0

        combined_score = (
            similarity_score * 0.4 +
            title_similarity * 0.2 +
            genre_overlap * 0.2 +
            popularity_score * 0.1 +
            rating_score * 0.1 +
            franchise_bonus
        )

        enhanced_scores.append((idx, combined_score))

    enhanced_scores.sort(key=lambda x: x[1], reverse=True)

    recommended_titles = []
    recommended_posters = []

    for idx, _ in enhanced_scores:
        movie_id = new_df.iloc[idx].movie_id
        title = new_df.iloc[idx].title
        poster = fetch_poster(movie_id)

        recommended_titles.append(title)
        recommended_posters.append(poster)

        if len(recommended_titles) == 5:
            break

    return recommended_titles, recommended_posters

def top_movies_by_genre(genre_name):
    genre_name = genre_name.strip().lower()
    filtered = new_df.copy()
    filtered = filtered[filtered['genres'].apply(lambda genres: genre_name in [g.lower() for g in genres])]

    def weighted_score(row):
        v = row['vote_count']
        r = row['vote_average']
        m = filtered['vote_count'].quantile(0.6)
        C = filtered['vote_average'].mean()
        return (v / (v + m)) * r + (m / (v + m)) * C

    filtered['score'] = filtered.apply(weighted_score, axis=1)
    top_movies = filtered.sort_values(by='score', ascending=False).head(5)
    return top_movies['title'].tolist(), top_movies['movie_id'].tolist()

def get_all_genres():
    genres = set()
    for lst in new_df['genres']:
        genres.update(lst)
    return sorted(genres)
