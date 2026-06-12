import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy import text

load_dotenv()

engine = create_engine(
    f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
    f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}"
    f"/{os.getenv('DB_NAME')}"
)

with open(
    "sql/create_tables.sql",
    "r",
    encoding="utf-8"
) as file:
    sql_script = file.read()

with engine.connect() as conn:

    for statement in sql_script.split(";"):

        statement = statement.strip()

        if statement:

            conn.execute(text(statement))

    conn.commit()

print("Tables created")