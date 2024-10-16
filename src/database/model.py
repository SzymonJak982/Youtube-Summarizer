from sqlalchemy import Column, Integer, String, DateTime
# from .database import Base
from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker
# from sqlalchemy import create_engine


# optional argument for many threads: connect_args={"check_same_thread": False
# engine = create_engine('sqlite:///local_db_file.db')
# Session = sessionmaker(autoflush=False, bind=engine)
#
Base = declarative_base()


class Summary(Base):
    __tablename__ = 'summaries'
    id = Column(Integer, primary_key=True)
    video_title = Column(String, nullable=False)
    timestamp = Column(String, nullable=True)
    video_url = Column(String, nullable=False)
    video_id = Column(String, nullable=True)
    summary = Column(String, nullable=True)
    method_used = Column(String, nullable=True)

    def __repr__(self):
        return f"<Summary(id={self.id}, timestamp='{self.timestamp}', url='{self.video_title}', nickname='{self.video_url}')>"


# Base.metadata.create_all(engine)
# session = Session()


# def create_record(local_session: Session, summary: Summary) -> Summary:
#     with local_session as db:
#         try:
#             db.add(summary)
#             db.commit()
#             print("successfully created summary")
#             return summary
#         except Exception as e:
#             print(f"Exception happened: {e}")
#
#
# def delete_record(local_session: Session, summary: Summary):
#     with local_session as db:
#         try:
#             db.delete(summary)
#             db.commit()
#             print("successfully deleted summary")
#
#         except Exception as e:
#             print(f"Unexpected error when deleting user:{e}")
