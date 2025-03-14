from flask import Flask, render_template, request, jsonify
import pickle
import pandas as pd
import requests

# Load the saved model
with open("cosine_similarity_model.pkl", "rb") as model_file:
    vectorizer, cosine_sim, movies = pickle.load(model_file)

# Initialize Flask app
app = Flask(__name__)

# Function to fetch movie poster from TMDb API
def fetch_poster(movie_id):
    api_key = "8265bd1679663a7ea12ac168da84d2e8"
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-US"
    response = requests.get(url)

    if response.status_code != 200:
        print(f"Error fetching poster for movie_id {movie_id}")
        return "https://via.placeholder.com/150"  # Default image
    
    data = response.json()
    
    if 'poster_path' in data and data['poster_path']:
        return f"https://image.tmdb.org/t/p/w500/{data['poster_path']}"
    else:
        return "https://via.placeholder.com/150"  # Default image if no poster available

# Function to get recommendations
def get_recommendations(title, top_n=5):
    if title not in movies["title"].values:
        print(f"Movie '{title}' not found in dataset!")
        return []

    idx = movies[movies["title"] == title].index[0]
    
    # Step 1: Find movies with similar titles (Franchise-based recommendation)
    keyword = title.split()[0]  # Use the first word as the keyword (e.g., "Spider-Man")
    franchise_movies = movies[movies["title"].str.contains(keyword, case=False, na=False)]

    # If there are enough franchise movies, return them first
    if len(franchise_movies) >= top_n:
        recommended_movies = franchise_movies.head(top_n)
    else:
        # Step 2: Get top similar movies using cosine similarity
        similarity_scores = list(enumerate(cosine_sim[idx]))
        similarity_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)
        similarity_scores = similarity_scores[1:top_n+1]  # Exclude the first movie (itself)
        
        recommended_movie_indices = [i[0] for i in similarity_scores]
        recommended_movies = movies.loc[recommended_movie_indices]

    # Step 3: Fetch movie posters
    recommendations = []
    for _, row in recommended_movies.iterrows():
        poster_url = fetch_poster(row['movie_id'])  # Fetch poster using TMDb API
        recommendations.append({
            "title": row['title'],
            "poster_path": poster_url
        })
    
    print(f"Selected Movie: {title}")
    print("Recommended Movies:", recommendations)
    
    return recommendations

# Flask routes
@app.route("/")
def home():
    movie_list = movies["title"].tolist()
    return render_template("index.html", movies=movie_list)

@app.route("/recommend", methods=["POST"])
def recommend():
    data = request.get_json()
    movie_name = data.get("movie", "")

    recommendations = get_recommendations(movie_name)

    return jsonify(recommendations)

if __name__ == "__main__":
    app.run(debug=True)
