import pandas as pd

df = pd.read_csv(
    "data/survey_responses.csv"
)

assert len(df) > 0

assert df["engagement_score"].isnull().sum() == 0

print("Data quality checks passed")