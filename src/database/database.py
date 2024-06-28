from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base

engine = create_engine('sqlite:///local_db_file.db', connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autoflush=False, bind=engine)

Base = declarative_base()




