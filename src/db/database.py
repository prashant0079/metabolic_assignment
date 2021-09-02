import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
load_dotenv(os.path.join(BASE_DIR, ".env"))

SQLALCHEMY_DATABASE_URL = os.environ["DATABASE_URL"]

try:
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
    )

    # Sqlalchemy session created with the help of create_engine
    Session = sessionmaker(bind=engine)
except Exception as e:
    print("Some issue while connecting to database")
    print(f"Issue in detail:{e}")

# Used by all the models
Base = declarative_base()
