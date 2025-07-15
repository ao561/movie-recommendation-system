# Movie Recommendation System
## 📊 Dataset
This project uses the TMDB 5000 Movie Dataset available on Kaggle. It contains data on over 5,000 movies, including plot summaries, cast, crew, budget, and more.

[Link to the dataset on Kaggle](https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata)



## 🛠️ How It Works
The recommendation engine is built using the following pipeline:

1. **Data Cleaning & Merging:** The initial movie and credit datasets are loaded and merged. Irrelevant columns are dropped and missing values are handled.

2. **Feature Extraction:** Key information like genres, keywords, cast (top 5 actors), and the director are extracted from the raw text data.

3. **Feature Engineering:** The extracted features and the plot overview are combined into a single "tags" string for each movie. This string acts as the unique profile for each film.

4. **Stemming:** Each word in the "tags" is reduced to its root form (e.g., "loving" becomes "love") using NLTK's PorterStemmer.

5. **Text Vectorization using TF-IDF:** Each movie's "tags" string is converted into a numerical vector using TfidfVectorizer (5000 features). This creates a vector space where each movie has a unique position.

6. **Cosine Similarity:** The cosine similarity is calculated between all movie vectors. The resulting score (from 0 to 1) represents how similar the movies are. A score closer to 1 indicates a higher similarity.

7. **Recommendation:** When you input a movie, the system finds its vector and returns the movies with the highest similarity scores.

## ⚙️ How to Run
### 1. Initial Setup
First, clone the repository and set up the environment.
``` bash
# Clone the repository
git clone https://github.com/ao561/movie-recommendation-system.git
cd movie-recommendation-system

# Create and activate a virtual environment
python -m venv .venv
# On Windows:
.\.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate

# Install the required packages
pip install pandas numpy scikit-learn nltk streamlit requests
```
### 2. Processing the Data (First Time Only)
Run the `main.py` script once to process all the data and create the cached files.
``` bash
python main.py
```
This will generate two files: `movies_dict.pkl` and `similarity.pkl`.
### 3. Run the Web Application
Launch the interactive front-end by running the following command in your terminal:
``` bash
streamlit run app.py
```
