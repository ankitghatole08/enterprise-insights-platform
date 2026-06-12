import json
import requests
import pandas as pd

analytics = pd.read_csv(
    "analytics/output/analytics_results.csv"
)

sentiment = pd.read_csv(
    "sentiment/output/sentiment_results.csv"
)

positive_pct = round(
    (
        sentiment["sentiment_label"]
        .eq("Positive")
        .mean()
    ) * 100,
    2
)

negative_pct = round(
    (
        sentiment["sentiment_label"]
        .eq("Negative")
        .mean()
    ) * 100,
    2
)

prompt = f"""
You are a workforce analytics consultant.

Generate a concise executive summary.

Positive Sentiment: {positive_pct}%

Negative Sentiment: {negative_pct}%

Analytics:

{analytics.to_string(index=False)}

Provide:

1. Key Findings
2. Risks
3. Recommendations

Maximum 300 words.
"""

response = requests.post(
    "http://localhost:11434/api/generate",
    json={
        "model": "gemma:2b",
        "prompt": prompt,
        "stream": False
    }
)

output = response.json()

with open(
    "ai_insights/output/executive_summary.txt",
    "w",
    encoding="utf-8"
) as file:

    file.write(
        output["response"]
    )

print("Executive summary generated")