import os
import urllib
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, inspect

# Load variables from the .env file
load_dotenv()

server = os.getenv("DB_SERVER")
database = os.getenv("DB_NAME")

# Builds the ODBC connection string using Windows Authentication
params = urllib.parse.quote_plus(
    f"DRIVER={{ODBC Driver 17 for SQL Server}};"
    f"SERVER={server};"
    f"DATABASE={database};"
    f"Trusted_Connection=yes;"
)

engine = create_engine(f"mssql+pyodbc:///?odbc_connect={params}")
inspector = inspect(engine)

# Exports every table in the 'dbo' schema to its own CSV file
for table_name in inspector.get_table_names(schema="dbo"):
    df = pd.read_sql_table(table_name, engine, schema="dbo")
    df.to_csv(f"{table_name}.csv", index=False)
    print(f"Exported {table_name}.csv")
