import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer

df = pd.read_csv(
    "data/survey_responses.csv"
)

vectorizer = CountVectorizer(
    stop_words="english",
    max_features=20
)

matrix = vectorizer.fit_transform(
    df["feedback_text"]
)

keywords = vectorizer.get_feature_names_out()

keyword_df = pd.DataFrame(
    {
        "keyword": keywords
    }
)

keyword_df.to_csv(
    "sentiment/output/topics.csv",
    index=False
)

print("Topic extraction complete")