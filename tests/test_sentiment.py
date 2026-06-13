import pandas as pd


def test_sentiment_file_exists():

    df = pd.read_csv(
        "sentiment/output/sentiment_results.csv"
    )

    assert len(df) > 0


def test_sentiment_column():

    df = pd.read_csv(
        "sentiment/output/sentiment_results.csv"
    )

    assert "sentiment_label" in df.columns