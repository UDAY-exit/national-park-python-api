
import os
from urllib.parse import quote_plus

from dotenv import load_dotenv

load_dotenv()

connection_string = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    r"SERVER=(localdb)\MSSQLLocalDB;"
    "DATABASE=NationalPark_Python_DB;"
    "Trusted_Connection=yes;"
)

class Config:
    SQLALCHEMY_DATABASE_URI = (
        "mssql+pyodbc:///?odbc_connect="
        + quote_plus(connection_string)
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
