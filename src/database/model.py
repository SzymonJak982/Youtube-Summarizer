from sqlalchemy import Column, Integer, String  #, DateTime
from sqlalchemy.ext.declarative import declarative_base

# optional argument for many threads: connect_args={"check_same_thread": False
# engine = create_engine('sqlite:///local_db_file.db')
# Session = sessionmaker(autoflush=False, bind=engine)

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





