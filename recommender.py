import pickle
import pandas as pd

# loads saved data from files
movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
df = pd.DataFrame(movies_dict)
similarity_matrix = pickle.load(open('similarity.pkl', 'rb'))

# recommendation functions obtains and prints the best 5 matches
def recommend(movie_title):
    try:
        movie_index = df[df['original_title'] == movie_title].index[0]
        score = similarity_matrix[movie_index]
        movies_list = sorted(list(enumerate(score)), reverse = True, key = lambda x: x[1])[1:6]
    
        print(f"Recommendations for '{movie_title}':")
        for i in movies_list:
            print(df.iloc[i[0]].original_title)
    except IndexError:
        print(f"Movie: '{movie_title}' not found in the dataset.")

# user input
title = input("Please enter a movie: ") 
recommend(title)