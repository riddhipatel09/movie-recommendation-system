import pickle
import streamlit as st
import requests

# -------------------- CONFIG --------------------
API_KEY = "8265bd1679663a7ea12ac168da84d2e8"
PLACEHOLDER_URL = "https://via.placeholder.com/500x750?text=No+Image"

st.set_page_config(page_title="Movie Recommender", layout="wide")

# -------------------- FETCH POSTER --------------------
@st.cache_data
def fetch_poster(movie_id):
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US"
        response = requests.get(url, timeout=5)

        if response.status_code != 200:
            return None

        data = response.json()
        poster_path = data.get("poster_path")

        if poster_path is None:
            return None

        return "https://image.tmdb.org/t/p/w500/" + poster_path

    except:
        return None


# -------------------- RECOMMENDATION LOGIC (OPTION-1) --------------------
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(
        list(enumerate(similarity[index])),
        reverse=True,
        key=lambda x: x[1]
    )

    recommended_movie_names = []
    recommended_movie_posters = []

    for i in distances[1:]:
        movie_id = movies.iloc[i[0]].movie_id
        poster = fetch_poster(movie_id)

        # 👉 SKIP movies without posters
        if poster is None:
            continue

        recommended_movie_names.append(movies.iloc[i[0]].title)
        recommended_movie_posters.append(poster)

        if len(recommended_movie_names) == 5:
            break

    return recommended_movie_names, recommended_movie_posters


# -------------------- UI --------------------
st.title("Movie Recommender System")
st.markdown("Select a movie and get recommendations")

movies = pickle.load(open('movies.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

movie_list = movies['title'].values

selected_movie = st.selectbox(
    "Type or select a movie",
    movie_list
)

if st.button("Show Recommendation"):

    names, posters = recommend(selected_movie)

    st.subheader("Recommended Movies")

    cols = st.columns(5)

    for i in range(5):
        with cols[i]:
            st.image(posters[i], use_container_width=True)
            st.caption(names[i])
