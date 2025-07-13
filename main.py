import numpy as np
import pandas as pd
import ast

movies = pd.read_csv('tmdb_5000_movies.csv')
credits = pd.read_csv('tmdb_5000_credits.csv')

# merging dataframes via id
movies = movies.merge(credits, left_on='id', right_on='movie_id')

# relevant columns: genres, id, keywords, title, overview, cast, crew
movies = movies[['original_title', 'id', 'genres', 'overview', 'keywords', 'cast', 'crew']]
movies.dropna(inplace = True)

# functions to parse data
def extract_name(text):
    names = []
    for map in ast.literal_eval(text):
        names.append(map['name'])
    return names

def extract_director(text):
    name = []
    for map in ast.literal_eval(text):
        if map['job'] == 'Director':
            name.append(map['name'])
            break
    return name

# parsing data
movies['genres'] = movies['genres'].apply(extract_name)
movies['keywords'] = movies['keywords'].apply(extract_name)
movies['cast'] = movies['cast'].apply(extract_name).apply(lambda x: x[:3])
movies['crew'] = movies['crew'].apply(extract_director)



