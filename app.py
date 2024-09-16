import streamlit as st
import pickle
import pandas as pd
import requests

# Custom CSS for styling the app
st.markdown("""
    <style>
    body {
        background: #000000; /* Updated background to full black */
        color: #ffffff; /* White text color for contrast */
        font-family: 'Arial', sans-serif;
    }
    .logo {
        text-align: center;
        margin-top: 20px;
    }
    .logo img {
        width: 150px; /* Adjust width as needed */
        height: auto;
    }
    .title {
        color: #FFD700;
        text-align: center;
        font-size: 42px;
        font-weight: bold;
        margin-top: 20px;
        text-shadow: 2px 2px 5px rgba(0, 0, 0, 0.3);
    }
    .subtitle {
        color: #eee;
        text-align: center;
        font-size: 18px;
        margin-bottom: 40px;
    }
    .featured-section {
        padding: 20px;
        background: rgba(0, 0, 0, 0.8); /* Slightly transparent black for contrast */
        border-radius: 10px;
        margin-bottom: 40px;
    }
    .featured-title {
        color: #FFD700;
        text-align: center;
        font-size: 28px;
        font-weight: bold;
        margin-bottom: 20px;
        text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.3);
    }
    .featured-movie {
        margin-bottom: 20px;
    }
    .featured-movie img {
        border-radius: 15px;
        transition: transform 0.3s ease;
        width: 100%;
        height: auto;
    }
    .featured-movie img:hover {
        transform: scale(1.05);
    }
    .stButton>button {
        background: #FFD700;
        color: black;
        border: none;
        padding: 12px 30px;
        font-size: 16px;
        border-radius: 8px;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background: #FFA500;
        transform: translateY(-3px);
        box-shadow: 0px 4px 15px rgba(0, 0, 0, 0.3);
    }
    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# Fetch poster from TMDB API
def fetch_poster(movie_id):
    try:
        url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=b86a89b1952c1b69a380fca68fe2d524&language=en-US'
        response = requests.get(url)
        data = response.json()

        if 'poster_path' in data and data['poster_path']:
            poster_path = data['poster_path']
            full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
            return full_path
        else:
            return "https://via.placeholder.com/500x750?text=No+Image+Available"
    except Exception as e:
        st.error(f"Error fetching poster: {e}")
        return "https://via.placeholder.com/500x750?text=Error"

# Function to recommend movies based on similarity
def recommend(movie):
    try:
        index = movies[movies['title'] == movie].index[0]
        distances = similarity[index]
        movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

        recommended_movies = []
        recommended_movies_poster = []

        for i in movies_list:
            movie_id = movies.iloc[i[0]].movie_id
            recommended_movies.append(movies.iloc[i[0]].title)
            recommended_movies_poster.append(fetch_poster(movie_id))

        return recommended_movies, recommended_movies_poster
    except Exception as e:
        st.error(f"Error in recommendation function: {e}")
        return [], []

# Load the movie data and similarity matrix
movies_dict = pickle.load(open('movies.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Define featured movies (example IDs or titles)
featured_movies = [
    {'title': 'Inception', 'id': 27205},
    {'title': 'The Matrix', 'id': 603},
    {'title': 'Interstellar', 'id': 157336},
    {'title': 'Parasite', 'id': 496243},
    {'title': 'The Dark Knight', 'id': 155}
]

# TMDB Logo
st.markdown('<div class="logo"><img src="https://www.themoviedb.org/assets/brand/blue_short-1f31520466b0a1fc827d049fa46b43dd3dd041c5a804dc3ec1a0073948c4c027.svg" alt="TMDB Logo" /></div>', unsafe_allow_html=True)

# Centered title and subtitle with updated color and style
st.markdown('<h1 class="title">🎬 Movie Recommender System</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Find the best movies based on your favorite! Select a movie and get top recommendations.</p>', unsafe_allow_html=True)

# Featured movies section
st.markdown('<div class="featured-section"><h2 class="featured-title">Featured Movies</h2>', unsafe_allow_html=True)

# Display featured movies
cols = st.columns(len(featured_movies))
for i, movie in enumerate(featured_movies):
    with cols[i]:
        poster = fetch_poster(movie['id'])
        st.markdown(f"<div class='featured-movie'><img src='{poster}' /></div>", unsafe_allow_html=True)
        st.markdown(f"<p style='text-align: center; color: #FFD700;'>🎬 {movie['title']}</p>", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Movie selection dropdown
selected_movie_name = st.selectbox(
    'Choose a movie to get recommendations:',
    movies['title'].values,
    index=0
)

# Display recommendations on button click with loading animation
if st.button('Get Recommendations 🎥'):
    with st.spinner("Fetching your recommendations..."):
        names, posters = recommend(selected_movie_name)

    if names and posters:
        st.markdown("<h3 style='text-align: center;'>Here are 5 movies we recommend for you:</h3>", unsafe_allow_html=True)

        # Dynamically create columns based on the number of recommendations
        cols = st.columns(5)

        for i, col in enumerate(cols):
            with col:
                st.image(posters[i], use_column_width=True)
                st.markdown(f"<p style='text-align: center;'>🎬 {names[i]}</p>", unsafe_allow_html=True)
    else:
        st.error("Sorry, we couldn't find any recommendations for this movie.")

# Footer section
st.markdown("---")
st.markdown("<p style='text-align: center;'>🎥 Enjoy watching your recommendations! ✨</p>", unsafe_allow_html=True)
