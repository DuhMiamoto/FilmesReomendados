import streamlit as st
import pandas
import pickle
import requests
import dotenv
import os
import gzip

# efetivamente carrega os valores do arquivo
dotenv.load_dotenv(dotenv.find_dotenv())


def fetch_poster(movie_id):

    response = requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={API}')
    data = response.json()

    return f'https://image.tmdb.org/t/p/w500/{data["poster_path"]}'


def recommended(movie):
    movie_index = movie_list[movie_list['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recomended_movies_posters = []

    for i in movies:
        movie_id = movie_list.iloc[i[0]].movie_id
        # fetch poster from API

        recommended_movies.append(movie_list.iloc[i[0]].title)
        recomended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies, recomended_movies_posters


API = os.getenv('API')

movie_list = pickle.load(open('movies.pkl', 'rb'))

movie_list_values = movie_list['title'].values

with gzip.open('similarity.pkl.gz', 'rb') as file: 
    similarity = pickle.load(file)

st.title('Recomendação de Filmes')

select_movie_name = st.selectbox(
    'Escolha um filme',
    (movie_list_values))

if st.button('Recomendação'):
    names, posters = recommended(select_movie_name)

    num_columns = 5  # Número de colunas desejado
    cols = st.columns(num_columns)

    for i, name in enumerate(names[:num_columns]):
        with cols[i]:
            st.image(posters[i])
            if len(name) > 15:
                st.write(name)
            else:
                st.text(name)
