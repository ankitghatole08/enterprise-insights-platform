import os

import polars as pl
from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

engine = create_engine(
    f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

employees = pl.read_csv(
    "data/employees.csv"
)

survey_responses = pl.read_csv(
    "data/survey_responses.csv"
)

employees.to_pandas().to_sql(
    "employees",
    engine,
    if_exists="append",
    index=False
)

survey_responses.to_pandas().to_sql(
    "survey_responses",
    engine,
    if_exists="append",
    index=False
)

print("Data loaded successfully")