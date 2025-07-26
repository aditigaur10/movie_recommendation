import streamlit as st
import pickle
import pandas as pd
import requests

# Load data
movies = pickle.load(open('movies.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Function to fetch poster from TMDB API
def fetch_poster(movie_title):
    try:
        response = requests.get(
          f'https://api.themoviedb.org/3/search/movie?api_key=<<04f748c6bd453a2bd9b0742caf32f786>>&query={movie_title}'

        )
        data = response.json()
        poster_path = data['results'][0]['poster_path']
        full_path = "https://image.tmdb.org/t/p/w500" + poster_path
        return full_path
    except:
        return "https://via.placeholder.com/300x450?text=No+Image"

# Recommend function
def recommend(movie):
    movie = movie.lower()
    if movie not in movies['title'].str.lower().values:
        return [], []
    
    movie_index = movies[movies['title'].str.lower() == movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(
        list(enumerate(distances)), reverse=True, key=lambda x: x[1]
    )[1:6]

    recommended_movies = []
    recommended_posters = []
    for i in movie_list:
        title = movies.iloc[i[0]].title
        recommended_movies.append(title)
        recommended_posters.append(fetch_poster(title))
    return recommended_movies, recommended_posters

# Streamlit UI
st.title('🎬 Movie Recommender System')

movie_list = movies['title'].values
selected_movie = st.selectbox("Select a movie you like", movie_list)

if st.button('Recommend'):
    names, posters = recommend(selected_movie)
    if names:
        col1, col2, col3, col4, col5 = st.columns(5)
        cols = [col1, col2, col3, col4, col5]
        for i in range(len(names)):
            with cols[i]:
                st.text(names[i])
                st.image(posters[i])
    else:
        st.warning("Movie not found in database.")
