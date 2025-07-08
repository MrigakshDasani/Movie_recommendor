# 🎬 AI-Powered Movie Recommender System

An intelligent, interactive, and beautifully designed movie recommendation system built with **Streamlit**, offering users personalized movie suggestions based either on genre or similar movie titles. 
The system is powered by advanced **NLP techniques**, **TF-IDF vectorization**, and real-time data fetching from the **TMDB API**.
(Search for hollywood movies for better results)


## 🚀 Live Demo

🌐 [Click to view the live app](https://movierecommendor-mrig.streamlit.app/)  
🎥 Instantly discover the best movies tailored to your mood or your favorite titles!


## 🧠 Project Overview

This project is an advanced movie recommender system that provides two powerful recommendation modes:
1. **Genre-Based Filtering** — Top 5 movies based on a selected genre.
2. **Movie-Based Recommendation** — Finds top 5 movies similar to a user-entered title using vector similarity, fuzzy matching, and franchise detection.

Each recommended movie includes:
- Movie **poster**
- Real-time **star rating**
- A clean and animated **UI/UX**


## 🧰 Tech Stack

| Category           | Tools & Libraries                            |
|--------------------|----------------------------------------------|
| Frontend UI        | `Streamlit`, `HTML/CSS (customized)`         |
| Backend & Logic    | `Python`, `Pandas`, `NumPy`, `sklearn`,`nltk`|
| NLP                | `TF-IDF Vectorizer`, `Porter Stemmer`        |
| API Integration    | `TMDB API` for posters and metadata          |
| Deployment         | `Streamlit Community Cloud` / `Render`       |
| Fuzzy Matching     | `FuzzyWuzzy` for intelligent movie match     |


## 📦 Dataset Used

### 🎥 TMDB 5000 Movie Dataset

- `tmdb_5000_movies.csv`
- `tmdb_5000_credits.csv`

> These datasets include a wide range of movie metadata like **genres, cast, crew, keywords, overview, vote average, vote count**, and more.
> 
> 📍 Source: [Kaggle - TMDB 5000 Movie Dataset](https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata)


## ⚙️ Key Features

- 🎯 **Dual Recommendation Modes**
  - Based on movie title (via TF-IDF similarity)
  - Based on genre popularity (via weighted rating)
  
- 🎨 **Modern & Interactive UI**
  - Smooth animations
  - Stylish gradient title
  - Hover effects for poster cards

- ⭐ **Poster + Implementing IMDB rating mechanism**
  - Real-time data fetched from **TMDB API**
  - Displays poster based on IMDB average rating mechanism

- 🔍 **Smart Matching**
  - Handles typos, partial matches, franchise similarity using `fuzzywuzzy` and `regex`


## 🧪 How It Works

1. **Preprocessing & Tag Creation**:
   - Extracts data from multiple columns (overview, genres, keywords, cast, crew)
   - Cleans and combines into a single `tags` field
   - Applies stemming and tokenization

2. **Vectorization & Similarity**:
   - Transforms tags into numerical vectors using `TF-IDF`
   - Computes similarity with `cosine_similarity`

3. **Recommendation Engine**:
   - Ranks movies based on similarity, genre overlap, vote count, rating
   - Uses `franchise detection` to improve accuracy

4. **Deployment**:
   - Hosted via Streamlit with `setup.sh` and `config.toml`
   - Packaged using `requirements.txt` for smooth deployment

---

## 🛠 Local Setup

```bash
# 1. Clone the repo
git clone https://github.com/MrigakshDasani/Movie_recommendor
cd movie_recommendor

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate   # on Windows use venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the app
streamlit run app.py
