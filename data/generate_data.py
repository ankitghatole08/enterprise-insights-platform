from faker import Faker
import polars as pl
import random
from datetime import datetime, timedelta

fake = Faker()

NUM_EMPLOYEES = 10000
NUM_SURVEYS = 50000

departments = [
    "Engineering",
    "Sales",
    "HR",
    "Finance",
    "Marketing",
    "Operations",
    "Customer Success"
]

regions = [
    "Germany",
    "USA",
    "India",
    "UK",
    "France",
    "Canada"
]

positive_comments = [
    "Great manager support and collaboration.",
    "I enjoy working with my team.",
    "Career growth opportunities are excellent.",
    "Work life balance is very good.",
    "The company culture is positive and inclusive.",
    "Leadership communicates effectively."
]

negative_comments = [
    "Promotion process lacks transparency.",
    "Workload is often too high.",
    "Communication from leadership can improve.",
    "Career progression is unclear.",
    "Resources are limited for the team.",
    "Work life balance needs improvement."
]

mixed_comments = [
    "Team is supportive but workload is challenging.",
    "Good culture but career growth could improve.",
    "Manager is helpful but processes are slow.",
    "Interesting projects but staffing is limited.",
    "Strong leadership but communication can improve."
]

employees = []

for employee_id in range(1, NUM_EMPLOYEES + 1):

    employees.append(
        {
            "employee_id": employee_id,
            "department": random.choice(departments),
            "region": random.choice(regions),
            "tenure_years": round(random.uniform(0.5, 15), 1),
            "remote_worker": random.choice([0, 1]),
            "salary_band": random.choice(
                ["Junior", "Mid", "Senior", "Lead"]
            )
        }
    )

employee_df = pl.DataFrame(employees)

responses = []

for response_id in range(1, NUM_SURVEYS + 1):

    employee = random.randint(1, NUM_EMPLOYEES)

    manager_support = random.randint(1, 10)
    career_growth = random.randint(1, 10)
    work_life_balance = random.randint(1, 10)
    compensation = random.randint(1, 10)

    engagement_score = round(
        (
            manager_support
            + career_growth
            + work_life_balance
            + compensation
        )
        / 4,
        2,
    )

    experiment_group = random.choice(
        ["Program_A", "Program_B"]
    )

    comment_pool = random.choice(
        [
            positive_comments,
            negative_comments,
            mixed_comments,
        ]
    )

    feedback_text = random.choice(comment_pool)

    survey_date = (
        datetime.today()
        - timedelta(days=random.randint(0, 730))
    ).date()

    responses.append(
        {
            "response_id": response_id,
            "employee_id": employee,
            "survey_date": survey_date,
            "manager_support": manager_support,
            "career_growth": career_growth,
            "work_life_balance": work_life_balance,
            "compensation": compensation,
            "engagement_score": engagement_score,
            "experiment_group": experiment_group,
            "feedback_text": feedback_text
        }
    )

responses_df = pl.DataFrame(responses)

employee_df.write_csv(
    "data/employees.csv"
)

responses_df.write_csv(
    "data/survey_responses.csv"
)

print("employees.csv created")
print("survey_responses.csv created")