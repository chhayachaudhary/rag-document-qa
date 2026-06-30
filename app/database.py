from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

#SQlite database file will be created in your project root
DATABASE_URL = "sqlite:///./app.db"

#echo=true shows the actual sql queries in terminal = helps in understanding/learning
engine= create_engine(DATABASE_URL,connect_args={"check_same_thread": False}, echo=True)

SessionLocal =sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base=declarative_base()

#
#
#dependcy function - gives each request its own database session
def get_db():
    db= SessionLocal()
    try:
        yield db
    finally:
        db.close()    


