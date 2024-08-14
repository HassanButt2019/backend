
import json
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from fastapi import Depends
import os

# SQLite database URL for local development
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

# Create a SQLAlchemy engine
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

# Create a configured "Session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a Base class
Base = declarative_base()



class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        return json.JSONEncoder.default(self, o)


def to_json( data):
        return json.loads(json.dumps(data, cls=JSONEncoder))


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()




