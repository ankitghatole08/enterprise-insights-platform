import os
import requests

import pandas as pd
import plotly.express as px
import streamlit as st

from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title="Enterprise Insights Platform",
    layout="wide"
)

# --------------------------------------------------
# DATABASE
# --------------------------------------------------

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
ON sr.employee_id = e.employee_id
"""

df = pd.read_sql(query, engine)

sentiment_df = pd.read_csv(
    "sentiment/output/sentiment_results.csv"
)

df["sentiment_score"] = sentiment_df["sentiment_score"]
df["sentiment_label"] = sentiment_df["sentiment_label"]

# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

st.sidebar.title("Filters")

department_filter = st.sidebar.multiselect(
    "Department",
    sorted(df["department"].unique()),
    default=sorted(df["department"].unique())
)

region_filter = st.sidebar.multiselect(
    "Region",
    sorted(df["region"].unique()),
    default=sorted(df["region"].unique())
)

experiment_filter = st.sidebar.multiselect(
    "Experiment Group",
    sorted(df["experiment_group"].unique()),
    default=sorted(df["experiment_group"].unique())
)

filtered_df = df[
    (df["department"].isin(department_filter))
    & (df["region"].isin(region_filter))
    & (df["experiment_group"].isin(experiment_filter))
]

csv_data = filtered_df.to_csv(
    index=False
)

st.sidebar.download_button(
    label="Download Filtered Dataset",
    data=csv_data,
    file_name="filtered_dataset.csv",
    mime="text/csv"
)

# --------------------------------------------------
# TITLE
# --------------------------------------------------

st.title(
    "Enterprise Insights & Decision Intelligence Platform"
)

# --------------------------------------------------
# KPI SECTION
# --------------------------------------------------

total_responses = len(filtered_df)

avg_engagement = round(
    filtered_df["engagement_score"].mean(),
    2
)

positive_pct = round(
    (
        filtered_df["sentiment_label"]
        .eq("Positive")
        .mean()
    ) * 100,
    2
)

negative_pct = round(
    (
        filtered_df["sentiment_label"]
        .eq("Negative")
        .mean()
    ) * 100,
    2
)

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Responses",
    f"{total_responses:,}"
)

col2.metric(
    "Avg Engagement",
    avg_engagement
)

col3.metric(
    "Positive %",
    f"{positive_pct}%"
)

col4.metric(
    "Negative %",
    f"{negative_pct}%"
)

# --------------------------------------------------
# TABS
# --------------------------------------------------

tab1, tab2, tab3, tab4 = st.tabs(
    [
        "Workforce Insights",
        "Sentiment Analysis",
        "Statistics",
        "AI Insights"
    ]
)

# --------------------------------------------------
# TAB 1
# --------------------------------------------------

with tab1:

    st.subheader(
        "Engagement by Department"
    )

    department_chart = (
        filtered_df
        .groupby("department")["engagement_score"]
        .mean()
        .reset_index()
    )

    fig = px.bar(
        department_chart,
        x="department",
        y="engagement_score",
        color="engagement_score",
        title="Average Engagement by Department"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.subheader(
        "Career Growth vs Engagement"
    )

    fig2 = px.scatter(
        filtered_df,
        x="career_growth",
        y="engagement_score",
        color="department",
        title="Career Growth vs Engagement"
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )

# --------------------------------------------------
# TAB 2
# --------------------------------------------------

with tab2:

    sentiment_counts = (
        filtered_df["sentiment_label"]
        .value_counts()
        .reset_index()
    )

    sentiment_counts.columns = [
        "sentiment",
        "count"
    ]

    fig3 = px.pie(
        sentiment_counts,
        names="sentiment",
        values="count",
        title="Sentiment Distribution"
    )

    st.plotly_chart(
        fig3,
        use_container_width=True
    )

    st.subheader(
        "Employee Comments"
    )

    st.dataframe(
        filtered_df[
            [
                "feedback_text",
                "sentiment_label",
                "sentiment_score"
            ]
        ],
        use_container_width=True,
        height=400
    )

# --------------------------------------------------
# TAB 3
# --------------------------------------------------

with tab3:

    analytics_df = pd.read_csv(
        "analytics/output/analytics_results.csv"
    )

    st.subheader(
        "Statistical Results"
    )

    st.dataframe(
        analytics_df,
        use_container_width=True
    )

    # ------------------------------------------
    # Executive Summary Metrics
    # ------------------------------------------

    st.subheader(
        "Regression Insights"
    )

    col1, col2 = st.columns(2)

    col1.metric(
        "R² Score",
        "0.932"
    )

    col2.metric(
        "Adjusted R²",
        "0.932"
    )

    st.success(
        """
