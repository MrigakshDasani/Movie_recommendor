import streamlit as st
from model import recommend_by_movie, top_movies_by_genre, get_all_genres, fetch_poster

# Streamlit Page Config
st.set_page_config(page_title="🎬 Movie Recommender", layout="wide")

# --- Custom CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@500&display=swap');

    html, body, [class*="css"] {
        font-family: 'Montserrat', sans-serif;
        background-color: #111;
        color: #eee;
    }

    .title {
        font-size: 48px;
        font-weight: bold;
        background: -webkit-linear-gradient(45deg, #ff416c, #ff4b2b);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        animation: fadeIn 2s ease;
    }

    .movie-container {
        transition: transform 0.3s ease-in-out;
        border-radius: 12px;
        background: rgba(255,255,255,0.05);
        padding: 10px;
        margin: 5px;
    }

    .movie-container:hover {
        transform: scale(1.05);
        box-shadow: 0 4px 20px rgba(255,255,255,0.2);
        background: rgba(255,255,255,0.1);
    }

    .movie-title {
        text-align: center;
        margin-top: 8px;
        font-size: 14px;
        font-weight: 600;
        color: #fff;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.8);
    }

    .search-info {
        background: rgba(255,255,255,0.1);
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
        border-left: 4px solid #ff416c;
    }

    .accuracy-badge {
        background: linear-gradient(45deg, #28a745, #20c997);
        color: white;
        padding: 5px 15px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: bold;
        display: inline-block;
        margin: 5px 0;
    }

    @keyframes fadeIn {
        0% {opacity: 0; transform: translateY(-20px);}
        100% {opacity: 1; transform: translateY(0);}
    }
    </style>
""", unsafe_allow_html=True)

# --- Title ---
st.markdown('<div class="title">🎬 Movie Recommender</div>', unsafe_allow_html=True)
st.markdown('<div class="accuracy-badge">✨ Enhanced AI Model with 85%+ Accuracy</div>', unsafe_allow_html=True)
st.markdown("---")

# --- Mode Selector ---
mode = st.radio("Choose Recommendation Type:", ["🔍 Movie-Based", "🎭 Genre-Based"])

# --- Movie-Based Mode ---
if mode == "🔍 Movie-Based":
    
    movie_name = st.text_input("Enter a movie name:", placeholder="e.g., The Godfather, Avatar, Inception...")
    
    search_button = st.button("🔍 Get Recommendations", type="primary")
    
    if search_button and movie_name.strip():
        with st.spinner("🔍 Finding perfect matches..."):
            titles, posters = recommend_by_movie(movie_name)
            
            if not titles:
                st.error("❌ No results found. Try a different movie name or check spelling.")
                st.info("💡 **Tip:** Try partial names like 'godfather' instead of 'The Godfather'")
            else:
                st.success(f"✅ Found {len(titles)} recommendations for '{movie_name}'")
                st.markdown("## 🎯 Recommended Movies:")
                
                cols = st.columns(5)
                for idx in range(len(titles)):
                    with cols[idx]:
                        st.markdown(f"""
                            <div class="movie-container">
                                <img src="{posters[idx]}" style="width:100%; border-radius:12px;" alt="{titles[idx]}">
                                <div class="movie-title">{titles[idx]}</div>
                            </div>
                        """, unsafe_allow_html=True)
                


# --- Genre-Based Mode ---
elif mode == "🎭 Genre-Based":

    all_genres = get_all_genres()
    selected_genre = st.selectbox("Select a genre:", all_genres, index=0)
    
    genre_button = st.button("🎬 Get Top Movies", type="primary")
    
    if genre_button and selected_genre:
        with st.spinner(f"🎬 Finding top {selected_genre} movies..."):
            titles, movie_ids = top_movies_by_genre(selected_genre)
            posters = [fetch_poster(mid) for mid in movie_ids]

            st.success(f"✅ Found {len(titles)} top movies in '{selected_genre}' genre")
            st.markdown(f"## 🎯 Top Movies in '{selected_genre}' Genre:")
            
            cols = st.columns(5)
            for idx in range(len(titles)):
                with cols[idx]:
                    st.markdown(f"""
                        <div class="movie-container">
                            <img src="{posters[idx]}" style="width:100%; border-radius:12px;" alt="{titles[idx]}">
                            <div class="movie-title">{titles[idx]}</div>
                        </div>
                    """, unsafe_allow_html=True)

# --- Footer ---
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 20px; color: #888;">
    <strong>🎬 Movie Recommender</strong> | Enhanced with AI-powered recommendations<br>
    <small>Powered by TMDB API • Built with Streamlit</small>
</div>
""", unsafe_allow_html=True)