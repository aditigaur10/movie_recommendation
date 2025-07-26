import pandas as pd
import ast
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pickle

# Load the datasets
movies = pd.read_csv(r'C:\Users\aditi\Downloads\archive (1)\tmdb_5000_movies.csv')
credits = pd.read_csv(r'C:\Users\aditi\Downloads\archive (1)\tmdb_5000_credits.csv')

# Merge datasets on title
movies = movies.merge(credits, on='title')

# Keep relevant columns
movies = movies[['movie_id', 'title', 'overview', 'genres', 'keywords', 'cast', 'crew']]

# Define functions to extract useful text
def convert(obj):
    L = []
    for i in ast.literal_eval(obj):
        L.append(i['name'])
    return L

def convert_cast(obj):
    L = []
    for i in ast.literal_eval(obj):
        if i['order'] < 3:
            L.append(i['name'])
    return L

def fetch_director(obj):
    for i in ast.literal_eval(obj):
        if i['job'] == 'Director':
            return [i['name']]
    return []

def collapse(L):
    return " ".join(L)

# Apply all conversions
movies.dropna(inplace=True)
movies['genres'] = movies['genres'].apply(convert)
movies['keywords'] = movies['keywords'].apply(convert)
movies['cast'] = movies['cast'].apply(convert_cast)
movies['crew'] = movies['crew'].apply(fetch_director)
movies['overview'] = movies['overview'].apply(lambda x: x.split())

# Combine all tags
movies['tags'] = movies['overview'] + movies['genres'] + movies['keywords'] + movies['cast'] + movies['crew']
movies['tags'] = movies['tags'].apply(lambda x: " ".join(x))

# Final dataframe
new_df = movies[['movie_id', 'title', 'tags']]

# Convert tags to vectors
cv = CountVectorizer(max_features=5000, stop_words='english')
vectors = cv.fit_transform(new_df['tags']).toarray()

# Compute similarity
similarity = cosine_similarity(vectors)

# Save pickles
pickle.dump(new_df, open('movies.pkl', 'wb'))
pickle.dump(similarity, open('similarity.pkl', 'wb'))

print("✅ Pickles generated successfully!")
