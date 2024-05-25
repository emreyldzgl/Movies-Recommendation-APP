import base64
import streamlit as st
import pandas as pd

from ContentBasedRecommendation import content_based_recommender, cosine

df = pd.read_csv("dataset/imdb_top_1000.csv")


def get_img_as_base64(file):
    with open(file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()


img = get_img_as_base64("./image/background.png")
page_bg_img = f"""
<style>
[data-testid="stAppViewContainer"] > .main {{
background-image:url("data:image/png;base64,{img}");
background-size: cover;
background-position: center top;
background-repeat: no-repeat;
background-attachment: fixed;
}}
[data-testid="stHeader"]
{{background: rgba(0, 0, 0, 0.2);}}
<style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)

st.markdown("""
        <style>
            .title {
                text-align: center;
                font-family: Yellow peace;
                font-weight: lighter;
                color: rgba(255, 255, 255, 1);
                font-size: 2.5rem;
                padding-bottom: 20px;
            }
            .me {
                text-align: center;
                font-family: Yellow peace;
                color: rgba(94, 78, 207);
                font-size: 1 rem;
                padding: 0;
                margin: 0;
            }
            .a {
                text-align: center;
                font-family: Yellow peace;
                color: rgba(94, 78, 207);
                padding: 0;
                margin: 0;
            }

        </style>
    """, unsafe_allow_html=True)
st.markdown("<h1 class='title'>🎞 MOVIE RECOMMENDATION 🎞 </h1>", unsafe_allow_html=True)

tab1, tab2 = st.tabs(["Recommendation", "Details"])
st.markdown("""
    <style>
    div[role="tablist"] {
        justify-content: center;
    }
    </style>
    """, unsafe_allow_html=True)

with tab1:

    col1, col2 = st.columns(2)
    movies = col1.selectbox("The Movie You're Watching:", df["Series_Title"])

    # Seçilen filmin poster linkini al
    selected_movie_poster = df[df["Series_Title"] == movies]["Poster_Link"].values[0]
    col2.image(selected_movie_poster, width=70)

    count = st.slider("Number of Movies to Recommend:", min_value=0, max_value=10, step=1)
    st.markdown("""
        <style>
        .stSlider {
            width: 300px !important;  /* Change the width as needed */
        }
        </style>
        """, unsafe_allow_html=True)
    if st.button("Recommend"):
        recommendations = content_based_recommender(movies, cosine, count, df)
        num_columns = 5
        columns = st.columns(num_columns)

        for idx, recommendation in enumerate(recommendations):
            col_idx = idx % num_columns
            with columns[col_idx]:
                poster_link = df[df["Series_Title"] == recommendation]["Poster_Link"].values[0]
                IMDB = df[df["Series_Title"] == recommendation]["IMDB_Rating"].values[0]
                with columns[col_idx]:
                    st.image(poster_link, width=100)
                    st.write(f"**Title:** {recommendation}" f"\n\n**Rating:** {IMDB}")
with tab2:

    recommendations = content_based_recommender(movies, cosine, count, df)
    num_columns = 2
    columns = st.columns(num_columns)
    for idx, recommendation in enumerate(recommendations):
        col_idx = idx % num_columns
        with columns[col_idx]:
            poster_link = df[df["Series_Title"] == recommendation]["Poster_Link"].values[0]
            st.image(poster_link, width=120)

            Director = df[df["Series_Title"] == recommendation]["Director"].values[0]
            Star1 = df[df["Series_Title"] == recommendation]["Star1"].values[0]
            Star2 = df[df["Series_Title"] == recommendation]["Star2"].values[0]
            Star3 = df[df["Series_Title"] == recommendation]["Star3"].values[0]
            IMDB = df[df["Series_Title"] == recommendation]["IMDB_Rating"].values[0]
            Genre = df[df["Series_Title"] == recommendation]["Genre"].values[0]
            Overview = df[df["Series_Title"] == recommendation]["Overview"].values[0]
            Runtime_ = df[df["Series_Title"] == recommendation]["Runtime"].values[0]

            st.write(f"**Director:** {Director}\n" f"\n" f"**Actor:** {Star1}\n" f"\n" f"**Actor:** {Star2}\n"
                     f"\n" f"**Actor:** {Star3}\n"f"**Title:** {recommendation}\n" f"\n" f"**Genre:** {Genre}\n"
                     f"\n" f"**Overview:** {Overview}\n" f"\n" f"**Runtime:** {Runtime_}\n" f"\n**Rating:** {IMDB}")

