import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

pd.set_option('display.max_columns', None)
pd.set_option('display.width', 500)
pd.set_option('display.expand_frame_repr', False)

df = pd.read_csv("dataset/imdb_top_1000.csv")
df.head()

df["Overview"].head()


def calculate_cosine_sim(dataframe):
    tfidf = TfidfVectorizer(stop_words='english')
    dataframe['Overview'] = dataframe['Overview'].fillna('')
    tfidf_matrix = tfidf.fit_transform(dataframe['Overview'])
    cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)
    return cosine_sim


cosine = calculate_cosine_sim(df)


def content_based_recommender(title, cosine_sim, count, dataframe):
    # create index
    indices = pd.Series(dataframe.index, index=dataframe['Series_Title'])
    indices = indices[~indices.index.duplicated(keep='last')]
    # title's index
    movie_index = indices[title]
    # similarity scores calculate
    similarity_scores = pd.DataFrame(cosine_sim[movie_index], columns=["score"])
    # Top 10 movies
    movie_indices = similarity_scores.sort_values("score", ascending=False)[1:count+1].index
    return dataframe['Series_Title'].iloc[movie_indices]


content_based_recommender("The Godfather", cosine, 5, df)

