# app.py
import streamlit as st
import pandas as pd
import ast
import pickle
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# -----------------------------------------------------------
#  Function to Load and Preprocess Data (Cached for Speed)
# -----------------------------------------------------------
@st.cache_resource
def load_data():
    # Load datasets
    movies = pd.read_csv("tmdb_5000_movies.csv")
    credits = pd.read_csv("tmdb_5000_credits.csv")
    # Merge datasets on title
    movies = movies.merge(credits, on='title')

    # Keep only important columns
    movies = movies[['id', 'title', 'overview', 'genres', 'keywords', 'cast', 'crew']]
    movies.dropna(inplace=True)

    # Helper function to convert stringified lists
    def convert(obj):
        L = []
        for i in ast.literal_eval(obj):
            L.append(i['name'])
        return L

    # Extract top 3 cast
    def convert_cast(obj):
        L = []
        counter = 0
        for i in ast.literal_eval(obj):
            if counter < 3:
                L.append(i['name'])
                counter += 1
        return L

    # Extract director name
    def fetch_director(obj):
        L = []
        for i in ast.literal_eval(obj):
            if i['job'] == 'Director':
                L.append(i['name'])
                break
        return L

    # Apply transformations
    movies['genres'] = movies['genres'].apply(convert)
    movies['keywords'] = movies['keywords'].apply(convert)
    movies['cast'] = movies['cast'].apply(convert_cast)
    movies['crew'] = movies['crew'].apply(fetch_director)

    # Remove spaces in multi-word names
    def collapse(L):
        return [i.replace(" ", "") for i in L]

    movies['genres'] = movies['genres'].apply(collapse)
    movies['keywords'] = movies['keywords'].apply(collapse)
    movies['cast'] = movies['cast'].apply(collapse)
    movies['crew'] = movies['crew'].apply(collapse)

    # Combine features
    def join_features(row):
        return (
            row['overview']
            + " "
            + " ".join(row['genres'])
            + " "
            + " ".join(row['keywords'])
            + " "
            + " ".join(row['cast'])
            + " "
            + " ".join(row['crew'])
        )

    movies['tags'] = movies.apply(join_features, axis=1)

    # Create new DataFrame for model
    new_df = movies[['id', 'title', 'tags']]
    new_df['tags'] = new_df['tags'].apply(lambda x: x.lower())

    # Vectorize text
    cv = CountVectorizer(max_features=5000, stop_words='english')
    vectors = cv.fit_transform(new_df['tags']).toarray()

    # Compute cosine similarity matrix
    similarity = cosine_similarity(vectors)

    return new_df, similarity


# -----------------------------------------------------------
#  Recommendation Function
# -----------------------------------------------------------
def recommend(movie):
    movie = movie.lower()
    if movie not in new_df['title'].str.lower().values:
        return ["Movie not found in dataset."]
    movie_index = new_df[new_df['title'].str.lower() == movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    recs = []
    for i in movie_list:
        recs.append(new_df.iloc[i[0]].title)
    return recs


# -----------------------------------------------------------
#  Streamlit App Interface
# -----------------------------------------------------------
st.title("🎬 AI Movie Recommendation System")
st.write("This AI-powered app recommends movies based on content similarity using NLP and Machine Learning.")

# Load data (cached)
with st.spinner("Loading data and computing similarities... (this may take a minute on first run)"):
    new_df, similarity = load_data()

# Movie selection dropdown
selected_movie_name = st.selectbox("🎥 Select a movie you like:", new_df['title'].values)

# Show recommendations
if st.button("🔍 Recommend"):
    with st.spinner("Finding similar movies..."):
        recommendations = recommend(selected_movie_name)
    st.subheader("✅ Recommended Movies:")
    for i in recommendations:
        st.write("👉", i)

st.success("App is ready! You can now get instant movie recommendations.")
