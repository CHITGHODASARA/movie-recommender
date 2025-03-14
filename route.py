# from flask import Flask, render_template, request
# import pickle
# import pandas as pd
# import requests

# # Load the saved model
# with open("cosine_similarity_model.pkl", "rb") as model_file:
#     vectorizer, cosine_sim, movies = pickle.load(model_file)

# # Function to fetch movie posters from TMDB
# def fetch_poster(movie_title):
#     api_key = "8265bd1679663a7ea12ac168da84d2e8"  # Replace with your TMDB API key
#     url = f"https://api.themoviedb.org/3/search/movie?api_key={api_key}&query={movie_title}"
#     response = requests.get(url).json()
#     if response["results"]:
#         poster_path = response["results"][0].get("poster_path")
#         if poster_path:
#             return f"https://image.tmdb.org/t/p/w500/{poster_path}"
#     return "https://via.placeholder.com/150"  # Default placeholder image if no poster is found

# # Function to get movie recommendations
# def get_recommendations(title, movies_df, cosine_sim_matrix, top_n=5):
#     idx = movies_df[movies_df["title"] == title].index
#     if len(idx) == 0:
#         return []
#     idx = idx[0]
#     similarity_scores = sorted(enumerate(cosine_sim_matrix[idx]), key=lambda x: x[1], reverse=True)
#     similarity_scores = similarity_scores[1:top_n+1]
#     movie_indices = [i[0] for i in similarity_scores]

#     recommended_movies = []
#     for i in movie_indices:
#         movie_title = movies_df.iloc[i]["title"]
#         poster_url = fetch_poster(movie_title)
#         recommended_movies.append((movie_title, poster_url))

#     return recommended_movies

# # Initialize Flask app
# app = Flask(__name__)

# @app.route('/', methods=['GET', 'POST'])
# def home():
#     recommendations = []
#     movie_name = ""
#     if request.method == 'POST':
#         movie_name = request.form['movie_name']
#         recommendations = get_recommendations(movie_name, movies, cosine_sim)
#     return render_template('index.html', recommendations=recommendations, movie_name=movie_name, movies=movies["title"].tolist())

# if __name__ == '__main__':
#     app.run(debug=True)
