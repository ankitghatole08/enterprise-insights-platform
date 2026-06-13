# Enterprise Insights Architecture

```text
Employee Survey Data
        |
        v
  Polars ETL Layer
        |
        v
    PostgreSQL
        |
        +----------------+
        |                |
        v                v
 Statistical      Sentiment Analysis
 Analysis              (VADER)
        |                |
        +-------+--------+
                |
                v
        AI Insights Layer
          (Ollama)
                |
                v
       Streamlit Dashboard
```