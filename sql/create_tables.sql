DROP TABLE IF EXISTS survey_responses;
DROP TABLE IF EXISTS employees;

CREATE TABLE employees
(
    employee_id INTEGER PRIMARY KEY,
    department VARCHAR(100),
    region VARCHAR(100),
    tenure_years NUMERIC,
    remote_worker INTEGER,
    salary_band VARCHAR(50)
);

CREATE TABLE survey_responses
(
    response_id INTEGER PRIMARY KEY,
    employee_id INTEGER,
    survey_date DATE,
    manager_support INTEGER,
    career_growth INTEGER,
    work_life_balance INTEGER,
    compensation INTEGER,
    engagement_score NUMERIC,
    experiment_group VARCHAR(50),
    feedback_text TEXT,

    CONSTRAINT fk_employee
    FOREIGN KEY (employee_id)
    REFERENCES employees(employee_id)
);