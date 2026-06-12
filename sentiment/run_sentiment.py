import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

df = pd.read_csv(
    "data/survey_responses.csv"
)

analyzer = SentimentIntensityAnalyzer()

scores = []

for text in df["feedback_text"]:

    sentiment = analyzer.polarity_scores(
        str(text)
    )

    scores.append(
        sentiment["compound"]
    )

df["sentiment_score"] = scores

def classify(score):

    if score >= 0.05:
        return "Positive"

    if score <= -0.05:
        return "Negative"

    return "Neutral"

df["sentiment_label"] = df[
    "sentiment_score"
].apply(classify)

df.to_csv(
    "sentiment/output/sentiment_results.csv",
    index=False
)

print("Sentiment analysis complete")