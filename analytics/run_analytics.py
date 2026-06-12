import os

import pandas as pd
from dotenv import load_dotenv
from scipy.stats import pearsonr
from scipy.stats import f_oneway
from scipy.stats import ttest_ind
from sqlalchemy import create_engine

import statsmodels.api as sm

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
ON sr.employee_id = e.employee_id
"""

df = pd.read_sql(query, engine)

print(f"Rows Loaded: {len(df)}")

results = []

# --------------------------------------------------
# Correlation
# --------------------------------------------------

corr, pvalue = pearsonr(
    df["career_growth"],
    df["engagement_score"]
)

results.append(
    {
        "analysis": "career_growth_vs_engagement",
        "metric": corr,
        "p_value": pvalue
    }
)

# --------------------------------------------------
# ANOVA
# --------------------------------------------------

groups = []

for dept in df["department"].unique():

    groups.append(
        df[
            df["department"] == dept
        ]["engagement_score"]
    )

anova_stat, anova_p = f_oneway(*groups)

results.append(
    {
        "analysis": "department_anova",
        "metric": anova_stat,
        "p_value": anova_p
    }
)

# --------------------------------------------------
# Regression
# --------------------------------------------------

X = df[
    [
        "manager_support",
        "career_growth",
        "work_life_balance",
        "compensation"
    ]
]

X = sm.add_constant(X)

y = df["engagement_score"]

model = sm.OLS(y, X).fit()

results.append(
    {
        "analysis": "regression_r_squared",
        "metric": model.rsquared,
        "p_value": None
    }
)

# --------------------------------------------------
# A/B Testing
# --------------------------------------------------

group_a = df[
    df["experiment_group"] == "Program_A"
]["engagement_score"]

group_b = df[
    df["experiment_group"] == "Program_B"
]["engagement_score"]

t_stat, t_pvalue = ttest_ind(
    group_a,
    group_b
)

results.append(
    {
        "analysis": "ab_test",
        "metric": t_stat,
        "p_value": t_pvalue
    }
)

results_df = pd.DataFrame(results)

results_df.to_csv(
    "analytics/output/analytics_results.csv",
    index=False
)

with open(
    "analytics/output/regression_summary.txt",
    "w",
    encoding="utf-8"
) as file:

    file.write(
        model.summary().as_text()
    )

print("Analytics completed")