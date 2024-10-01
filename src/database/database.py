from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .model import Base
from sqlalchemy.orm import declarative_base
# from model import Summary

from sqlalchemy import Column, Integer, String, DateTime
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker
# from sqlalchemy import create_engine


# optional argument for many threads: connect_args={"check_same_thread": False
# engine = create_engine('sqlite:///local_db_file.db')
# Session = sessionmaker(autoflush=False, bind=engine)
#
# Base = declarative_base()

# Base = declarative_base()
#
# class Summary(Base):
#     __tablename__ = 'summaries'
#     id = Column(Integer, primary_key=True)
#     video_title = Column(String, nullable=False)
#     timestamp = Column(String, nullable=True)
#     video_url = Column(String, nullable=False)
#     summary = Column(String, nullable=True)
#     method_used = Column(String, nullable=True)
#
#     def __repr__(self):
#         return f"<Summary(id={self.id}, timestamp='{self.timestamp}', url='{self.video_title}', nickname='{self.video_url}')>"
#

engine = create_engine('sqlite:///local_db_file.db', connect_args={"check_same_thread": False})


SessionLocal = sessionmaker(autoflush=False, bind=engine)
Base.metadata.create_all(engine)




