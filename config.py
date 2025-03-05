from dotenv import load_dotenv
import os


load_dotenv()


CONFIG = {
    "database": {
        "type": "PostgreSQL",
        "host": "localhost",
        "port": 5432,
        "user": os.getenv("USERNAME_DB"),
        "password": os.getenv("PASSWORD_DB"),
        "dbname": "smartgymdb"
    }
}