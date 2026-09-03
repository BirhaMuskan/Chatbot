import pyodbc
import os
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    conn = pyodbc.connect(
        f"DRIVER={{ODBC Driver 17 for SQL Server}};"
        f"SERVER={os.getenv('SQL_SERVER')};"
        f"DATABASE={os.getenv('SQL_DATABASE')};"
        f"Trusted_Connection=yes;"
    )
    return conn