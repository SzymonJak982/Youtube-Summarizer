from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .model import Base

# TODO: Create connection to postgres
engine = create_engine('sqlite:///local_db_file.db', connect_args={"check_same_thread": False})


SessionLocal = sessionmaker(autoflush=False, bind=engine)
Base.metadata.create_all(engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



