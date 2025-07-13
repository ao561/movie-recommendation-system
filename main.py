import numpy as np
import pandas as pd
import ast
from nltk.stem.porter import PorterStemmer
from sklearn.feature_extraction.text import CountVectorizer

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
movies['cast'] = movies['cast'].apply(extract_name).apply(lambda x: x[:5])
movies['crew'] = movies['crew'].apply(extract_director)
movies['overview'] = movies['overview'].apply(lambda x: x.split())

def remove_spaces(word_list):
    return [i.replace(" ", "") for i in word_list]

movies['genres'] = movies['genres'].apply(remove_spaces)
movies['keywords'] = movies['keywords'].apply(remove_spaces)
movies['cast'] = movies['cast'].apply(remove_spaces)
movies['crew'] = movies['crew'].apply(remove_spaces)

# tag creation
movies['tags'] = movies['overview'] + movies['genres']+ movies['keywords'] + movies['cast'] + movies['crew']

df = movies[['id', 'original_title', 'tags']]
df['tags'] = df['tags'].apply(lambda x: " ".join(x).lower())

ps = PorterStemmer()

# stem tag words to prevent similar repeats when vectorising
def stem(text):
    out = []
    for i in text.split():
        out.append(ps.stem(i))
    return " ".join(out)

df['tags'] = df['tags'].apply(stem)

# text vectorisation via the BoW model
x = CountVectorizer(max_features = 5000, stop_words = 'english')
vectors = x.fit_transform(df['tags']).toarray()