The regression model explains approximately 93.2% of the variation in employee engagement scores.

Key drivers of engagement:

• Manager Support

• Career Growth

• Work-Life Balance

• Compensation

All predictors are statistically significant (p < 0.001).
"""
    )

    # ------------------------------------------
    # Full Regression Output
    # ------------------------------------------

    with open(
        "analytics/output/regression_summary.txt",
        "r",
        encoding="utf-8"
    ) as file:

        regression_text = file.read()

    with st.expander(
        "View Full Regression Output"
    ):

        st.code(
            regression_text,
            language="text"
        )

# --------------------------------------------------
# TAB 4
# --------------------------------------------------

with tab4:

    st.subheader(
        "AI Executive Insights"
    )

    st.info(
        "Generate executive-level workforce insights based on the currently selected filters."
    )

    if st.button(
        "Generate AI Summary",
        type="primary"
    ):

        avg_engagement = round(
            filtered_df["engagement_score"]
            .mean(),
            2
        )

        positive_pct = round(
            (
                filtered_df["sentiment_label"]
                .eq("Positive")
                .mean()
            ) * 100,
            2
        )

        negative_pct = round(
            (
                filtered_df["sentiment_label"]
                .eq("Negative")
                .mean()
            ) * 100,
            2
        )

        top_department = (
            filtered_df.groupby("department")[
                "engagement_score"
            ]
            .mean()
            .idxmax()
        )

        bottom_department = (
            filtered_df.groupby("department")[
                "engagement_score"
            ]
            .mean()
            .idxmin()
        )

        analytics_df = pd.read_csv(
            "analytics/output/analytics_results.csv"
        )

        prompt = f"""
You are a Senior People Analytics Consultant.

Analyze the following workforce analytics data.

Department Filter:
{department_filter}

Region Filter:
{region_filter}

Experiment Group Filter:
{experiment_filter}

Average Engagement:
{avg_engagement}

Positive Sentiment:
{positive_pct}%

Negative Sentiment:
{negative_pct}%

Top Performing Department:
{top_department}

Lowest Performing Department:
{bottom_department}

Statistical Results:
{analytics_df.to_string(index=False)}

Provide:

1. Executive Summary
2. Key Findings
3. Risks
4. Recommendations

Use bullet points.

Maximum 300 words.
"""

        with st.spinner(
            "Analyzing workforce data and generating AI recommendations..."
        ):

            response = requests.post(
                "http://localhost:11434/api/generate",
                json={
                    "model": "qwen2.5:1.5b",
                    "prompt": prompt,
                    "stream": False
                },
                timeout=300
            )

            result = response.json()

        st.success(
            "Executive Summary Generated"
        )

        st.markdown(
            result["response"]
        )

        report_name = (
        "reports/executive_summary.txt"
        )

        with open(
            report_name,
            "w",
            encoding="utf-8"
        ) as file:

            file.write(
                result["response"]
            )

        with open(
            report_name,
            "r",
            encoding="utf-8"
        ) as file:

            st.download_button(
                label="Download Summary",
                data=file,
                file_name="executive_summary.txt",
                mime="text/plain"
            )