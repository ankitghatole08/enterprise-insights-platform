import os

import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()

engine = create_engine(
    f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
    f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}"
    f"/{os.getenv('DB_NAME')}"
)

query = """
SELECT
    sr.*,
    e.department,
    e.region,
    e.tenure_years,
    e.remote_worker,
    e.salary_band
FROM survey_responses sr
JOIN employees e
ON sr.employee_id=e.employee_id
"""

df = pd.read_sql(
    query,
    engine
)

sentiment = pd.read_csv(
    "sentiment/output/sentiment_results.csv"
)

df["sentiment_score"] = sentiment[
    "sentiment_score"
]

df["sentiment_label"] = sentiment[
    "sentiment_label"
]

df.to_csv(
    "dashboard/dashboard_dataset.csv",
    index=False
)

print("Dashboard dataset exported")