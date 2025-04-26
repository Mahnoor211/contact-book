from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///./contact_book.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
Sessionlocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

Base = declarative_base()


def get_db():
    try:
        db = Sessionlocal()
        yield db
    finally:
        db.close()
