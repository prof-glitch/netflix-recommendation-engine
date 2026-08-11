# Netflix Recommendation Engine

[Live Demo](https://netflix-recommendation-engine-nrqdzge5zdp5ddksrulpyz.streamlit.app/)

A movie recommendation system built using collaborative filtering and SVD. The system predicts movie ratings for a user and recommends the top 10 movies they are most likely to enjoy.

The project includes a Streamlit web application with movie posters fetched from TMDB.

## Features

- Personalized top 10 movie recommendations
- Collaborative filtering using SVD
- Removes movies already watched by the user
- Predicts ratings for unseen movies
- TMDB API integration for movie posters
- Streamlit web interface
- Handles invalid User IDs
- Deployed online using Streamlit Community Cloud

## Screenshots

### App Interface

![App Interface](screenshots/Screenshot%202026-08-11%20224145.png)

### Recommendation Results

![Recommendation Results](screenshots/Screenshot%202026-08-11%20224216.png)

### Movie Recommendations

![Movie Recommendations](screenshots/Screenshot%202026-08-11%20224421.png)

## Problem Statement

With a large number of movies available, users can find it difficult to decide what to watch. The goal of this project is to build a recommendation system that uses a user's previous movie ratings to predict their preferences and recommend movies they have not watched yet.

## How the Recommendation System Works

The system uses collaborative filtering to recommend movies based on user rating patterns.

1. The user's previously rated movies are identified.
2. Movies the user has already watched are removed from the recommendation candidates.
3. The trained SVD model predicts ratings for the remaining movies.
4. The movies are sorted by predicted rating.
5. The top 10 highest-rated movies are recommended.
6. TMDB is used to fetch movie posters for the recommendations.

## SVD Model

Singular Value Decomposition (SVD) is used to learn hidden patterns between users and movies from their rating history.

The model learns latent factors that represent user preferences and movie characteristics. It then uses these learned factors to predict how a user might rate movies they have not watched.

The predicted ratings are used to rank candidate movies and generate the final top 10 recommendations.

## Model Evaluation

The SVD model was evaluated using Root Mean Square Error (RMSE) and Mean Absolute Error (MAE).

| Model | RMSE | MAE |
|---|---:|---:|
| Baseline SVD | 0.9904 | 0.7844 |
| Tuned SVD | 0.9676 | 0.7675 |

The tuned SVD model performed better than the baseline model, reducing both RMSE and MAE.

## Technologies Used

- Python
- Pandas
- Scikit-Surprise
- Streamlit
- TMDB API
- Git
- GitHub
- Git LFS

## Project Structure

```text
netflix-recommendation-engine/
├── app.py
├── best_svd_model.pkl
├── all_movies.pkl
├── user_history.pkl
├── movie_titles.csv
├── requirements.txt
├── README.md
├── .gitignore
├── .gitattributes
└── .streamlit/
    └── secrets.toml
