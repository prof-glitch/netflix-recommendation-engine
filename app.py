import streamlit as st
import pandas as pd
import pickle
import requests
import urllib.request
import urllib.parse
import json
import time


st.set_page_config(
    page_title="Netflix Recommendation Engine",
    page_icon="🎬",
    layout="wide"
)
st.sidebar.title("NETFLIX RECOMMENDATION ENGINE")
st.sidebar.write("This is a application recommends movies " 
"based on the user history using Collaborative Filtering (SVD).")
st.sidebar.markdown("---")
st.sidebar.subheader("How it works")
st.sidebar.write("1. Enter a user ID in the input box.\n"
                 "2. Click on the 'Give Recommendations\n"
                 "3. The model predicts ratings for unrated movies.\n"
                 "4.the top 10 movies are displayed\n")
st.sidebar.markdown("---")
st.sidebar.write("MODEL: SVD")
st.sidebar.write("recommendations: top 10")

#loading the svd model
with open("best_svd_model.pkl", "rb") as f:
  best_model = pickle.load(f) 
  #loading the movies data
with open("all_movies.pkl","rb") as f:
  all_movies=pickle.load(f)
#load movies titles
movie_titles = pd.read_csv("movie_titles.csv")
movie_dict= movie_titles.set_index('movie_id')['movie_name'].to_dict()
#loading the user history
with open('user_history.pkl','rb') as f:
    user_history=pickle.load(f)
st.title("🎬 Netflix Recommendation Engine")
st.markdown("persoalized movie recommendations powered by Collaborative Filtering (SVD)")
st.caption("Enter a user id below and let the svd model find you the movie you would love")
st.markdown("---")
user_id=st.number_input("ENTER USER ID TO GET MOVIE RECOMMENDATIONS",min_value=1,step=1)
recommend_button=st.button("🎬Give Recommendations")

tmdb_token=st.secrets["TMDB_TOKEN"]
def get_poster(movie_name):
    if "poster_cache" not in st.session_state:
        st.session_state.poster_cache={}

    if movie_name in st.session_state.poster_cache:
        return st.session_state.poster_cache[movie_name]

    search_name=movie_name

    if ": Season" in movie_name:
        search_name=movie_name.split(": Season")[0]

    try:
        url="https://api.themoviedb.org/3/search/multi"
        params=urllib.parse.urlencode({"query":search_name,"language":"en-US"})
        request=urllib.request.Request(url+"?"+params,headers={"Authorization":f"Bearer {tmdb_token}","User-Agent":"NetflixRecommendationEngine/1.0"})
        response=urllib.request.urlopen(request,timeout=10)
        data=json.loads(response.read().decode())

        movie_title=search_name.lower().strip()

        for result in data.get("results",[]):
            result_title=result.get("title",result.get("name","")).lower().strip()

            if result.get("media_type")=="tv" and result_title==movie_title and result.get("poster_path"):
                poster="https://image.tmdb.org/t/p/w500"+result["poster_path"]
                st.session_state.poster_cache[movie_name]=poster
                return poster

        return None

    except Exception:
        return None

    


if recommend_button:

    if user_id not in user_history:
        st.warning("User ID not found in the database.")

    else:
     with st.spinner("Generating recommendations ...."):
        st.write(f"### Recommendations for User ID: {user_id}")
        watched_movies=user_history.get(user_id,[])
        movies_to_predict=list(set(all_movies)-set(watched_movies))
        predictions=[]
        for movie in movies_to_predict:
            pred=best_model.predict(user_id,movie)
            predictions.append((movie,pred.est))
        predictions.sort(key=lambda x:x[1],reverse=True)
        top_10=predictions[:10]
        recommendation_df=pd.DataFrame(top_10,columns=["movie_id","predicted_rating"])
        recommendation_df["movie_name"]=recommendation_df["movie_id"].map(movie_dict)
        recommendation_df=recommendation_df[["movie_name","predicted_rating"]]
        recommendation_df["predicted_rating"]=recommendation_df["predicted_rating"].round(2)
        st.subheader("Top 10 Movie Recommendations")
        st.write(f"Here are the top 10 movies recommended for User ID {user_id}.")
        for index,row in recommendation_df.iterrows():
            poster_url=get_poster(row["movie_name"])
            col1,col2=st.columns([1,4])
            with col1:
                if poster_url:
                    st.image(poster_url,width=120)
                else:
                    st.markdown("🎬")
                    st.caption("Poster unavailable")
            with col2:
                st.markdown(f"### {index+1}. {row['movie_name']}")
                st.markdown(f"⭐ Predicted Rating: **{row['predicted_rating']:.2f} / 5**")
                st.caption("Recommended based on your predicted preferences.")
            st.markdown("---")
        st.success("Recommendations generated successfully!")
        
          
                 


  