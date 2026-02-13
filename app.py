import streamlit as st
import pickle
import pandas as pd
import requests

movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

indices = pickle.load(open('indices.pkl', 'rb'))

cs = pickle.load(open('cs.pkl', 'rb'))

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=9b09491307a7f3329e03f9cf3fdc1a90&language=en-US".format(movie_id)
    data = requests.get(url).json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

def recommend(movie,n=5,movies=movies,indices=indices,cs=cs):
    idx = indices[movie]
    sim_scores = cs[idx]
    movie_indices = sim_scores[0:n]
    rec_movies = movies['title'][movie_indices]
    movie_ids = movies['movie_id'][movie_indices].values
    posters = [fetch_poster(movie_id) for movie_id in movie_ids]
    return rec_movies, posters



st.title("Movie Recommender System")

selected_movie = st.selectbox(
    'Select a movie to get recommendations:', movies['title'].values
)

if st.button('Recommend'):
    st.write('You selected:', selected_movie)
    recommendations, posters = recommend(selected_movie, n=5)
    recommendations = recommendations.reset_index(drop=True)
    st.write('Recommended Movies:')
    
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(recommendations[0])
        st.image(posters[0])
    with col2:
        st.text(recommendations[1])
        st.image(posters[1])
    with col3:
        st.text(recommendations[2])
        st.image(posters[2])
    with col4:
        st.text(recommendations[3])
        st.image(posters[3])
    with col5:
        st.text(recommendations[4])
        st.image(posters[4])
