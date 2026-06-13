import os
import requests
import pandas as pd

from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()


def get_engine():

    return create_engine(
        f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
        f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}"
        f"/{os.getenv('DB_NAME')}"
    )


def generate_ai_summary(prompt):

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "qwen2.5:1.5b",
            "prompt": prompt,
            "stream": False
        },
        timeout=300
    )

    return response.json()["response"]