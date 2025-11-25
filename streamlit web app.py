import streamlit as st
import pickle
import requests
import random
import time

# Page configuration
st.set_page_config(page_title="Movie Recommender", page_icon="🎬", layout="wide")

# Initialize session state for splash screen
if 'splash_shown' not in st.session_state:
    st.session_state.splash_shown = False

# Splash Screen
if not st.session_state.splash_shown:
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700;900&display=swap');
        
        .splash-screen {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100vh;
            background: linear-gradient(rgba(15, 17, 21, 0.95), rgba(15, 17, 21, 0.98)), 
                        url('https://img.sanishtech.com/u/84f7f76c3a17dbe36ea2a8e0da2512e3.jpg');
            background-size: cover;
            background-position: center;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            z-index: 9999;
            animation: fadeOut 3s ease-in-out 2s forwards;
        }
        
        @keyframes fadeOut {
            to {
                opacity: 0;
                visibility: hidden;
            }
        }
        
        .splash-logo {
            font-family: 'Poppins', sans-serif;
            font-size: 5rem;
            font-weight: 900;
            background: linear-gradient(135deg, #E50914 0%, #FFB200 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            animation: glow 2s ease-in-out infinite, slideIn 1s ease-out;
            letter-spacing: 3px;
        }
        
        @keyframes glow {
            0%, 100% {
                filter: drop-shadow(0 0 20px rgba(229, 9, 20, 0.6));
            }
            50% {
                filter: drop-shadow(0 0 40px rgba(229, 9, 20, 0.9));
            }
        }
        
        @keyframes slideIn {
            from {
                transform: translateY(-50px);
                opacity: 0;
            }
            to {
                transform: translateY(0);
                opacity: 1;
            }
        }
        
        .splash-subtitle {
            font-family: 'Poppins', sans-serif;
            font-size: 1.3rem;
            color: #FFB200;
            margin-top: 20px;
            font-weight: 300;
            letter-spacing: 2px;
            animation: fadeIn 1.5s ease-out;
        }
        
        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }
        
        .loading-bar {
            width: 300px;
            height: 3px;
            background: rgba(255, 178, 0, 0.2);
            border-radius: 10px;
            margin-top: 40px;
            overflow: hidden;
        }
        
        .loading-progress {
            height: 100%;
            background: linear-gradient(90deg, #E50914, #FFB200);
            animation: loading 2s ease-in-out;
            border-radius: 10px;
        }
        
        @keyframes loading {
            from { width: 0%; }
            to { width: 100%; }
        }
        </style>
        
        <div class="splash-screen">
            <div class="splash-logo">MOVIE RECOMMENDER</div>
            <div class="splash-subtitle">Discover Your Next Favorite</div>
            <div class="loading-bar">
                <div class="loading-progress"></div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    time.sleep(5)
    st.session_state.splash_shown = True
    st.rerun()

# Main App CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800;900&family=Montserrat:wght@400;600;700&display=swap');
    
    /* Global styles */
    .stApp {
        background: linear-gradient(rgba(15, 17, 21, 0.88), rgba(15, 17, 21, 0.92)), 
                    url('https://img.sanishtech.com/u/84f7f76c3a17dbe36ea2a8e0da2512e3.jpg');
        background-size: cover;
        background-attachment: fixed;
        background-position: center;
        filter: blur(0px);
        color: #F2F2F2;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Header */
    .main-header {
        background: linear-gradient(180deg, rgba(26, 28, 34, 0.95) 0%, rgba(26, 28, 34, 0.85) 100%);
        backdrop-filter: blur(15px);
        border-bottom: 2px solid #E50914;
        padding: 18px 50px;
        margin-bottom: 40px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        box-shadow: 0 4px 20px rgba(229, 9, 20, 0.2);
    }
    
    .logo-container {
        display: flex;
        align-items: center;
        gap: 15px;
    }
    
    .logo-icon {
        font-size: 2.5rem;
        animation: rotate 4s linear infinite;
    }
    
    @keyframes rotate {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
    }
    
    .logo-text {
        font-family: 'Poppins', sans-serif;
        font-size: 1.8rem;
        font-weight: 800;
        background: linear-gradient(135deg, #E50914 0%, #FFB200 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        letter-spacing: 2px;
        text-transform: uppercase;
    }
    
    /* Hero Section */
    .hero-section {
        max-width: 900px;
        margin: 0 auto 50px auto;
        padding: 0 20px;
        text-align: center;
    }
    
    .hero-title {
        font-family: 'Poppins', sans-serif;
        font-size: 3rem;
        font-weight: 800;
        color: #F2F2F2;
        margin-bottom: 15px;
        text-shadow: 0 4px 10px rgba(0, 0, 0, 0.5);
    }
    
    .hero-title span {
        background: linear-gradient(135deg, #E50914 0%, #FFB200 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .hero-subtitle {
        font-family: 'Poppins', sans-serif;
        font-size: 1.1rem;
        color: #B8B8B8;
        font-weight: 300;
        line-height: 1.6;
    }
    
    /* Search Box */
    .stSelectbox > div > div {
        background: #1A1C22;
        border: 2px solid rgba(229, 9, 20, 0.3);
        border-radius: 12px;
        color: #F2F2F2;
        font-family: 'Poppins', sans-serif;
        font-size: 1.05rem;
        padding: 12px;
        transition: all 0.3s ease;
    }
    
    .stSelectbox > div > div:hover,
    .stSelectbox > div > div:focus {
        border-color: #E50914;
        box-shadow: 0 0 20px rgba(229, 9, 20, 0.3);
    }
    
    .stSelectbox label {
        font-family: 'Poppins', sans-serif;
        font-size: 1.1rem;
        color: #F2F2F2;
        font-weight: 600;
        margin-bottom: 10px;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #E50914 0%, #B5070F 100%);
        color: #F2F2F2;
        border: none;
        border-radius: 10px;
        padding: 14px 32px;
        font-size: 1rem;
        font-weight: 700;
        font-family: 'Poppins', sans-serif;
        cursor: pointer;
        transition: all 0.3s ease;
        width: 100%;
        text-transform: uppercase;
        letter-spacing: 1px;
        box-shadow: 0 4px 15px rgba(229, 9, 20, 0.4);
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #FF0A16 0%, #E50914 100%);
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(229, 9, 20, 0.6);
    }
    
    /* Genre Expander */
    .streamlit-expanderHeader {
        background: #1A1C22;
        border: 2px solid rgba(255, 178, 0, 0.3);
        border-radius: 10px;
        color: #F2F2F2;
        font-family: 'Poppins', sans-serif;
        font-weight: 600;
        padding: 15px;
        transition: all 0.3s ease;
    }
    
    .streamlit-expanderHeader:hover {
        border-color: #FFB200;
        box-shadow: 0 0 20px rgba(255, 178, 0, 0.2);
    }
    
    /* Movie Cards */
    @keyframes cardPop {
        from {
            opacity: 0;
            transform: scale(0.9) translateY(20px);
        }
        to {
            opacity: 1;
            transform: scale(1) translateY(0);
        }
    }
    
    .movie-card {
        background: #1A1C22;
        border: 2px solid rgba(229, 9, 20, 0.2);
        border-radius: 12px;
        padding: 12px;
        transition: all 0.4s ease;
        cursor: pointer;
        margin: 10px 0;
        animation: cardPop 0.5s ease-out;
        position: relative;
        overflow: hidden;
    }
    
    .movie-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(229, 9, 20, 0.1), transparent);
        transition: left 0.5s ease;
    }
    
    .movie-card:hover::before {
        left: 100%;
    }
    
    .movie-card:hover {
        transform: translateY(-10px) scale(1.03);
        border-color: #E50914;
        box-shadow: 0 12px 30px rgba(229, 9, 20, 0.5);
        background: linear-gradient(135deg, #1A1C22 0%, #252830 100%);
    }
    
    .movie-title {
        font-family: 'Poppins', sans-serif;
        font-size: 0.92rem;
        color: #F2F2F2;
        text-align: center;
        margin-top: 12px;
        font-weight: 600;
        height: 44px;
        overflow: hidden;
        text-overflow: ellipsis;
        display: -webkit-box;
        -webkit-line-clamp: 2;
        -webkit-box-orient: vertical;
        line-height: 1.5;
    }
    
    /* Section Title */
    .section-title {
        font-family: 'Poppins', sans-serif;
        font-size: 2rem;
        font-weight: 700;
        color: #F2F2F2;
        margin: 50px 0 30px 0;
        text-align: center;
        position: relative;
        padding-bottom: 15px;
    }
    
    .section-title::after {
        content: '';
        position: absolute;
        bottom: 0;
        left: 50%;
        transform: translateX(-50%);
        width: 100px;
        height: 3px;
        background: linear-gradient(90deg, #E50914, #FFB200);
        border-radius: 5px;
    }
    
    .section-title span {
        color: #FFB200;
    }
    
    /* Images */
    img {
        border-radius: 8px;
        width: 100%;
        height: auto;
        object-fit: cover;
        transition: all 0.3s ease;
    }
    
    .movie-card:hover img {
        transform: scale(1.05);
    }
    
    /* Column Animation */
    [data-testid="column"] {
        padding: 0 10px;
        animation: cardPop 0.6s ease-out;
    }
    
    [data-testid="column"]:nth-child(1) { animation-delay: 0.05s; }
    [data-testid="column"]:nth-child(2) { animation-delay: 0.1s; }
    [data-testid="column"]:nth-child(3) { animation-delay: 0.15s; }
    [data-testid="column"]:nth-child(4) { animation-delay: 0.2s; }
    [data-testid="column"]:nth-child(5) { animation-delay: 0.25s; }
    
    /* Loading Spinner */
    .stSpinner > div {
        border-color: #E50914 transparent transparent transparent !important;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 40px;
        color: #666;
        font-family: 'Poppins', sans-serif;
        font-size: 0.9rem;
        margin-top: 80px;
        border-top: 1px solid rgba(229, 9, 20, 0.2);
    }
    
    .footer-text {
        color: #999;
        font-weight: 300;
    }
    
    .footer-email {
        color: #E50914;
        font-weight: 600;
        text-decoration: none;
    }
    
    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: #0F1115;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(180deg, #E50914, #FFB200);
        border-radius: 5px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(180deg, #FF0A16, #FFD54F);
    }
    </style>
""", unsafe_allow_html=True)

# Load data
@st.cache_data
def load_data():
    movie = pickle.load(open("movie.pkl", 'rb'))
    similarity = pickle.load(open("simliarity.pkl", 'rb'))
    return movie, similarity

movie, similarity = load_data()
movies_list = movie['title'].values

# Initialize session states
if 'show_genre_results' not in st.session_state:
    st.session_state.show_genre_results = False
if 'selected_genre' not in st.session_state:
    st.session_state.selected_genre = None
if 'show_random' not in st.session_state:
    st.session_state.show_random = False

# Header
st.markdown("""
    <div class="main-header">
        <div class="logo-container">
            <div class="logo-icon">🎬</div>
            <div class="logo-text">Movie Recommender</div>
        </div>
    </div>
""", unsafe_allow_html=True)

# Hero Section
st.markdown("""
    <div class="hero-section">
        <div class="hero-title">Find Your <span>Perfect Movie</span></div>
        <div class="hero-subtitle">Search thousands of movies and get instant AI-powered recommendations tailored to your taste</div>
    </div>
""", unsafe_allow_html=True)

# Search Box
select_movie = st.selectbox(
    "🔍 Search for a movie",
    movies_list,
    key="movie_search"
)

# Action Buttons
col1, col2 = st.columns([1, 1])

with col1:
    show_recommend = st.button("🎯 Get Recommendations", use_container_width=True)

with col2:
    if st.button("🎲 Surprise Me", use_container_width=True):
        st.session_state.show_random = True
    else:
        if 'show_random' not in st.session_state:
            st.session_state.show_random = False

# Genre Filter
with st.expander("🎭 Browse by Genre", expanded=False):
    genres = ["Action", "Comedy", "Drama", "Horror", "Romance", "Sci-Fi", "Thriller", "Animation"]
    
    genre_cols = st.columns(4)
    for idx, genre in enumerate(genres):
        with genre_cols[idx % 4]:
            if st.button(genre, key=f"genre_{genre}", use_container_width=True):
                st.session_state.show_genre_results = True
                st.session_state.selected_genre = genre

def fetch_poster(movie_id):
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=c7ec19ffdd3279641fb606d19ceb9bb1&language=en-US"
        data = requests.get(url, timeout=5)
        data = data.json()
        poster_path = data.get('poster_path')
        if poster_path:
            return f"https://image.tmdb.org/t/p/w500/{poster_path}"
        return "https://via.placeholder.com/500x750?text=No+Poster"
    except:
        return "https://via.placeholder.com/500x750?text=No+Poster"

def get_movie_genres(movie_id):
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=c7ec19ffdd3279641fb606d19ceb9bb1&language=en-US"
        data = requests.get(url, timeout=5)
        data = data.json()
        genres = [g['name'] for g in data.get('genres', [])]
        return genres
    except:
        return []

def recommender(movies):
    index = movie[movie['title'] == movies].index[0]
    distance = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda vector: vector[1])
    recommend_movie = []
    recommend_poster = []
    for i in distance[1:11]:
        movie_id = int(movie.iloc[i[0]].id)
        recommend_movie.append(movie.iloc[i[0]].title)
        recommend_poster.append(fetch_poster(movie_id))
    return recommend_movie, recommend_poster

def get_genre_based_movies(genre):
    genre_movies = []
    genre_posters = []
    sampled_movies = random.sample(list(movies_list), min(50, len(movies_list)))
    
    for movie_title in sampled_movies:
        try:
            movie_id = int(movie[movie['title'] == movie_title].iloc[0].id)
            movie_genres = get_movie_genres(movie_id)
            
            if genre in movie_genres:
                genre_movies.append(movie_title)
                genre_posters.append(fetch_poster(movie_id))
                
                if len(genre_movies) >= 10:
                    break
        except:
            continue
    
    while len(genre_movies) < 10:
        random_movie = random.choice(list(movies_list))
        if random_movie not in genre_movies:
            try:
                movie_id = int(movie[movie['title'] == random_movie].iloc[0].id)
                genre_movies.append(random_movie)
                genre_posters.append(fetch_poster(movie_id))
            except:
                continue
    
    return genre_movies[:10], genre_posters[:10]

def get_random_recommendations():
    random_movies = random.sample(list(movies_list), min(10, len(movies_list)))
    recommend_poster = []
    for movie_title in random_movies:
        try:
            movie_id = int(movie[movie['title'] == movie_title].iloc[0].id)
            recommend_poster.append(fetch_poster(movie_id))
        except:
            recommend_poster.append("https://via.placeholder.com/500x750?text=No+Poster")
    return random_movies, recommend_poster

# Display Recommendations
if show_recommend:
    with st.spinner('✨ Finding perfect matches...'):
        movie_name, movie_poster = recommender(select_movie)
    
    st.markdown(f'<div class="section-title">Based on <span>"{select_movie}"</span></div>', unsafe_allow_html=True)
    
    for row in range(2):
        cols = st.columns(5)
        for col_idx in range(5):
            movie_idx = row * 5 + col_idx
            if movie_idx < len(movie_name):
                with cols[col_idx]:
                    st.markdown('<div class="movie-card">', unsafe_allow_html=True)
                    st.image(movie_poster[movie_idx], use_container_width=True)
                    st.markdown(f'<div class="movie-title">{movie_name[movie_idx]}</div>', unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)

if st.session_state.show_random:
    with st.spinner('🎲 Picking surprises...'):
        movie_name, movie_poster = get_random_recommendations()
    
    st.markdown('<div class="section-title">Random <span>Picks</span></div>', unsafe_allow_html=True)
    
    for row in range(2):
        cols = st.columns(5)
        for col_idx in range(5):
            movie_idx = row * 5 + col_idx
            if movie_idx < len(movie_name):
                with cols[col_idx]:
                    st.markdown('<div class="movie-card">', unsafe_allow_html=True)
                    st.image(movie_poster[movie_idx], use_container_width=True)
                    st.markdown(f'<div class="movie-title">{movie_name[movie_idx]}</div>', unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)

if st.session_state.show_genre_results and st.session_state.selected_genre:
    with st.spinner(f'🎬 Loading {st.session_state.selected_genre} movies...'):
        movie_name, movie_poster = get_genre_based_movies(st.session_state.selected_genre)
    
    st.markdown(f'<div class="section-title"><span>{st.session_state.selected_genre}</span> Movies</div>', unsafe_allow_html=True)
    
    for row in range(2):
        cols = st.columns(5)
        for col_idx in range(5):
            movie_idx = row * 5 + col_idx
            if movie_idx < len(movie_name):
                with cols[col_idx]:
                    st.markdown('<div class="movie-card">', unsafe_allow_html=True)
                    st.image(movie_poster[movie_idx], use_container_width=True)
                    st.markdown(f'<div class="movie-title">{movie_name[movie_idx]}</div>', unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("""
    <div class="footer">
        <p class="footer-text">Made with ❤️ by <a href="mailto:azan@96809@gmail.com" class="footer-email">azan@96809@gmail.com</a></p>
    </div>
""", unsafe_allow_html=True)