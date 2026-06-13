import pandas as pd


def test_analytics_results_exist():

    df = pd.read_csv(
        "analytics/output/analytics_results.csv"
    )

    assert len(df) > 0


def test_required_columns():

    df = pd.read_csv(
        "analytics/output/analytics_results.csv"
    )

    required = [
        "analysis",
        "metric",
        "p_value"
    ]

    for col in required:

        assert col in df.columns