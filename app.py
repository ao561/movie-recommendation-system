import pickle
import pandas as pd
import streamlit as st
import requests

# loads saved data from files
try:
    movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
    df = pd.DataFrame(movies_dict)
    similarity_matrix = pickle.load(open('similarity.pkl', 'rb'))
except FileNotFoundError:
    st.error("Model files not found. Please run the main.py script first to generate them.")
    st.stop()


# fetches poster url from TMDB API
def fetch_poster(movie_id):
    try:
        api_key = "24e92c3fdd4094bdf0b12f57aa752e9e"
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-US"
        response = requests.get(url)
        response.raise_for_status()  # Raises an HTTPError for bad responses (4xx or 5xx)
        data = response.json()
        poster_path = data.get('poster_path')
        if poster_path:
            return "https://image.tmdb.org/t/p/w500/" + poster_path
        else:
            return "https://via.placeholder.com/500x750.png?text=No+Poster+Available"
    except requests.exceptions.RequestException as e:
        st.error(f"API request failed: {e}")
        return "https://via.placeholder.com/500x750.png?text=API+Error"


# recommendation functions returns the best 5 movie matches and their posters
def recommend(movie_title):
    try:
        movie_index = df[df['original_title'] == movie_title].index[0]
        score = similarity_matrix[movie_index]
        movies_list = sorted(list(enumerate(score)), reverse = True, key = lambda x: x[1])[1:6]

        recommended_movies_details = []

        for i in movies_list:
            movie_details = df.iloc[i[0]]
            movie_id = movie_details.id
            details = {
                'id': movie_id,
                'title': movie_details.original_title,
                'poster': fetch_poster(movie_id),
                'score': round(i[1] * 100, 2), # Convert score to percentage
                'runtime': movie_details.runtime,
                'release_date': movie_details.release_date,
                'vote_average': movie_details.vote_average,
                'overview': movie_details.overview
            }
            recommended_movies_details.append(details)
        return recommended_movies_details
    except IndexError:
        return []

# web app interface

st.title('Movie Recommender System')

st.set_page_config(layout="wide")

# drop down select box
selected_movie_name = st.selectbox(
    'Select a movie to get recommendations:',
    df['original_title'].values)

# button which when clicked shows recommendations
if st.button('Recommend'):
    with st.spinner('Finding recommendations...'):
        recommendations = recommend(selected_movie_name)
        
        if recommendations:
            st.subheader("Here are your top 5 recommendations:")
            # Display each recommendation vertically
            for movie in recommendations:
                st.write("---") # Divider line
                col1, col2 = st.columns([1, 4]) # Poster column is 1/5th of the width
                with col1:
                    st.image(movie['poster'])
                with col2:
                    st.subheader(movie['title'])
                    st.markdown(f"**Similarity Score:** {movie['score']}%")
                    st.markdown(f"**Release Date:** {movie['release_date']}")
                    st.markdown(f"**Runtime:** {int(movie['runtime'])} minutes")
                    st.markdown(f"**Rating:** {movie['vote_average']}/10")
                    st.write("**Overview:**")
                    st.write(movie['overview'])
                    st.markdown(f"[View on TMDB](https://www.themoviedb.org/movie/{movie['id']})")
        else:
            st.warning("Could not find recommendations for the selected movie.")