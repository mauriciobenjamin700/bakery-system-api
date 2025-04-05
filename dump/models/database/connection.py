import decouple
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DB_URL= "postgresql://postgres:postgres@localhost:3000/postgres"
print("-------------------------------")
print(DB_URL)
print("-------------------------------")
engine = create_engine(DB_URL, pool_pre_ping=True)
Session = sessionmaker(bind=engine)
