from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL  = "sqlite:///C:\\Users\\Tore\\Desktop\\fastapi-flask-sqlalchemy-main\\DBcon\\db.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread":False})

SessionLocal = sessionmaker(autoflush=False, bind=engine)

Base = declarative_base()